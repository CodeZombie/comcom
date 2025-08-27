import os
from typing import List, Dict, Callable
from comcom.comfy_ui.server.server import ComfyServer
from comcom.playbook.workflow_instance import WorkflowInstance

from comcom.comfy_ui.file_management.image import save_remote_image_locally

class ComCom:
    def __init__(self):
        self._root_path: str | None = os.getcwd()
        self._playbook_filename: str | None = None # Excludes the .yaml extension
        self.comfy_server: ComfyServer = ComfyServer("127.0.0.1", 8188)

    @property
    def playbook_files(self) -> List[str]:
        playbook_files = []
        for file in os.listdir(self.root_path):
            if file.endswith(".yaml"):
                playbook_files.append(file.rstrip(".yaml"))
        return playbook_files
    
    @property
    def root_path(self) -> str:
        return self._root_path

    def set_root_path(self, root_path: str) -> bool:
        absolute_path = os.path.abspath(root_path)
        if os.path.exists(absolute_path) and os.path.isdir(absolute_path):
            self._root_path = absolute_path
        
        # If there's only one playbook in this folder, let's just automatically select it and save everyone some time.
        if len(self.playbook_files) == 1:
            self._playbook_filename = self.playbook_files[0]

            return True
        else:
            return False

    @property
    def playbook_filename(self) -> str:
        return self._playbook_filename
    
    def set_playbook_filename(self, playbook_filename: str) -> bool:
        # strip extension
        playbook_filename = playbook_filename.rstrip(".yaml")
        if playbook_filename not in self.playbook_files:
            return False
        self._playbook_filename = playbook_filename
        return True
    
    def submit_workflow(self, workflow: WorkflowInstance, on_progress_callable: Callable) -> Dict:
        local_path_to_remote_file_map = self.comfy_server.submit_workflow_instance(workflow, on_progress_callable)
        print("local_path_to_remote_file_map")
        print(local_path_to_remote_file_map)
        for local_path, remote_file in local_path_to_remote_file_map.items():
            print("Saving \"{}\" to \"{}\"".format(remote_file.full_filepath, local_path))
            save_remote_image_locally(remote_file.full_filepath, remote_file.filename + " [output]", local_path, 'png')

    def execute_worlflow_by_path(self, workflow_path: str | List[str], on_progress_callable: Callable) -> Dict:
        return self.submit_workflow(self.get_workflow_by_path(workflow_path), on_progress_callable)

    
    @property
    def playbook_path(self) -> str:
        return os.path.join(self.root_path, self.playbook_filename + ".yaml")