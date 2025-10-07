import os
from typing import List, Dict, Callable
from comcom.comfy_ui.server.server import ComfyServer
from comcom.playbook.recipe import Recipe
import yaml
from comcom.playbook.deep_yaml import deep_yaml_load

# from comcom.comfy_ui.file_management.image import save_remote_image_locally

# How this works:
# You start it up with a project root path and server info.
# Then you select a Recipe file.
# It gives you a list of recipes within that file to execute
# You choose one, and execute it.
# That's it.

class ComCom:
    def __init__(
            self, 
            project_root_path: str | None = os.getcwd(),
            #selected_recipe_file: str | None = None,  # excludes the .yaml
            server_ip: str = "127.0.0.1", 
            port: int = 8188
        ):
        self._project_root_path: str | None = project_root_path
        #self._selected_recipe_file: str | None = selected_recipe_file # Excludes the .yaml extension
        self._selected_recipe: Recipe | None = None
        self.comfy_server: ComfyServer = ComfyServer(server_ip, port)

    @property
    def recipe_files(self) -> List[str]:
        recipe_files = []
        for file in os.listdir(self.project_root_path):
            if file.endswith(".yaml"):
                recipe_files.append(file[:-len('.yaml')])
        return recipe_files
    
    @property
    def project_root_path(self) -> str:
        return self._project_root_path

    def set_project_root_path(self, project_root_path: str) -> bool:
        absolute_path = os.path.abspath(project_root_path)
        if os.path.exists(absolute_path) and os.path.isdir(absolute_path):
            self._project_root_path = absolute_path
        
        # If there's only one recipe in this folder, let's just automatically select it and save everyone some time.
        if len(self.recipe_files) == 1:
            self.select_recipe_file(self.recipe_files[0])
            #self._selected_recipe_file = 
            return True
        if len(self.recipe_files) > 1:
            return True
        
        return True
    

    @property
    def selected_recipe(self):
        return self._selected_recipe
    
    def select_recipe_file(self, recipe_file: str, and_solve=True) -> bool:
        if recipe_file not in self.recipe_files:
            return False
        full_recipe_path: str = os.path.join(self._project_root_path, recipe_file + ".yaml")
        import json
        self._selected_recipe = Recipe.model_validate(deep_yaml_load(open(full_recipe_path, 'r').read()))
        self._selected_recipe.id = recipe_file
        if and_solve:
            self._selected_recipe.solve()
        return True
    
    def execute_recipe(self, recipe: Recipe, on_progress_callable: Callable, on_preview_image: Callable | None = None) -> List[str]:
        if recipe.is_dirty:
            generated_images = self.comfy_server.execute_recipe(recipe, on_progress_callable, on_preview_image)
            return generated_images
        else:
            print(f"Recipe {recipe.id} does not need to run. Skipping...")
        return []
    
    def get_recipe(self, recipe_path: str):
        recipe_path = recipe_path.split('.')
        
        if recipe_path[0] == self.selected_recipe.id:
            if len(recipe_path) == 1:
                return self.selected_recipe 
            return self.selected_recipe.get_recipe(recipe_path[1:])
        return None
        
    def interrupt(self):
        self.comfy_server.interrupt()

    @property
    def playbook_path(self) -> str:
        return os.path.join(self.project_root_path, self.selected_recipe_file + ".yaml")