from typing import Dict, List
import os
import argparse
import yaml
import random

from rich.console import Console
from rich.prompt import Prompt
from rich.progress import Progress
from rich.live import Live

from comcom.playbook.template_solver.exceptions import InvalidKeyException, LoopDetectedException

from comcom.playbook.recipe import Recipe
from comcom.playbook.deep_yaml import deep_yaml_load

from comcom.comfy_ui.server.exceptions import ComfyConnectionError, ComfyServerError, PromptExecutionError

from comcom.comcom import ComCom

class ComComCLIException(Exception):
    pass

FUN_EMOJIS = [
    'grinning_face_with_smiling_eyes', 
    'zombie', 
    'wrench', 
    'fox_face', 
    'flying_saucer', 
    'flamingo', 
    'ok_woman', 
    'ogre', 
    'muscle', 
    'mouse', 
    'fire',
    'fish',
    'watermelon',
    'maple_leaf',
    ]

class ComComCLI:
    def __init__(self, comcom: ComCom, project_directory: str, recipe_file: str, recipe_path: str, no_input: bool, recursive=False, debug_recipe=None):
        self.console = Console()
        self.comcom = comcom

        self.console.print("\n [b][blue]com[/][cyan]com[/][/] [bright_black]v0.1.0[/]".format(random.choice(FUN_EMOJIS)))
        self.console.print(" [bright_black]the comfyui workflow composer.[/]")
        self.console.print(" [bright_black]https://github.com/CodeZombie/comcom[/]\n")

        if project_directory:
            project_directory = '.'
        
        project_directory = os.path.abspath(project_directory)

        if comcom.set_project_root_path(project_directory):
            self.console.print("Set [bold]project directory[/] to [cyan]{}[/]\n".format(os.path.abspath(project_directory)))
        else:
            raise ComComCLIException("[red]Invalid path: {}".format(os.path.abspath(project_directory)))
        
        if len(comcom.recipe_files) == 0:
            raise ComComCLIException("[red]No recipe files found in {}".format(comcom.project_root_path))
        
        if recipe_file is not None:
            if not comcom.select_recipe_file(recipe_file):
                invalid_recipe_file_message = "[red]Invalid recipe path. Recipe \"{}\" not found in {}".format(recipe_file, comcom.project_root_path)
                if no_input:
                    raise ComComCLIException(invalid_recipe_file_message)
                else:
                    self.console.print(invalid_recipe_file_message)

        if not comcom.selected_recipe and not no_input:
            self.console.print("[blue bold]Select a recipe file:")
            for index, value in enumerate(comcom.recipe_files):
                self.console.print("  [yellow]{}[/]:[bold]{}[/]".format(index + 1, value))
            while comcom.selected_recipe is None:
                selected_recipe_value = input("[bold]Playbook[/] [gray](name or index)[/]: ")
                if selected_recipe_value.isnumeric() and int(selected_recipe_value) > 0 and int(selected_recipe_value) <= len(comcom.recipe_files):
                    selected_recipe_value = comcom.recipe_files[int(selected_recipe_value) - 1]
                    
                if comcom.select_recipe_file(selected_recipe_value):
                    break
                self.console.print("[red]Invalid recipe file name or index: {}".format(selected_recipe_value))

        elif not comcom.selected_recipe and no_input:
            raise ComComCLIException("[red]No playbook specified[/]. Please specify a playbook file by name using the [green]--playbook[/] argument")

        self.console.print("Set [bold]recipe file[/] to [cyan]{}.yaml[/]\n".format(comcom.selected_recipe.id))

        if debug_recipe:
            # import json
            # self.console.print(f"Saving compiled recipe to {debug_recipe}")
            # full_recipe_path: str = os.path.join(project_directory, selected_recipe_value + ".yaml")
            # yaml_dict = deep_yaml_load(open(full_recipe_path, 'r').read())
            # print(yaml_dict)
            # compiled_recipe = json.loads(json.dumps(yaml_dict))
            # with open(debug_recipe, 'w') as f:
            #     yaml.dump(compiled_recipe, f)
            # return None
            with open(debug_recipe, 'w') as f:
                yaml.dump(dict(comcom.selected_recipe), f)


        recipe = None
        if recipe_path:
            recipe = comcom.get_recipe(recipe_path)
        if not recipe:
            if no_input:
                raise ComComCLIException("[red]Invalid recipe path:[/] \"{}\"".format(recipe_path))
            indented_recipes = comcom.selected_recipe.get_indented_children()

            #flattened_recipe_paths = [comcom.selected_recipe.id] if comcom.selected_recipe.is_executable else []
            #flattened_recipe_paths.extend(list(comcom.selected_recipe.get_executable_flattened_children().keys()))
            if len(indented_recipes) == 0:
                raise ComComCLIException("Recipe file \"{}\" is not executable and has no executable recipes.".format(comcom.selected_recipe.id))

            self.console.print("Select a recipe from {}:".format(comcom.selected_recipe.id))
            indented_recipe_names = [v[0] for v in indented_recipes]
            for index, value in enumerate(indented_recipe_names):
                is_dirty = indented_recipes[index][1].is_dirty
                self.console.print("  [yellow]{:03d}[/]: [{}][bold]{}[/][/]".format(
                    index + 1,
                    "red" if is_dirty else "blue", 
                    value))
            while recipe is None:
                selected_recipe_path_value = Prompt.ask("  [bold]Recipe[/] [gray](name or index)[/]: ", default="1")
                if selected_recipe_path_value.isnumeric() and int(selected_recipe_path_value) > 0 and int(selected_recipe_path_value) <= len(indented_recipe_names):
                    recipe = indented_recipes[int(selected_recipe_path_value) - 1][1]
                    #selected_recipe_path_value = indented_recipe_names[int(selected_recipe_path_value) - 1]
                    if recipe:
                        break

                recipe = comcom.get_recipe(selected_recipe_path_value)
                if recipe:
                    break
                self.console.print("[red]Invalid recipe name or index: {}".format(selected_recipe_path_value))

        self.console.print("Set [bold]recipe[/] to [red]{}.yaml[/].[cyan]{}[/]".format(comcom.selected_recipe.id, recipe.id))

        #on_node_progress = lambda node, value, max: self.console.print("[bold]{}[/]: [yellow]{}[/] / [yellow]{}[/]".format(node, value, max))

        self.progress = Progress()
        self.progress_task_ids: Dict = {} # node_id: task_id

        try:
            with Live(self.progress):
                comcom.execute_recipe(recipe, self.on_node_progress)
            
        except (ComfyConnectionError, ComfyServerError, PromptExecutionError) as e:
            raise ComComCLIException("[red][bold]ERROR: [/]{}[/]".format(str(e)))
        
    def on_node_progress(self, node_id, value, max):
        if node_id not in self.progress_task_ids.keys():
            self.progress_task_ids[node_id] = self.progress.add_task("Processing node [bold]#{}[/]".format(node_id), total=max)

        self.progress.update(self.progress_task_ids[node_id], completed=value)
    