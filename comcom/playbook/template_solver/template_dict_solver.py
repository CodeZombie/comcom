from typing import Dict, Tuple, List
import copy
import re
import itertools
from rich.console import Console
from .exceptions import LoopDetectedException, InvalidKeyException, MaximumResolutionDepthException
from .dot_dict import DotDict


def nested_replace(dictionary: Dict, substring: str, replace_with: str) -> Dict:
    for key in dictionary.keys():
        if isinstance(dictionary[key], Dict):
            dictionary[key] = nested_replace(dictionary[key], substring, replace_with)
        else:
            dictionary[key] = dictionary[key].replace(substring, replace_with)
    return dictionary

def deep_merge_dicts(dict1, dict2):
    """
    Recursively merges dict2 into dict1.
    Values from dict2 will overwrite values from dict1 in case of conflicts,
    unless both values are dictionaries, in which case they are merged recursively.
    """
    merged_dict = dict1.copy()  # Create a copy to avoid modifying dict1 in place

    for key, value in dict2.items():
        if key in merged_dict and isinstance(merged_dict[key], dict) and isinstance(value, dict):
            # If both values are dictionaries, merge them recursively
            merged_dict[key] = deep_merge_dicts(merged_dict[key], value)
        else:
            # Otherwise, overwrite the value in merged_dict with the value from dict2
            merged_dict[key] = value
    return merged_dict

