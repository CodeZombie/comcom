from copy import deepcopy
from typing import Self, Optional, List
from pydantic import BaseModel, Field, AliasPath

from comcom.comfy_ui.definition.node_definitions import NodeDefinitions
from comcom.comfy_ui.definition.node_definition import NodeDefinition
from comcom.comfy_ui.definition.input_definitions import InputDefinitions
from comcom.comfy_ui.definition.input_definition import InputDefinition

from .slot import ComfySlot
from .node import ComfyNode

from .abstract_graph import AbstractGraph

class SubgraphDefinition(AbstractGraph):
    input_slots: list[ComfySlot] = Field(validation_alias=AliasPath('inputs'), default=[])
    output_slots: list[ComfySlot] = Field(validation_alias=AliasPath('outputs'), default=[])
    subgraphs: Optional[list[Self]] = Field(validation_alias=AliasPath('definitions', 'subgraphs'), default=[])

    def to_node_definition(self) -> NodeDefinition:
        input_definitions: List[InputDefinition] = []
        input_slot_dict = {'required': {}}
        for input_slot in self.input_slots:
            input_slot_dict['required'][input_slot.name] = [input_slot.type]
        return NodeDefinition.model_validate({
            'input': input_definitions,
            'output': [output_slot.type for output_slot in self.output_slots],
            'output_name': [output_slot.name for output_slot in self.output_slots],
            'name': self.id,
            'display_name': self.id,
            'output_node': False
        })

    def get_input_slot(self, name: str) -> ComfySlot:
        for inp in self.input_slots:
            if inp.name == name:
                return inp
        return None
    
    def get_output_slot(self, name: str) -> ComfySlot:
        for out in self.output_slots:
            if out.name == name:
                return out
        return None

    # TODO: I think we need to place the prefix before links as well.
    # I think we can probably do this with pydantic?
    # Modify the validator for subgraphs to automagically apply prefixes to all links and internal slots? That should do the trick.
    # Or we can just do that here.
    def get_expanded_nodes(self, subgraph_instance: ComfyNode, node_definitions: NodeDefinitions, prefix: str = "") -> List[ComfyNode]:
        prefix = "{}:{}".format(prefix, self.id) if prefix else self.id

        expanded_nodes: List[ComfyNode] = []
        
        # Expand child subgraphs
        for subgraph in self.subgraphs:
            expanded_nodes.extend(subgraph.get_expanded_nodes(self.id))

        # Expand all child subgraphs
        nodes_that_are_subgraph_instances: List[ComfyNode] = [node for node in expanded_nodes if node.type in [self.type].extend([subgraph.type for subgraph in self.subgraphs])]
        while len(nodes_that_are_subgraph_instances) > 0:
            subgraph_instance_node: ComfyNode = nodes_that_are_subgraph_instances[0]
            subgraph_def: SubgraphDefinition = [sgdef for sgdef in [self].extend(self.subgraphs) if sgdef.type == subgraph_instance_node.type]
            expanded_nodes.append(subgraph_def.get_expanded_nodes(subgraph_instance_node, subgraph_def, prefix))
            nodes_that_are_subgraph_instances.remove(node)
            expanded_nodes.remove(node)

        # Copy all of the subgraphs nodes into the expanded_nodes list.
        for node in self.nodes:
            expanded_nodes.append(deepcopy(node))
            
        # At this point, every node is created in `expanded_nodes`

        # RESOLVE INPUTS
        for instance_input in subgraph_instance.get_inputs(self.to_node_definition()).values():
            # If the source input
            if instance_input.is_link:
                input_slot: ComfySlot = self.get_input_slot(instance_input.name)
                interior_link_ids: str = input_slot.linkIds
                for interior_node in expanded_nodes:
                    for interior_node_input in interior_node.link_inputs:
                        if interior_node_input.link in interior_link_ids:
                            interior_node_input.link = instance_input.value
        
        # RESOLVE OUTPUTS
        for instance_output in subgraph_instance.get_outputs():
            output_slot: ComfySlot = self.get_output_slot(instance_output.name)
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
    