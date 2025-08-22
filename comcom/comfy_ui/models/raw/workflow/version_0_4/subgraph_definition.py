from copy import deepcopy
from typing import Self, Optional, List
from pydantic import BaseModel, Field, AliasPath

from .node import Comfy_V0_4_Node

from comcom.comfy_ui.models.normalized.workflow.subgraph_definition import NormalizedSubgraphDefinition
from comcom.comfy_ui.models.normalized.node_definition.node_definition import NormalizedNodeDefinition


from .output import Comfy_V0_4_Output
from .link_input import Comfy_V0_4_LinkInput

class Comfy_V0_4_SubgraphDefinition(BaseModel):
    id: str
    revision: int
    nodes: list[Comfy_V0_4_Node]
    version: float
    input_slots: list[Comfy_V0_4_Output] = Field(validation_alias=AliasPath('inputs'), default=[])
    output_slots: list[Comfy_V0_4_LinkInput] = Field(validation_alias=AliasPath('outputs'), default=[])
    subgraph_definitions: Optional[list[Self]] = Field(validation_alias=AliasPath('definitions', 'subgraphs'), default=[])

    def to_normalized(self, node_definitions: List[NormalizedNodeDefinition]) -> NormalizedSubgraphDefinition:
        return NormalizedSubgraphDefinition(
            id=self.id,
            revision=self.revision,
            nodes=[node.to_normalized(node_definitions) for node in self.nodes],
            version=self.version,
            incoming=[input_slot.to_normalized() for input_slot in self.input_slots],
            outgoing=[output_slot.to_normalized() for output_slot in self.output_slots],
            subgraph_definitions=[subgraph_definition.to_normalized(node_definitions) for subgraph_definition in self.subgraph_definitions]
        )
    
    def to_node_definition(self):
        return NormalizedSubgraphDefinition(
            id=self.id,
            revision=self.revision,
            nodes=[],
            version=self.version,
            incoming=[input_slot.to_normalized() for input_slot in self.input_slots],
            outgoing=[output_slot.to_normalized() for output_slot in self.output_slots],
            subgraph_definitions=[]
        ).to_node_definition()