class TemplateDictSolver:
    # TODO: Validate that this regex is correct and not stupid slow
    placeholder_pattern = re.compile(r'(?<!\{)\{([^{}]+)\}(?!\})|^\$(.+)') # Matches '{val}' or '$val' but not '{{val}}'
    # \{([^}]+)\}[^}]|^\$(.+)
    max_iterations: int = 16
    ESCAPED_CURLY_BRACKET_PLACEHOLDER_OPEN = "_!*COMCOM_OPEN_ESCAPE_CURLY_BRACKET*!_"
    ESCAPED_CURLY_BRACKET_PLACEHOLDER_CLOSED = "_!*COMCOM_CLOSED_ESCAPE_CURLY_BRACKET*!_"


    @classmethod
    def _get_unresolved_placeholders_from_value(cls, value: str | List) -> List:
        if isinstance(value, str):
            return list(itertools.chain(*TemplateDictSolver.placeholder_pattern.findall(value)))
        if isinstance(value, list):
            unresolved_placeholders: List = []
            for item in value:
                if isinstance(item, str):
                    unresolved_placeholders.extend(list(itertools.chain(*TemplateDictSolver.placeholder_pattern.findall(item))))
            return unresolved_placeholders
        return []



    @classmethod
    def get_unresolved_placeholder_map(cls, data: Dict) -> Tuple[Dict[str, List[str]], int]:
        """
            Returns a flattened dictionary containing a list of all the unresolved replacements within the dict's string values.
            It also returns a hash representing the values and keys of the dict.

            For example:

            get_unresolved_placeholder_map(
                data={
                    'a': "Hello {subject}",
                    'b': {
                        'c': "Goodbye, {name}"
                    },
                    'd': "$a"
                })
            
            will return:
            (
                {
                    'a': ['subject],
                    'b.c': ['name'],
                    'd': ['a']
                },
                938402384994
            )
        """
        unresolved_placeholders = {}
        for key in data.keys():
            unresolved_placeholders[key] = []
            # if isinstance(data[key], str):
            #     unresolved_placeholders[key] = list(itertools.chain(*TemplateDictSolver.placeholder_pattern.findall(data[key])))
            # elif isinstance(data[key], list):

            if isinstance(data[key], Dict):
                sub_unresolved_placeholder_map, _ = TemplateDictSolver.get_unresolved_placeholder_map(data[key])
                for subdotdict_key in sub_unresolved_placeholder_map.keys():
                    unresolved_placeholders["{}.{}".format(key, subdotdict_key)] = sub_unresolved_placeholder_map[subdotdict_key]
            else:
                unresolved_placeholders[key] = cls._get_unresolved_placeholders_from_value(data[key])

        s = ""
        for key in unresolved_placeholders.keys():
            s += "{}::{}".format(key, ''.join(k for k in unresolved_placeholders[key]))
        return unresolved_placeholders, hash(s)
    
    @classmethod
    def get_non_empty_keys_from_dict_of_lists(cls, dict_of_lists) -> List[str]:
        """
        Given a dictionary containing lists of strings, this will flatten the dictionary, discarding any empty strings
        and return the values as a list.
        """
        non_empty_keys: List[str] = []
        for key in dict_of_lists.keys():
            if dict_of_lists[key]:
                non_empty_keys.append(key)
        return non_empty_keys
        
    @classmethod
    def solve(cls, data: Dict, extra_data_source: Dict = {}) -> Dict:
        history: Dict[int, Dict] = {}
        iteration_count: int = 0

        solved_dict: Dict = copy.deepcopy(data)
        step_history, step_hash = TemplateDictSolver.get_unresolved_placeholder_map(solved_dict)
        history[step_hash] = step_history

        while iteration_count < TemplateDictSolver.max_iterations:
            iteration_count += 1
            TemplateDictSolver._in_place_solve_step(solved_dict, deep_merge_dicts(extra_data_source, solved_dict)) # extra_data_source | solved_dict
            step_history, step_hash = TemplateDictSolver.get_unresolved_placeholder_map(solved_dict)
            unresolved_keys = TemplateDictSolver.get_non_empty_keys_from_dict_of_lists(step_history)
            if not unresolved_keys:
                return solved_dict
            if step_hash in history.keys():
                raise LoopDetectedException(unresolved_keys)
            history[step_hash] = step_history

        # This should never really be reached. 
        # The loop detection system SHOULD catch all loops before they get to this point, but I'm going to leave this here 
        # just in case because if the above code doesn't catch a loop it _will_ result in a complete system crash.
        raise MaximumResolutionDepthException("Maximum resolution depth {} reached without solving for the following keys: {}".format(TemplateDictSolver.max_iterations, unresolved_keys))
    
    # extra_data_source should have {'^': parent.data}

    @classmethod
    def _in_place_solve_step(cls, data: Dict, data_source: Dict):
        dot_dict_data_source: DotDict = DotDict(data_source)

        for key in data.keys():
            if isinstance(data[key], dict):
                try:
                    TemplateDictSolver._in_place_solve_step(data[key], data_source) #data[key].__interior_solve_interpolations(data_source) #  | {'^': self}
                except InvalidKeyException as e:
                    raise InvalidKeyException(
                        entry_key="{}.{}".format(key, e.entry_key), 
                        invalid_key=e.invalid_key, 
                        template_string=e.template_string,
                        available_keys=e.available_keys)
            else:
                try:
                    data[key] = cls._value_solve_step(data[key], dot_dict_data_source)
                except (KeyError, AttributeError) as e:
                    raise InvalidKeyException(
                        entry_key=key, 
                        invalid_key=str(e), 
                        template_string=data[key], 
                        available_keys=dot_dict_data_source.get_flattened_keys())
    @classmethod
    def _value_solve_step(cls, value: str | List[str], dot_dict_data_source: DotDict):
        if isinstance(value, str):
            if value.startswith('$'):
                key_path = value[1:].split('.')
                dot_dict_value = dot_dict_data_source
                # Traverse the key path against dot_dict_data_source
                for v in key_path:
                    if v not in dot_dict_value.keys():
                        raise KeyError(value[1:])
                    dot_dict_value = dot_dict_value.get(v, None)
                value = dot_dict_value
            else:
                value = value \
                .replace("{{", TemplateDictSolver.ESCAPED_CURLY_BRACKET_PLACEHOLDER_OPEN) \
                .replace("}}", TemplateDictSolver.ESCAPED_CURLY_BRACKET_PLACEHOLDER_CLOSED) \
                .format(**dot_dict_data_source) \
                .replace(TemplateDictSolver.ESCAPED_CURLY_BRACKET_PLACEHOLDER_OPEN, "{{") \
                .replace(TemplateDictSolver.ESCAPED_CURLY_BRACKET_PLACEHOLDER_CLOSED, "}}")
            return value
        elif isinstance(value, List):
            output: List[str] = []
            for item in value:
                output.append(cls._value_solve_step(item, dot_dict_data_source))
            return output
        
        return value
