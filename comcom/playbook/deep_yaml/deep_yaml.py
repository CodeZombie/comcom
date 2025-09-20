import yaml
from yaml.constructor import SafeConstructor
from yaml.nodes import Node, SequenceNode, ScalarNode, MappingNode
import copy
import os
from rich.console import Console

def unflatten_data(data_dict: dict) -> dict:
    """
    Transforms a dictionary with hierarchical keys (represented by tuples)
    into a nested dictionary structure.

    Args:
        data_dict: The input dictionary, parsed from a YAML file
                   using the custom TupleKeyLoader.

    Returns:
        A nested dictionary where hierarchies are represented by a 'recipes' key.
    """
    root_node = {}
    _process_level(data_dict, root_node)
    return root_node

def _process_level(current_level_dict: dict, parent_node: dict):
    """
    Recursively processes a dictionary level, separating properties (string keys)
    from hierarchical paths (tuple keys) and merging them into the nested structure.

    Args:
        current_level_dict: The dictionary representing the current level of data.
        parent_node: The node in the output structure to which properties and
                     recipes from the current level will be added.
    """

    def node_deep_merge(source: dict, destination: dict) -> dict:
        """
        Recursively merges the source dictionary into the destination dictionary.

        - If a key exists in both and both values are dictionaries, it recurses.
        - Otherwise, the value from the source dictionary overwrites the destination.

        Args:
            source: The dictionary to merge from.
            destination: The dictionary to merge into (will be modified in place).

        Returns:
            The modified destination dictionary.
        """
        for key, value in source.items():
            if isinstance(value, dict) and key in destination and isinstance(destination[key], dict):
                node_deep_merge(value, destination[key])
            else:
                destination[key] = value
        return destination

    properties = {k: v for k, v in current_level_dict.items() if isinstance(k, str)}
    paths = {k: v for k, v in current_level_dict.items() if isinstance(k, tuple)}

    properties = copy.deepcopy(properties)
    paths = copy.deepcopy(paths)

    #parent_node.update(properties)
    node_deep_merge(properties, parent_node)
    
    console = Console()

    for path_parts, value in paths.items():
        parts = path_parts
        current_node = parent_node
        
        for part in parts:
            if 'recipes' not in current_node:
                current_node['recipes'] = {}
            current_node = current_node['recipes'].setdefault(part, {})
        
        if isinstance(value, dict):
            _process_level(value, current_node)
        else:
            print(f"Warning: Value for path '{path_parts}' is a scalar and will be ignored. Path values should be dictionaries.")

def deep_merge(base, overrides):
    """
    Returns a new dictionary representing the deep merge of base and overrides.
    """
    overrides = copy.deepcopy(overrides)
    result = copy.deepcopy(base)

    for key, value in overrides.items():
        if key in result and isinstance(result.get(key), dict) and isinstance(value, dict):
            # If the key exists and both values are dicts, recurse
            result[key] = deep_merge(result[key], value)
        else:
            # Otherwise, just set the value in the new dictionary
            result[key] = value
            
    return result


def construct_reference(loader, node):
    """
    Constructs an object from a referenced YAML file.
    """
    # Get the file path from the YAML node's value
    filenames = []
    if isinstance(node, ScalarNode):
        filenames.append(loader.construct_scalar(node))
    elif isinstance(node, SequenceNode):
        filenames.extend(loader.construct_sequence(node))

    data = {}


    # Get the directory of the current YAML file to resolve relative paths
    current_file_path = loader.name
    base_dir = os.path.dirname(current_file_path)
    
    for filename in filenames:
        # Construct the full path to the referenced file
        referenced_path = os.path.join(base_dir, filename)
        
        # --- SECURITY CHECK ---
        # Ensure the resolved path is within the same directory or a subdirectory
        if not os.path.abspath(referenced_path).startswith(os.path.abspath(base_dir)):
            raise yaml.constructor.ConstructorError(
                f"Reference to '{filename}' is outside the allowed directory.",
                node.start_mark
            )

        try:
            print(os.path.abspath(referenced_path))
            with open(referenced_path, 'r') as f:
                # Load the referenced file using a new instance of the same Loader class.
                # This ensures that !reference tags and other custom logic
                # work recursively and consistently
                
                #data = deep_merge(yaml.load(f, Loader=DeepMergeLoader), data)
                data = deep_merge(deep_yaml_load(f.read()), data)
        except FileNotFoundError:
            raise yaml.constructor.ConstructorError(
                f"Referenced file not found: '{filename}'",
                node.start_mark
            )
        except RecursionError:
            raise yaml.constructor.ConstructorError(
                "Infinite import cycle occurred attempting to import \"{}\"".format(referenced_path),
                node.start_mark)
    return data

