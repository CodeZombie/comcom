from typing import Dict, Callable
import uuid
import websocket
import urllib
import json
import time
import select
from functools import lru_cache
from comcom.comfy_ui.models.common.workflow import Workflow
from comcom.comfy_ui.models.raw.node_definitions.version_1_0.node_definitions import Comfy_v1_0_NodeDefinitions
from comcom.comfy_ui.models.normalized.node_definition.node_definition import NormalizedNodeDefinition

from comcom.comfy_ui.server.exceptions import ComfyConnectionError

class ComfyServer:
    def __init__(self, host, port):
        self.host: str = host
        self.port: int = port
        self.client_id: str = str(uuid.uuid4())

    @property
    def _url_without_protocol(self):
        return f"{self.host}:{self.port}"
    
    @lru_cache()
    def get_node_definitions_dict(self) -> Dict:
        try:
            response = urllib.request.urlopen(f"http://{self._url_without_protocol}/object_info")
        except urllib.error.URLError as e:
            raise ComfyConnectionError("Failed to fetch node definitions", self._url_without_protocol, str(e))
        
        return json.loads(response.read().decode('utf-8'))
    
    def submit_workflow_instance(self, workflow: Workflow, on_node_progress: Callable) -> Dict[str, str]:
        node_definitions = Comfy_v1_0_NodeDefinitions.model_validate(self.get_node_definitions_dict()).to_normalized()

        prompt_dict = {
            'prompt': workflow.to_api_dict(node_definitions),
            'client_id': self.client_id
        }
        prompt_json = json.dumps(prompt_dict).encode('utf-8')
        try:
            req = urllib.request.Request(f'http://{self._url_without_protocol}/prompt', data=prompt_json)
        except urllib.error.URLError as e:
            raise ComfyConnectionError(self._url_without_protocol, str(e))
        try:
            return_data = json.loads(urllib.request.urlopen(req).read())
        except urllib.error.HTTPError as e:
            errors = []
            error_dict = json.loads(e.read())
            for node_id, node_error_dict in error_dict.get('node_errors', {}).items():
                for error in node_error_dict.get('errors', []):
                    errors.append(
                        "Node {node_id} ({node_type}) failed with error \"{error_text}.\" [{extra}]".format(
                            node_id=node_id, 
                            node_type=node_error_dict.get('class_type', "Unknown node class type"),
                            error_text=error.get('details', "Unknown error"),
                            extra=error.get('extra_info', "")))            
            for error in errors:
                print("Errors occurred submitting prompt:")
                print("  {}".format(error))

        prompt_id = return_data['prompt_id']

        websocket_connection = websocket.WebSocket()
        websocket_connection.connect(f"ws://{self._url_without_protocol}/ws?clientId={self.client_id}")
        timeout_start_time = time.time()
        try:
            while True:
                if time.time() - timeout_start_time > 30:
                    raise Exception("Timed out waiting for prompt to execute")
                websocket_message, _, _ = select.select([websocket_connection], [], [], 0.1)
                if websocket_message:
                    timeout_start_time = time.time()
                    out = websocket_connection.recv()
                    if isinstance(out, str):
                        message = json.loads(out)
                        message_type = message.get('type')
                        data = message.get('data', {})

                        # if message_type == 'executing':
                        #     if data.get('prompt_id', None) == prompt_id:
                        #         break
                        if message_type == 'status':
                            status = data.get('status', {})
                            exec_info = status.get('exec_info', {})
                            queue_remaining = exec_info.get('queue_remaining', None)
                            if queue_remaining == 0:
                                break
                        elif message_type == 'execution_success':
                            if data.get('prompt_id', None) == prompt_id:
                                break
                        elif message_type == 'progress':
                            if data.get('prompt_id', None) != prompt_id:
                                continue
                            value = data.get('value', None)
                            max = data.get('max', None)
                            node = data.get('node', None)
                            if value is not None and max is not None and node is not None:
                                on_node_progress(node, value, max)
                    else:
                        continue
        finally:
            websocket_connection.close()

        prompt_id = return_data['prompt_id']
        node_outputs = {}
        prompt_history = json.loads(urllib.request.urlopen(f"http://{self._url_without_protocol}/history/{prompt_id}").read())[prompt_id]
        for node_id in prompt_history['outputs']:
            node_output = prompt_history['outputs'][node_id]
            if 'images' in node_output:
                for image in node_output['images']:
                    image_url_data = urllib.parse.urlencode({"filename": image['filename'], "subfolder": image['subfolder'], "type": image['type']})
                    node_outputs[node_id] = f"http://{self._url_without_protocol}/view?{image_url_data}"

        return node_outputs        
