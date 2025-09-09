from dataclasses import dataclass
from typing import Dict, Any, Self, List, Optional, Tuple
from typing_extensions import TypeAliasType
from pydantic import BaseModel, field_validator, SkipValidation
import os
from rich.console import Console
from pathlib import Path

from comcom.playbook.utils.dict_utils import flatten_dict
from comcom.playbook.template_solver.template_dict_solver import TemplateDictSolver
from comcom.playbook.template_solver.exceptions import InvalidKeyException, LoopDetectedException
from comcom.comfy_ui.models.raw.workflow.version_0_4.workflow import Comfy_V0_4_Workflow
from comcom.comfy_ui.models.normalized.node_definition.node_definition import NormalizedNodeDefinition

from comcom.playbook.exceptions import InvalidNodeInWorkflowExceptionc

def deep_merge_dicts(dict1, dict2):
    """
    Recursively merges dict2 into dict1.
    Values from dict2 will overwrite values from dict1 in case of conflicts,
    unless both values are dictionaries, in which case they are merged recursively.
    """
    merged_dict = dict1.copy()

    for key, value in dict2.items():
        if key in merged_dict and isinstance(merged_dict[key], dict) and isinstance(value, dict):
            # If both values are dictionaries, merge them recursively
            merged_dict[key] = deep_merge_dicts(merged_dict[key], value)
        else:
            # Otherwise, overwrite the value in merged_dict with the value from dict2
            merged_dict[key] = value
    return merged_dict

@dataclass
class SaveFileRequest:
    output_node_id: str
    local_path: str
    requires_editing: bool = False


ValidPrimativeTypes = TypeAliasType(
    'ValidPrimativeTypes',
    'str | int | float | bool | None'
)
ValuesDict = TypeAliasType(
    'ValuesDict',
    'Dict[str,  ValidPrimativeTypes | ValuesDict] | ValidPrimativeTypes'
)

