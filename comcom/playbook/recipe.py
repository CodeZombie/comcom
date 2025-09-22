from dataclasses import dataclass
from typing import Dict, Any, Self, List, Optional, Tuple
from typing_extensions import TypeAliasType
from pydantic import BaseModel, field_validator, SkipValidation, Field
import os
import copy
import hashlib
import uuid
import json
from rich.console import Console
from pathlib import Path
from comcom.comfy_ui.file_management.local_file import LocalFile
from comcom.comfy_ui.file_management.media_metadata import MediaMetadata

from comcom.playbook.utils.dict_utils import flatten_dict
from comcom.playbook.template_solver.template_dict_solver import TemplateDictSolver
from comcom.playbook.template_solver.exceptions import InvalidKeyException, LoopDetectedException
from comcom.comfy_ui.models.raw.workflow.version_0_4.workflow import Comfy_V0_4_Workflow
from comcom.comfy_ui.models.normalized.node_definition.node_definition import NormalizedNodeDefinition

from comcom.playbook.exceptions import InvalidNodeInWorkflowExceptionc

def get_sha1_of_file(filepath, chunk_size=4096):
    """
    Calculates the SHA-1 hash of a file's contents.

    Args:
        filepath (str): The path to the file.
        chunk_size (int): The size of chunks to read from the file (in bytes).

    Returns:
        str: The hexadecimal representation of the SHA-1 hash.
    """
    sha1_hash = hashlib.sha1()
    try:
        with open(filepath, 'rb') as f:
            while True:
                chunk = f.read(chunk_size)
                if not chunk:
                    break  # End of file
                sha1_hash.update(chunk)
        return sha1_hash.hexdigest()
    except FileNotFoundError:
        return "File not found."
    except Exception as e:
        return f"An error occurred: {e}"

def deep_merge_dicts(dict1, dict2):
    """
    Recursively merges dict2 into dict1.
    Values from dict2 will overwrite values from dict1 in case of conflicts,
    unless both values are dictionaries, in which case they are merged recursively.
    """
    merged_dict = copy.deepcopy(dict1)

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

TemplatesDict = TypeAliasType(
    'TemplatesDict',
    'Dict[str, str | TemplatesDict]'
)

ValidPrimativeTypes = TypeAliasType(
    'ValidPrimativeTypes',
    'str | int | float | bool | None'
)
ValuesDict = TypeAliasType(
    'ValuesDict',
    'Dict[str,  ValidPrimativeTypes | ValuesDict] | ValidPrimativeTypes'
)



