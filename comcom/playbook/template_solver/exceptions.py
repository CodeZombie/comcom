class LoopDetectedException(Exception): pass

class MaximumResolutionDepthException(Exception): pass

class InvalidKeyException(Exception):
    def __init__(self, entry_key: str, invalid_key: str, template_string: str):
        
        super().__init__("Attempting to access unknown key {invalid_key} in template \'{entry_key}\': \'{template_string}\'".format(
            invalid_key=invalid_key,
            entry_key=entry_key,
            template_string=template_string
        ))
        self.entry_key: str = entry_key
        self.invalid_key: str = invalid_key
        self.template_string: str = template_string