class AbstractIODefinition:
    @property
    def inputs(self):
        raise Exception("AbstractIODEfinition.inputs not implemented. Do not call this.")
    
    @property
    def outputs(self):
        raise Exception("AbstractIODEfinition.outputs not implemented. Do not call this.")