class Recipe(BaseModel):
    uuid: str = Field(default_factory=lambda: str(uuid.uuid4()))
    global_id: Optional[str] = ""
    id: Optional[str | None] = "root"
    workflow: Optional[str | None] = None
    values: Optional[Dict[str, ValuesDict]] = {}
    load: Optional[Dict[str, ValuesDict]] = {}
    nodes: Optional[Dict[str, ValuesDict]] = {}
    save: Optional[Dict[str, str | Dict[str, str | List]]] = {}
    recipes: Optional[Dict[str, Self]] = {}
    templates: Optional[TemplatesDict] = {}

    @property
    def is_executable(self):
        return self.workflow != None

    @property
    def sha1(self):
        recipe_hash = ""
        if self.workflow:
            recipe_hash = get_sha1_of_file(self.workflow)
        recipe_hash += hashlib.sha1(json.dumps(self.values, sort_keys=True).encode('utf-8')).hexdigest()
        recipe_hash += hashlib.sha1(json.dumps(self.load, sort_keys=True).encode('utf-8')).hexdigest()
        recipe_hash += hashlib.sha1(json.dumps(self.nodes, sort_keys=True).encode('utf-8')).hexdigest()
        recipe_hash += hashlib.sha1(json.dumps(self.save, sort_keys=True).encode('utf-8')).hexdigest()
        return hashlib.sha1(recipe_hash.encode('utf-8')).hexdigest()
    
    @property
    def saved_media_metadata(self):
        metadatas: Dict[str, MediaMetadata] = {}
        for save_file in self.save.values():
            if isinstance(save_file, str):
                save_filepath = save_file
            else:
                save_filepath = save_file.get('filename')
            local_filepath = os.path.join("outputs", save_filepath)
            if not os.path.exists(local_filepath):
                metadatas[save_filepath] = None
                continue
            local_file = LocalFile(path=local_filepath)
            if not local_file or not os.path.exists(local_file.metadata_path):
                metadatas[save_filepath] = None
                continue
            metadatas[save_filepath] = MediaMetadata.from_file(local_file.metadata_path)
        return metadatas

    
    @property
    def is_dirty(self):
        this_recipe_hash = self.sha1
        for save_file in self.save.values():
            if isinstance(save_file, str):
                save_filepath = save_file
            else:
                save_filepath = save_file.get('filename')
            local_filepath = os.path.join("outputs", save_filepath)
            if not os.path.exists(local_filepath):
                return True
            local_file = LocalFile(path=local_filepath)
            if not local_file:
                print("Save file \"{}\" does not exist. Re-running".format(local_file.path_str))
                return True
            if not os.path.exists(local_file.metadata_path):
                return True
            metadata = MediaMetadata.from_file(local_file.metadata_path)
            if not metadata:
                print("Save file \"{}\" has no metadata file. Re-running".format(local_file.path_str))
                return True
            if metadata.sha1 != local_file.sha1:
                print("Save file \"{}\"'s sha1 ({}) does not match the sha1 in the metadata ({}). Re-running".format(local_file.path_str, local_file.sha1, metadata.sha1))
                return True
            if metadata.recipe_hash != None and metadata.recipe_hash != this_recipe_hash:
                print("Metadata recipe hash ({}) does not match the actual recipe hash ({}). Rerunning.".format(metadata.recipe_hash, this_recipe_hash))
                return True
        for load_filepath in self.load.values():
            local_filepath = os.path.join("outputs", load_filepath)
            if not os.path.exists(local_filepath):
                return False
            local_file = LocalFile(path=local_filepath)
            metadata = MediaMetadata.from_file(local_file.metadata_path)
            if not metadata:
                return True
            if metadata.sha1 != local_file.sha1:
                return True
        return False

    def __str__(self):
        s = "~ {}\n".format(self.id)
        s += "~ Load:\n"
        for k, v in self.load.items():
            s += "~    {}: {}\n".format(k, v)
        s += "~ Nodes:\n"
        for k, v in self.nodes.items():
            s += "~    {}: {}\n".format(k, v)
        s += "~ Save:\n"
        for k, v in self.save.items():
            s += "~    {}: {}\n".format(k, v)
        return s


    def model_post_init(self, __context):
        for recipe_id, recipe in self.recipes.items():
            recipe.id = recipe_id

    def solve(self, parent_global_id: str = "", parent_values: Dict = {}, parent_templates: Dict = {}):
        self.global_id = f"{parent_global_id}.{self.id}" if parent_global_id else self.id
        active_templates: Dict = deep_merge_dicts(parent_templates, self.templates)
        parent_values_without_grandparent = parent_values.copy()
        parent_values_without_grandparent.pop('^', None)
        try:
            self.values = TemplateDictSolver.solve(self.values, deep_merge_dicts(self.templates, parent_values_without_grandparent) | {'^': parent_values})

            generational_values: Dict = deep_merge_dicts(parent_values_without_grandparent, self.values)
            self.load = TemplateDictSolver.solve(self.load, deep_merge_dicts(active_templates, generational_values) | {'^': parent_values})
            self.nodes = TemplateDictSolver.solve(self.nodes, deep_merge_dicts(active_templates, generational_values) | {'^': parent_values})
            self.save = TemplateDictSolver.solve(self.save, deep_merge_dicts(active_templates, generational_values) | {'^': parent_values})
        except (InvalidKeyException, LoopDetectedException) as e:
            e.recipe_path.insert(0, self.id)
            raise e
        
        for child_recipe in self.recipes.values():
            try:
                child_recipe.solve(
                    self.global_id,
                    generational_values | {'^': parent_values } | {'nodes': self.nodes} | {'save': self.save} | {'load': self.load},
                    active_templates
                    )
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
    
    def get_indented_children(self, indent: int = 0) -> Tuple[str, Self]:
        recipes = []
        recipes.append(
            (
                f"{"    " * indent}{self.id}",
                self
            )
        )
        for recipe in self.recipes.values():
            recipes.extend(recipe.get_indented_children(indent + 1))
        return recipes
    
    def get_recipes_by_uuid(self, uuids: List[str]) -> List[Self]:
        found = []
        if str(self.uuid) in uuids:
            found.append(self)
        
        for child in self.recipes.values():
            f = child.get_recipes_by_uuid(uuids)
            if f:
                found.extend(f)
        return found


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

    