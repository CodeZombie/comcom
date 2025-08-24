from typing import Dict
def flatten_dict(dictionary: Dict) -> Dict:
    output_dict: Dict = {}
    for key, value in dictionary.items():
        if isinstance(value, Dict):
            flattened_subdict = flatten_dict(value)
            for subkey, subvalue in flattened_subdict.items():
                output_dict["{}.{}".format(key, subkey)] = subvalue
        else:
            output_dict[key] = value
    return output_dict
