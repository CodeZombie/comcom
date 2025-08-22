from typing import List, Self
from dataclasses import dataclass
import copy

from .node import NormalizedNode
from .link_input import NormalizedLinkInput
from .output import NormalizedOutput

from comcom.comfy_ui.models.normalized.node_definition.node_definition import NormalizedNodeDefinition
from comcom.comfy_ui.models.normalized.node_definition.slot_definition import NormalizedSlotDefinition

from comcom.comfy_ui.models.normalized.utils.bypass import Bypass

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
    
    def to_node_definition(self) -> NormalizedNodeDefinition:
        return NormalizedNodeDefinition(
            name=self.id,
            display_name=self.id,
            output_node=False,
            input_slot_definitions=[NormalizedSlotDefinition(name=input.name, type=input.type, metadata={}) for input in self.incoming],
            output_slot_definitions=[NormalizedSlotDefinition(name=output.name, type=output.type, metadata={}) for output in self.outgoing],
            is_subgraph=True
        )
    
    # 
    def get_internal_bypasses(self, subgraph_instance: NormalizedNode) -> dict[str, str]:
        bypasses: List[Bypass] = []

        #bypass_map: dict[str, str] = {}
        for incoming_slot in self.incoming:
            for incoming_slot_link_id in incoming_slot.links:
                for input in subgraph_instance.inputs:
                    if input.name == incoming_slot.name:
                        if input.is_link:
                            bypasses.append(Bypass(
                                source_link_id=input.value,
                                input_link_id_that_needs_to_be_changed=incoming_slot_link_id
                            ))
                        else:
                            bypasses.append(Bypass(
                                source_link_id=None,
                                input_link_id_that_needs_to_be_changed=incoming_slot_link_id,
                                is_raw_value=True,
                                raw_value=input.value
                            ))
        return bypasses
    
    def get_external_bypasses(self, subgraph_instance: NormalizedNode) -> dict[str, str]:
        bypasses: List[Bypass] = []
        for outgoing_slot in self.outgoing:
            for output in subgraph_instance.outputs:
                if output.name == outgoing_slot.name:
                    for output_link in output.links:
                        bypasses.append(Bypass(
                            source_link_id=outgoing_slot.link,
                            input_link_id_that_needs_to_be_changed=output_link
                        ))
        return bypasses

    # <link_id>:<real external ultimate source link id>
    def as_normalized_node_list(self, subgraph_instance: NormalizedNode, node_definitions: List[NormalizedNodeDefinition], subgraph_definitions: List[Self], prefix: str = "") -> List[NormalizedNode]:
            prefix = "{}:{}".format(prefix, subgraph_instance.id) if prefix else subgraph_instance.id
            subgraph_definitions_as_node_definitions = [subgraph_definition.to_node_definition() for subgraph_definition in self.subgraph_definitions]
            
            expanded_nodes: List[NormalizedNode] = []
            # TODO: we CANNOT modify these values in-place because this SubgraphDefinition may be re-used for a different instance somewhere else :(
            for expanded_incoming_slot in self.incoming:
                expanded_incoming_slot.apply_prefix_to_links(prefix)
            for expanded_outgoing_slot in self.outgoing:
                expanded_outgoing_slot.apply_prefix_to_link(prefix)
                
            subgraph_definition_ids = [subgraph_definition.id for subgraph_definition in subgraph_definitions]
            for node in self.nodes:
                if node.type not in subgraph_definition_ids:
                    expanded_nodes.append(copy.deepcopy(node))

            # Apply prefix to all input and output link IDs in every node
            subgraph_instances: List[NormalizedNode] = [node for node in self.nodes if node.type in subgraph_definition_ids]
            for node in expanded_nodes:
                node.apply_prefix_to_links(prefix)

            for subgraph_instance_node in subgraph_instances:
                subgraph_definition = next(iter([subgraph_definition for subgraph_definition in subgraph_definitions if subgraph_definition.id == subgraph_instance_node.type]), None)
                expanded_nodes.extend(subgraph_definition.as_normalized_node_list(subgraph_instance_node, node_definitions + subgraph_definitions_as_node_definitions, subgraph_definitions, prefix=""))
                subgraph_ext_bypasses = subgraph_definition.get_external_bypasses(subgraph_instance_node)
                for node in expanded_nodes:
                    node.apply_bypasses(subgraph_ext_bypasses)


            # # Expand all subgraph instances within this subgraph definition
            # for subgraph_definition in self.subgraph_definitions:
            #     for node in subgraph_instances:
            #         if node.type == subgraph_definition.id:
            #             expanded_nodes.append(subgraph_definition.as_normalized_node_list(node, node_definitions, prefix))
            #             subgraph_output_bypass_map = subgraph_definition.get_output_bypass_map(node)
            #             for node in expanded_nodes:
            #                 node.apply_bypass_map(subgraph_output_bypass_map)

            internal_bypasses = self.get_internal_bypasses(subgraph_instance)
            for expanded_node in expanded_nodes:
                expanded_node.apply_bypasses(internal_bypasses)

            for node in expanded_nodes:
                node.id = "{}:{}".format(prefix, node.id)

            return expanded_nodes
        