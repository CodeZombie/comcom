from typing import List
class LoopDetectedException(Exception):
    def __init__(self, looping_keys):
        super().__init__(self)
        self.recipe_path = []
        self.looping_keys = looping_keys
    
    def __str__(self):
        return "Loop detected in recipe \"{recipe_path}\" between the following key(s): {keys}".format(
            recipe_path='.'.join([str(rid) for rid in self.recipe_path]),
            keys=', '.join([str(key) for key in self.looping_keys])
        )

class MaximumResolutionDepthException(Exception): pass

class InvalidKeyException(Exception):
    def __init__(self, entry_key: str, invalid_key: str, template_string: str, available_keys: List[str]):
        
        # super().__init__("Attempting to access unknown key {invalid_key} in template \'{entry_key}\': \'{template_string}\'. Available keys: {available_keys}".format(
        #     invalid_key=invalid_key,
        #     entry_key=entry_key,
        #     template_string=template_string,
        #     available_keys=available_keys
        # ))
        super().__init__()
        self.recipe_path = []
        self.entry_key: str = entry_key
        self.invalid_key: str = invalid_key
        self.template_string: str = template_string
        self.available_keys: List[str] = available_keys

    def __str__(self):
        return "{recipe_path}Attempting to access unknown key {invalid_key} in template \'{entry_key}\': \'{template_string}\'. Available keys: {available_keys}".format(
            recipe_path="Error in recipe \"{}\": ".format('.'.join([str(rid) for rid in self.recipe_path])) if self.recipe_path else "",
            invalid_key=self.invalid_key,
            entry_key=self.entry_key,
            template_string=self.template_string,
            available_keys=self.available_keys
        )