from typing import Dict, Self, List
import copy

class DotDict(dict):
    def __getattr__(self, name):
        if name in self.keys():
            return self[name]
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

    def to_dict(self) -> Dict:
        output_dict: Dict = {}
        for key, value in self.items():
            if isinstance(value, DotDict):
                output_dict[key] = value.to_dict()
            else:
                output_dict[key] = value
        return output_dict
    