# 2. The Constructor is the same, but our call to deep_merge inside it changes slightly.
class CircularDetectConstructor(SafeConstructor):

    def construct_mapping(self, node, deep=True):
        if node in self.processing_stack:
            raise yaml.constructor.ConstructorError(
                "Circular reference detected in merge key", node.start_mark
            )
        
        self.processing_stack.append(node)
        
        mapping = {}
        self.flatten_mapping(node) # This still helps resolve aliases
        for key_node, value_node in node.value:
            key = self.construct_object(key_node, deep=deep)

            value = self.construct_object(value_node, deep=deep)

            if key in mapping and isinstance(mapping.get(key), dict) and isinstance(value, dict):
                mapping[key] = deep_merge(mapping[key], value)
            else:
                mapping[key] = value
        
        self.processing_stack.pop()
        return mapping
    
class DeepMergeLoader(yaml.FullLoader, CircularDetectConstructor):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.processing_stack = []

    Constructor = CircularDetectConstructor

def construct_tuple(loader: DeepMergeLoader, node: Node):
    """Construct a tuple from a YAML sequence."""
    return tuple(loader.construct_sequence(node))

def construct_path_string(loader, node):
    """
    Given a sequence like `[.., path, to, value]`, this will
    return a reverse string-path: `$^.path.to.value`
    """
    if not isinstance(node, SequenceNode):
        if isinstance(node, ScalarNode):
            return loader.construct_scalar(node)
        elif isinstance(node, MappingNode):
            return loader.construct_mapping(node, deep=True)
        else:
            raise Exception("????????")
        
    def conv_key(key):
        if key == '..':
            return '^'
        return str(key)
    
    sequence = loader.construct_sequence(node)
    str_seq = [conv_key(part) for part in sequence]
    return "${}".format('.'.join(str_seq))        

DeepMergeLoader.add_constructor('!import', construct_reference)
#DeepMergeLoader.add_constructor('<<<', construct_reference)
DeepMergeLoader.add_constructor('!path', construct_path_string)
DeepMergeLoader.add_constructor('tag:yaml.org,2002:seq', construct_tuple) 

# def deep_yaml_load(yaml_str: str):
#     from rich.console import Console
    
#     data = yaml.load(yaml_str, Loader=DeepMergeLoader)
#     Console().print(data)
#     if data.get('<<<'):
#         data = deep_merge(data.get('<<<'), data)
#     unflattened_data = unflatten_data(data)
#     return unflattened_data

def resolve_merge_key(data):
    """
    Recursively resolves a data structure by deep-merging dictionaries 
    found under the '<<<' key into their parent dictionary.
    """
    
    # --- Handle Base Cases ---
    
    # If it's a list, recurse on each item
    if isinstance(data, list):
        return [resolve_merge_key(item) for item in data]
    
    # If it's not a dict (or list), return it as-is (e.g., int, str)
    if not isinstance(data, dict):
        return data

    # --- Handle Dictionaries ---
    
    # It's a dictionary.
    # Step 1: Recursively resolve all its child values *first*.
    # This ensures that any nested '<<<' keys are handled before
    # we process the '<<<' key at the current level.
    resolved_children = {}
    for key, value in data.items():
        resolved_children[key] = resolve_merge_key(value)

    # Step 2: Now that all children are resolved, handle the merge
    # at *this* level.
    
    # Start with the base dict (from '<<<'), if it exists and is a dict
    base = {}
    if '<<<' in resolved_children:
        # Get the resolved value of '<<<' and remove it from children
        merge_val = resolved_children.pop('<<<')
        if isinstance(merge_val, dict):
            base = merge_val  # This is our starting point

    # Step 3: Deep-merge the remaining items (the parent's keys)
    # *onto* the base. `resolved_children` now only contains the
    # parent's keys and their *already resolved* values.
    final_result = deep_merge(base, resolved_children)
    
    return final_result


def deep_yaml_load(yaml_str: str):
    
    console = Console()
    console.print()
    data: dict = yaml.load(yaml_str, Loader=DeepMergeLoader)
    data = resolve_merge_key(data)

    unflattened_data = unflatten_data(data)
    return unflattened_data
