
class AbstractSlotDefinition:
    @property
    def name() -> str:
        raise Exception("Not implemented")

    @property
    def type() -> str:
        raise Exception("Not implemented")
