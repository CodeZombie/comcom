from typing import List, Self
from dataclasses import dataclass
import copy

from .node import NormalizedNode
from .link_input import NormalizedLinkInput
from .output import NormalizedOutput

from comcom.comfy_ui.models.normalized.node_definition.node_definition import NormalizedNodeDefinition

@dataclass
class NormalizedSubgraphDefinition:
    id: str
    revision: int
    nodes: list[NormalizedNode]
    version: float
    incoming: List[NormalizedOutput]
    outgoing: List[NormalizedLinkInput]
    subgraph_definitions: List[Self]

    def get_incoming(self, name: str) -> NormalizedOutput:
        return next((incoming for incoming in self.incoming if incoming.name == name), None)

    def get_outgoing(self, name: str) -> NormalizedLinkInput:
        return next((outgoing for outgoing in self.outgoing if outgoing.name == name), None)
    
    def as_normalized_node_list(self, subgraph_instance: NormalizedNode, node_definitions: List[NormalizedNodeDefinition], prefix: str = "") -> List[NormalizedNode]:
            prefix = "{}:{}".format(prefix, self.id) if prefix else self.id

            expanded_nodes: List[NormalizedNode] = []
            
            # Expand all subgraph instances within this subgraph definition
            nodes_that_are_subgraph_instances: List[NormalizedNode] = [node for node in self.nodes if node.type in [subgraph_definition.id for subgraph_definition in self.subgraph_definitions]]
            for subgraph_definition in self.subgraph_definitions:
                for node in nodes_that_are_subgraph_instances:
                    if node.type == subgraph_definition.id:
                        expanded_nodes.append(subgraph_definition.as_normalized_node_list(node, node_definitions, prefix))

            # Add all non-subgraph-instance nodes to the expanded_nodes list.
            for node in self.nodes:
                if node.type not in [subgraph_definition.id for subgraph_definition in self.subgraph_definitions]:
                    expanded_nodes.append(copy.deepcopy(node))

            # At this point, every node is created in `expanded_nodes`

            # RESOLVE INPUTS
            for instance_input in subgraph_instance.get_inputs(self.to_node_definition()).values():
                # If the source input
                if instance_input.is_link:
                    input_slot: NormalizedOutput = self.get_incoming(instance_input.name)
                    interior_link_ids: str = input_slot.links
                    for interior_node in expanded_nodes:
                        for interior_node_input in interior_node.link_inputs:
                            if interior_node_input.link in interior_link_ids:
                                interior_node_input.link = instance_input.value
            
            # RESOLVE OUTPUTS
            for instance_output in subgraph_instance.outputs:
                output_slot: NormalizedLinkInput = self.get_outgoing(instance_output.name)
                output_slot_source_link_ids = output_slot.links
                for interior_node in expanded_nodes:
                    for interior_node_output in interior_node.outputs:
                        new_links = interior_node_output.links.copy()
                        for interior_link in interior_node_output.links:
                            if interior_link in output_slot_source_link_ids:
                                new_links.remove(interior_link)
                                new_links.extend(output_slot_source_link_ids)
                        interior_node_output.links = list(set(new_links))

            for node in expanded_nodes:
                node.id = "{}:{}".format(prefix, node.id)

            return expanded_nodes
        