class Recipe(BaseModel):
    id: Optional[str | None] = "root"
    workflow: Optional[str | None] = None
    values: Optional[Dict[str, ValuesDict]] = {}
    load: Optional[Dict[str, ValuesDict]] = {}
    nodes: Optional[Dict[str, ValuesDict]] = {}
    save: Optional[Dict[str, str | Dict[str, str | List]]] = {}
    recipes: Optional[Dict[str, Self]] = {}

    @property
    def is_executable(self):
        return self.workflow != None

    def model_post_init(self, __context):
        for recipe_id, recipe in self.recipes.items():
            recipe.id = recipe_id

    def solve(self, parent_values: Dict = {}):
        parent_values_without_grandparent = parent_values.copy()
        parent_values_without_grandparent.pop('^', None)
        try:
            self.values = TemplateDictSolver.solve(self.values, parent_values_without_grandparent | {'^': parent_values})
            self.load = TemplateDictSolver.solve(self.load, parent_values_without_grandparent | {'^': parent_values})
            self.nodes = TemplateDictSolver.solve(self.nodes, deep_merge_dicts(parent_values_without_grandparent, self.values) | {'^': parent_values})
            self.save = TemplateDictSolver.solve(self.save, deep_merge_dicts(parent_values_without_grandparent, self.values) | {'^': parent_values})
        except (InvalidKeyException, LoopDetectedException) as e:
            e.recipe_path.insert(0, self.id)
            raise e
        
        for child_recipe in self.recipes.values():
            try:
                child_recipe.solve(deep_merge_dicts(parent_values_without_grandparent, self.values) | {'^': parent_values } | {'nodes': self.nodes} | {'save': self.save} | {'load': self.load})
            except (InvalidKeyException, LoopDetectedException) as e:
                e.recipe_path.insert(0, self.id)
                raise e
            
    def to_api_dict(self, node_definitions: List[NormalizedNodeDefinition], load_remote_file_map: Dict[str, str]) -> Tuple[Dict | List[SaveFileRequest]]:
        console = Console()
        comfy_workflow = Comfy_V0_4_Workflow.model_validate_json(open(os.path.join('workflows', self.workflow)).read()).to_normalized(node_definitions).to_common(node_definitions)
        # Sanity check the workflow:
        for node in comfy_workflow.nodes:
            if '.' in node.title:
                raise InvalidNodeInWorkflowExceptionc(node.title, node.id, self.workflow, "Node names should not contain a '.' character")
        all_solved_values = flatten_dict(self.nodes) | flatten_dict(load_remote_file_map)
        for key, value in all_solved_values.items():
            node_input_path = key.rsplit('.', 1)
            if len(node_input_path) != 2:
                raise Exception("Recipe \"{recipe_id}\"'s Node Input path \"{node_input_path}\" is invalid. Must be formatted like \"<node title/id>.<input_name>\", not whatever that is.".format(recipe_id=self.id, node_input_path=key))
            node_identifier = node_input_path[0]
            input_identifier = node_input_path[1]
            # If the node identifier starts with a $, we want to search by ID
            nodes = []
            if node_identifier.startswith('$'):
                node = comfy_workflow.get_node_by_id(node_identifier[1:])
                if node:
                    nodes.append(node)
            # If we haven't found a node, let's try searching by title.
            # This will allow us to match nodes that have a `$` at the beginning of the title.
            if not nodes:
                nodes = comfy_workflow.get_nodes_by_title(node_identifier)
                if len(nodes) > 1:
                    print("WARNING: more than one node has the title {}. We're going to apply modifications to all of them. Be sure that this is what you want.".format(node_identifier))
            if not nodes:
                
                console.print("[yellow]:warning:  Could not find a node for identifier [/][blue]{}[/]".format(node_identifier))
            for node in nodes:
                input = node.get_input_by_name(input_identifier)

                if not input:
                    raise Exception('Node \"{node_title}\" (identified by \"{node_identifier}\") <type={node_type}> does not have an input called {input_identifier}. Available inputs are: {available_inputs}'.format(
                        node_title=node.title,
                        node_identifier=node_identifier,
                        node_type=node.type,
                        input_identifier=input_identifier,
                        available_inputs=[input.name for input in node.inputs if not input.is_link]
                        ))
                input.value = value
        
            # Reprehensible Hack Alert:

            # So ComfyUI doesn't treat all images on its server the same.
            # Images uploaded manually to the server are stored in an "Input" folder, and images generated by executing workflows
            # are stored in an "Output" folder. Makes sense, right?
            # And when you put a "LoadImage" node in your workflow and give the 'image' field a filename, ComfyUI will, by default, look inside the
            # "Input" folder for the image. This is all making sense to us so far, yeah?
            # WELL,
            # The Comfy Devs realized they need a way of loading images into workflows that exist in different subfolders. 
            # People want to load their "Outputs" as "Inputs", which seems like a fairly common thing to do in a DAG.
            # To solve this how-do-you-identify-which-folder-a-file-in conundrum, however, the Comfy boys decided, in their infinite wisdom, 
            # to not identify subfolders with a prefix, but with a goddamned suffix.
            # Yes sir, "MyCoolImage.png" inside the "Output" folder is not identified as "Output/MyCoolImage.png", but as "MyCoolImage.png [Output]"
            # Posix be damned.
            # However, this isn't the end of the world, we can just write a little @property function to handle this (`RemoteFile.api_name`)
            # Simple enough. Solved, right?
            # Nope. Comfy weren't done yet.
            # They decided, because they didn't want to have a "folder select" field in the normal "LoadImage" node or something, to create an entirely
            # new fucking node to handle loading images from the Output folder. 
            # Fuck me, right? 
            # Throwing a little `folder = "Output" if filename.endswith(" [Output]") else "Input"` in the existing `LoadImage` code is too 
            # good for them; had to spin up a whole new node for this one.
            #
            # Whatever. I took upon this burden of my own volition. This is my fault for writing ComCom in the first place.
            # And who am I to talk after writing `deep_yaml.py`
            #
            # Anyway, our disgusting little hack here is to look through all the nodes in the workflow, and check for any 
            # LoadImage nodes. If their `image` values end with " [Output]", we just swap the node type to `LoadImageOutput`
            # Thankfully, the `LoadImageOutput` node is definitionally compatible with `LoadImage` (They both output (IMAGE, MASK))
            # So nothing else should need to change besides the node type.

            for node in comfy_workflow.nodes:
                if node.type == "LoadImage":
                    image_input = node.get_input_by_name('image')
                    if image_input and image_input.value.endswith(" [Output]"):
                        node.type = "LoadImageOutput"
            # Hack over.

        save_file_requests: List[SaveFileRequest] = []
        for node_id_or_title, value in self.save.items():
            node_ids = []
            if node_id_or_title.startswith('$'):
                node_ids = [node_id_or_title[1:]]
            else:
                node_ids = [node.id for node in comfy_workflow.get_nodes_by_title(node_id_or_title)]
            if not node_ids:
                # TODO: make this a custom exception so we can print it nicer
                raise Exception("Failed to find node: \"{}\" in workflow: \"{}\" in recipe: \"{}\". Available nodes are: {}".format(node_id_or_title, comfy_workflow.id, self.id, [node.title for node in comfy_workflow.nodes]))

            for node_id in node_ids:
                if isinstance(value, str):
                    save_file_requests.append(SaveFileRequest(node_id, value, False))
                elif isinstance(value, Dict):
                    if 'filename' in value.keys():
                        save_file_requests.append(SaveFileRequest(node_id, value.get('filename'), False))
                    for requires_editing_entry in value.get('requires_editing', []):
                        save_file_requests.append(SaveFileRequest(node_id, requires_editing_entry, True))
                        

        # output_node_id_to_local_path_map = {}
        
        # for key, local_path in self.save.items():
        #     if key.startswith('$'):
        #         output_node_id_to_local_path_map[key[:1]] = local_path
        #     else:
        #         for node in comfy_workflow.get_nodes_by_title(key):
        #             output_node_id_to_local_path_map[node.id] = local_path

        return (comfy_workflow.as_api_dict(), save_file_requests)

    def get_recipe(self, path: List[str] | str | None) -> Self | None:
        if isinstance(path, str):
            path = path.split('.')
        if len(path) == 0:
            return None
        if path[0] in self.recipes.keys():
            if len(path) == 1:
                return self.recipes[path[0]]
            return self.recipes[path[0]].get_recipe(path[1:])
        return None


    # def get_recipe_by_path(self, recipe_path: List[str]) -> Self | None:
    #     if len(recipe_path) == 0:
    #         return None
    #     for id, recipe in self.recipes.items():
    #         if id == recipe_path[0]:
    #             if len(recipe_path) == 1:
    #                 return recipe
    #             return recipe.get_recipe_by_path(recipe_path[1:])
    #     return None

    def get_flattened_children(self):
        flattened_dict = {}
        for child_recipe in self.recipes.values():
            flattened_dict["{}.{}".format(self.id, child_recipe.id)] = child_recipe
            for child_id, child in child_recipe.get_flattened_children().items():
                flattened_dict["{}.{}".format(self.id, child_id)] = child
        return flattened_dict
    
    def get_executable_flattened_children(self):
        flat_children = self.get_flattened_children()
        return {k: v for k, v in flat_children.items() if v.is_executable}

    # def print(self, id, prfx=""):
    #     print("{}{}".format(prfx, id))
    #     print("{}  path:".format(prfx))
    #     print("{}    {}".format(prfx, self.path))
    #     print("{}  values:".format(prfx))
    #     for key, value in flatten_dict(self.values).items():
    #         print("{}    {}: {}".format(prfx, key, value))
    #     print("{}  input:".format(prfx))
    #     for key, value in flatten_dict(self.input).items():
    #         print("{}    {}: {}".format(prfx, key, value))
    #     print("{}  output:".format(prfx, prfx))
    #     for key, value in flatten_dict(self.output).items():
    #         print("{}    {}: {}".format(prfx, key, value))
    #     print("{}  workflows: ".format(prfx, prfx))
    #     for key, value in self.workflows.items():
    #         value.print(key, prfx + "    ")
    #     #print("  Children: {}".format([workflow.path for workflow in self.workflows]))

    