import yaml
from yaml.constructor import SafeConstructor
import copy
import os

def deep_merge(base, overrides):
    """
    Returns a new dictionary representing the deep merge of base and overrides.
    """
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
    filename = loader.construct_scalar(node)
    
    # Get the directory of the current YAML file to resolve relative paths
    current_file_path = loader.name
    base_dir = os.path.dirname(current_file_path)
    
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
        with open(referenced_path, 'r') as f:
            # Load the referenced file using a new instance of the same Loader class.
            # This ensures that !reference tags and other custom logic
            # work recursively and consistently
            return yaml.load(f, Loader=type(loader))
    except FileNotFoundError:
        raise yaml.constructor.ConstructorError(
            f"Referenced file not found: '{filename}'",
            node.start_mark
        )
    except RecursionError:
        raise yaml.constructor.ConstructorError(
            "Infinite import cycle occurred attempting to import \"{}\"".format(referenced_path),
            node.start_mark)

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
    
class DeepMergeLoader(yaml.SafeLoader, CircularDetectConstructor):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.processing_stack = []

    Constructor = CircularDetectConstructor

DeepMergeLoader.add_constructor('!import', construct_reference)

def deep_yaml_load(yaml_str: str):
    return yaml.load(yaml_str, Loader=DeepMergeLoader)
