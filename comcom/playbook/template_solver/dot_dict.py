from typing import Dict, Self, List
import copy

class DotDict(dict):
    def __getattr__(self, name):
        if name in self.keys():
            return self[name]
        elif name == "*":
            return self.str_csv
        elif name == "__deepcopy__":
            return self.get('__deepcopy__')
        raise KeyError(name)

    def __init__(self, d: Dict) -> Self:
        for key in d.keys():
            if isinstance(d[key], dict):
                self[key] = DotDict(copy.deepcopy(d[key]))
            else:
                self[key] = copy.copy(d[key])

    def get_flattened_keys(self) -> List[str]:
        flattened_keys: List[str] = []
        for key in self.keys():
            if isinstance(self[key], DotDict):
                subdict_keys = self[key].get_flattened_keys()
                flattened_keys.extend(["{}.{}".format(key, sdkey) for sdkey in subdict_keys])
            else:
                flattened_keys.append(key)
        return flattened_keys
    
    def get_deep_str_values(self) -> List[str]:
        values: List[str] = []
        for k, v in self.items():
            if isinstance(v, str):
                values.append(v)
            elif isinstance(v, dict):
                values.extend(v.get_deep_str_values())
        return values
    
    @property
    def str_csv(self):
        values: List[str] = [v for v in self.get_deep_str_values() if v]
        return ', '.join(values)

    def to_dict(self) -> Dict:
        output_dict: Dict = {}
        for key, value in self.items():
            if isinstance(value, DotDict):
                output_dict[key] = value.to_dict()
            else:
                output_dict[key] = value
        return output_dict
    