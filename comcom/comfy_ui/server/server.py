from typing import Dict, Callable, List
from dataclasses import dataclass
import uuid
import websocket
import urllib.request
import urllib.error
import json
import time
import hashlib
import os
import select
from functools import lru_cache
from rich.console import Console
from pydantic import ValidationError
from comcom.playbook.recipe import Recipe
from comcom.comfy_ui.models.normalized.node_definition.node_definition import NormalizedNodeDefinition

from comcom.comfy_ui.server.exceptions import ComfyConnectionError, ComfyServerError, PromptExecutionError

from comcom.comfy_ui.file_management.remote_file import RemoteFile

from comcom.comfy_ui.server.models.comfy_ui_server_stats import ComfyUIServerStatsRequest
from comcom.comfy_ui.server.models.comfy_ui_server_stats import ComfyUIServerStatsResponse

from comcom.comfy_ui.file_management.remote_file import RemoteFile
from comcom.comfy_ui.file_management.local_file import LocalFile

from comcom.comfy_ui.file_management.media_metadata import MediaMetadata


class ComfyServer:
    def __init__(self, host, port):
        self.console: Console = Console()
        self.host: str = host
        self.port: int = port
        self.client_id: str = str(uuid.uuid4())
        self.stats: ComfyUIServerStatsResponse | None = None
        # Attempt to connect to comfy to get version info
        try:
            url = f"http://{self._url_without_protocol}/{ComfyUIServerStatsRequest.endpoint}"
            server_stats_response = urllib.request.urlopen(url)
        except urllib.error.URLError as e:
            raise ComfyConnectionError("Failed to connect to ComfyUI Server.", self._url_without_protocol, str(e))
        
        self.stats: ComfyUIServerStatsResponse = ComfyUIServerStatsResponse.model_validate_json(server_stats_response.read().decode('utf-8'))
        self.interface_provider = None
        if self.stats.version.get('major') == 0:
            from comcom.comfy_ui.server.interface_adapters.comfy_v0 import ComfyUI_v0_InterfaceProvider
            self.interface_provider = ComfyUI_v0_InterfaceProvider
        else:
            raise Exception(f"Unknown ComfyUI Version: {self.stats.version_str}")
        
        try:
            raw_node_definitions = self.interface_provider.RawNodeDefinitionsModel.model_validate_json(
                json_data=urllib.request.urlopen(f"http://{self._url_without_protocol}/object_info").read().decode('utf-8')
            )
        except urllib.error.URLError as e:
            raise ComfyConnectionError("Failed to fetch node definitions from ComfyUI Server.", self._url_without_protocol, str(e))
        
        self.node_definitions: List[NormalizedNodeDefinition] = raw_node_definitions.to_normalized()

    @property
    def _url_without_protocol(self):
        if self.port:
            return f"{self.host}:{self.port}"
        return self.host
    
    @property
    def _url_with_protocol(self):
        return 'http://' + self._url_without_protocol
    
    def upload_image(self, local_file: LocalFile) -> RemoteFile:
        import requests
        
        request_model = self.interface_provider.ImageUploadRequestModel(
            filename=local_file.name, 
            image_data=local_file.data)
        upload_image_uri = f"http://{self._url_without_protocol}/{request_model.endpoint}"
        try:
            # TODO: Figure how how to make post requests lol
            http_response = requests.post(
                upload_image_uri, 
                files=request_model.files, 
                data=request_model.data
            )
        except requests.exceptions.RequestException as e:
            raise ComfyConnectionError(
                message="Failed to parse response from Comfy Server",
                server_url=upload_image_uri,
                error_message=str(e)
                )
        
        if http_response.status_code != 200:
            raise ComfyServerError(
                message="Failed to upload image: {}".format(str(local_file)),
                server_url=upload_image_uri,
                error_message=http_response.text
            )
        
        try:
            image_upload_response = self.interface_provider.ImageUploadResponseModel.model_validate_json(http_response.content)
        except ValidationError as e:
            # TODO: formalize how we want to handle unexpected responses from the server.
            self.console.print(e)
            self.console.log(f"Error occurred parsing response from comfyui server during {request_model.endpoint} request.")
            self.console.print("Actual returned data:")
            self.console.print(http_response.content)
            raise e
        
        # Now create/overwrite a metadata file next to the local file
        uploaded_image_remote_file = image_upload_response.to_remote_file()
        metadata: MediaMetadata = MediaMetadata.from_local_and_remote_files(local_file, uploaded_image_remote_file)
        metadata.save()

        return uploaded_image_remote_file
    
    def get_remote_file_from_local_file(self, local_file: LocalFile) -> RemoteFile:
        if local_file.metadata_file_exists:
            existing_metadata = MediaMetadata.from_file(local_file.metadata_path)
            if existing_metadata.has_sha1 and local_file.sha1 == existing_metadata.sha1:
                return existing_metadata.remote_file
            
        # upload the file to the server
        return self.upload_image(local_file)
    
    def download_file(self, target: RemoteFile, destination: LocalFile) -> LocalFile:
        print("Downloading {}...".format(target.filename))
        remote_data = urllib.request.urlopen(target.get_full_uri(self._url_with_protocol)).read()
        remote_file_hash = hashlib.sha1(remote_data).hexdigest()
        if destination.metadata_file_exists and destination.sha1 == remote_file_hash:
            return destination

        # Make dirs
        if not os.path.exists(os.path.dirname(destination.path_str)):
            os.makedirs(os.path.dirname(destination.path_str))
        with open(destination.path_str, 'wb') as f:
            f.write(remote_data)
        metadata = MediaMetadata.from_local_and_remote_files(local_file=destination, remote_file=target)
        metadata.save()
        

    def execute_recipe(self, recipe: Recipe, on_node_progress: Callable) -> List[MediaMetadata]:
        # Upload all of the recipe's input images to the comfyui server, and swap the paths.
        load_key_to_remote_file: Dict[str: RemoteFile] = {}
        for load_key, local_file_str in recipe.load.items():
            load_key_to_remote_file[load_key] = self.get_remote_file_from_local_file(LocalFile(path=os.path.join("outputs", local_file_str))).api_name
            print("Replaced load input \"{}\" with \"{}\"".format(local_file_str, load_key_to_remote_file[load_key]))
        api_dict, output_node_id_to_local_path_map = recipe.to_api_dict(self.node_definitions, load_key_to_remote_file)

        submit_prompt_request_model = self.interface_provider.SubmitPromptRequestModel(
            prompt_api_dict=api_dict,
            client_id=self.client_id
        )
        
        try:
            req = urllib.request.Request(
                f'http://{self._url_without_protocol}/{submit_prompt_request_model.endpoint}', 
                data=submit_prompt_request_model.data_json
            )
        except urllib.error.URLError as e:
            raise ComfyConnectionError(self._url_without_protocol, str(e))
        
        try:
            return_data = json.loads(urllib.request.urlopen(req).read())
        except urllib.error.HTTPError as e:
            submit_prompt_error_response_model = self.interface_provider.SubmitPromptErrorResponseModel.model_validate_json(e.read())
            raise PromptExecutionError(str(submit_prompt_error_response_model))

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
        
        #node_outputs = {}
        prompt_history_request = self.interface_provider.PromptHistoryRequestModel(prompt_id=prompt_id)
        try:
            prompt_history_http_response = urllib.request.urlopen(f"http://{self._url_without_protocol}/{prompt_history_request.endpoint}").read()
        except urllib.error.HTTPError as e:
            raise e # TODO: better error reporting
        try:
            prompt_history_response = self.interface_provider.PromptHistoryResponseModel.model_validate_json(prompt_history_http_response)
        except ValidationError as e:
            raise e # TODO: better error reporting
        
        for node_id, output in prompt_history_response.get_output_nodes_from_prompt_id(prompt_id).items():
            for remote_file in output.images:
                local_path = LocalFile(path=os.path.join("outputs", output_node_id_to_local_path_map.get(node_id)))
                remote_file = remote_file.to_remote_file()
                # Save the remote image locally, if it needs to be saved.
                self.download_file(remote_file, local_path)