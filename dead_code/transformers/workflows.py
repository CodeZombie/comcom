
from dataclasses import dataclass
from typing import Union
from typing_extensions import Self
import copy

def to_str_or_none(value: Union[str, None]) -> Union[str, None]:
    if value == None:
        return None
    return str(value)

def list_get(l, i, default=None):
    if i < len(l):
        return l[i]
    return default


@dataclass
class NodeDefinition:
    # TODO: Let's refactor this so that NodeDefinition holds a list of SlotDefinition objects.
    # SlotDefinitions will contain an id and a type.

    id: str
    input_names: list[str]
    output_names: list[str]
    input_types: list[str]


    def get_input_type(self, input_name: str) -> str:
        for i in range(len(self.input_names)):
            if self.input_names[i] == input_name:
                return self.input_types[i]
        raise Exception("Cannot get input type for input {}. Input not found.".format(input_name))

    def get_input_map_from_node_definition_dict(self, node_definition_dict: dict) -> dict:
        
        # Create a temporary list of all input names.
        # as we go through the existing input entries in the node, remove any input_names that dont have a 'widget' attribute.
        # This should leave us with a perfect map of temp_name -> widget_values
        input_names_with_widgets = self.input_names.copy()
        input_map: dict = dict()
        for input_def in node_definition_dict.get('inputs', []):
            input_name = input_def.get('name')
            input_map[input_name] = Link(input_def.get('link'), None, None)
            widget_name = input_def.get('widget', {}).get('name', None)
            if not widget_name:
                input_names_with_widgets.remove(input_name)
        
        # At this stage, `input_names_with_widgets` should perfectly map to the node_def's `widget_values`. 
        # We can literally zip them together and then merge with the existing input_map
        input_map = dict(zip(input_names_with_widgets, node_definition_dict.get('widgets_values', {}))) | input_map
        
        return input_map

    @classmethod
    def from_dict(cls, id, node_def_dict: dict) -> Self:
        fake_input_iterator = 0
        input_names: list[str] = []
        inputs_dict = node_def_dict.get('input', {}).get('required', {}) | node_def_dict.get('input', {}).get('optional', {})
        for input_name in inputs_dict:
            input_names.append(input_name)
            if input_name in inputs_dict.keys():
                if len(inputs_dict[input_name]) > 1 and inputs_dict[input_name][0] == 'INT':
                    if inputs_dict[input_name][1].get('control_after_generate'):
                        if fake_input_iterator > 0:
                            input_names.append('control_after_generate_{}'.format(fake_input_iterator))
                        else:
                            input_names.append('control_after_generate')
                        fake_input_iterator += 1

        output_names = node_def_dict.get('output_name', []).copy()

        input_types = []
        for input_name in input_names:
            if input_name == 'control_after_generate':
                input_types.append("STRING")
            else:
                input_types.append(inputs_dict[input_name][0])

        return cls(
            id,
            input_names,
            output_names,
            input_types
        )

    @classmethod
    def from_dicts(cls, node_def_dics: dict) -> dict[str, Self]:
        node_defs: dict[str, NodeDefinition] = dict()
        for key in node_def_dics.keys():
            node_defs[key] = cls.from_dict(key, node_def_dics[key])
        return node_defs

@dataclass
class NodeDefinitions:
    node_definitions: dict[str, NodeDefinition]

    @classmethod
    def from_dict(cls, node_definitions_dict: dict) -> Self:
        node_definitions: dict[str, NodeDefinition]
        for node_definition_name in node_definitions_dict.key():
            node_definitions[node_definition_name] = NodeDefinition.from_dict(node_definition_name, node_definitions_dict[node_definition_name])

        # Insert a Reroute definition.
        node_definitions['Reroute'] = NodeDefinition(
            id="Reroute",
            input_names=[""],
            output_names=[""],
            input_types=["*"]
        )

        return cls(
            node_definitions=node_definitions
        )



@dataclass
class Link:
    id: Union[int, str]
    source_node_id: str
    source_output_id: int

    @property
    def is_resolved(self):
        return self.source_node_id != None and self.source_output_id != None
    
    def __str__(self):
        return "<Link id:{} source_node:{} source_input:{}>".format(self.id, self.source_node_id, self.source_output_id)


@dataclass
class Input:
    id: str
    type: str
    value: Union[int, float, str, bool, Link]

    def __str__(self):
        return "<Input id:{} value:{}>".format(self.id, self.value)

    def change_link_id(self, f, t):
        if isinstance(self.value, Link):
            if self.value.id == f:
                self.value.id = t

@dataclass
class Output:
    name: str
    type: str
    link_ids: list[Union[int, str]]

    def __str__(self):
        return "<Output name:{} type:{} link_ids:{}>".format(self.name, self.type, self.link_ids)

    @classmethod
    def from_output_json_dict(cls, output_json_dict: dict):
        return Output(
            name=output_json_dict.get('name', None),
            type=output_json_dict.get('type', None),
            link_ids=(output_json_dict.get('links') or []).copy(),
        )
    
    def change_link_id(self, f, t):
        for i in range(len(self.link_ids)):
            if self.link_ids[i] == f:
                self.link_ids[i] = t

@dataclass
class Node:
    id: str
    class_type: str
    inputs: list[Input]
    outputs: list[Output]
    muted: bool = False

    def __str__(self):
        s = "<Node id:{} class_type:{}>".format(self.id, self.class_type)
        for input in self.inputs:
            s += "\n      {}".format(str(input))
        for output in self.outputs:
            s += "\n      {}".format(str(output))
        return s
    
    def get_input(self, input_id):
        for input in self.inputs:
            if input.id == input_id:
                return input
        return None
    
    # returns a dict that maps Output Links to their ultimate destination, effectively bypassing this node entirely.
    # The output map is structured as `{<source_link_id> : [destination_link_id, ...]}`
    # to use this dict, just find all sources for `source_link_id` and add `destination_link_ids` to that list.
    def get_bypass_map(self):
        class Found(Exception): pass
        bypass_map: dict[Union[str, int], Union[str, int]] = {}
        inputs_copy: list[Input] = copy.deepcopy(self.inputs)

        for output in self.outputs:
            for inp in inputs_copy:
                try:
                    if inp.type == output.type:
                        for link_id in output.link_ids:
                            source_link_id = inp.value.id if isinstance(inp.value, Link) else None
                            if source_link_id != None:
                                if source_link_id not in bypass_map.keys():
                                    bypass_map[source_link_id] = []
                                bypass_map[source_link_id].append(link_id)
                        inputs_copy.remove(inp)
                        raise Found
                except Found:
                    break

        return bypass_map

    @classmethod
    def from_node_json_dict(cls, node_dict: dict, node_definitions_dict: dict):
        node_defs = NodeDefinition.from_dicts(node_definitions_dict)
        
        inputs = []
        node_type = node_dict['type']
        node_def = node_defs.get(node_type)
        input_map = node_defs.get(node_type).get_input_map_from_node_definition_dict(node_dict)
        for input_name in node_defs.get(node_type).input_names:
            inputs.append(Input(
                id=input_name,
                type=node_def.get_input_type(input_name),
                value=input_map[input_name]
            ))

        return Node(
            id=node_dict.get('id'),
            class_type=node_dict.get('type', None),
            inputs=inputs,
            outputs=[Output.from_output_json_dict(o) for o in node_dict.get('outputs', [])],
            muted=node_dict.get('mode', 0) == 4
        )

    def get_input(self, input_id: str):
        for input in self.inputs:
            if input.id == input_id:
                return input
        
    def to_api_prompt(self):
        api_prompt_dict = {}
        api_prompt_dict['class_type'] = self.class_type
        api_prompt_dict['inputs'] = {}
        for input in self.inputs:
            api_prompt_dict['inputs'][input.id] = [input.value.source_node_id, input.value.source_output_id] if isinstance(input.value, Link) else input.value
        return api_prompt_dict
    
    def change_link_id(self, f, t):
        for io in self.inputs + self.outputs:
            io.change_link_id(f, t)


@dataclass
class SlotDefinition:
    id: str
    name: str
    type: str
    linkIds: list[int]

# TODO: Workflow should probably inherit from NodeDefinition
@dataclass
class Workflow:
    id: str
    revision: int
    version: float
    frontendVersion: str
    nodes: list[Node]
    subgraphs: list[Self]
    inputs: list[SlotDefinition] # Remove this and replace with list[Input]
    outputs: list[SlotDefinition] # Remove this and replace with list[Output]
    # subgraph_input_node: Node
    # subgraph_output_node: Node


    def get_node_by_id(self, node_id: str):
        for node in self.nodes:
            if str(node.id) == node_id:
                return node
        return None

    def __str__(self):
        s = self.id
        for node in self.nodes:
            s += "\n  {}".format(str(node))
        return s
    
    # TODO: all links should be stored as strings.
    def rename_link(self, link_id: str):
        pass

    def convert_to_subgraph_nodes(self, subgraph_instance: Node) -> list[Node]:
        wf_copy = copy.deepcopy(self)
        # Assign the link values for:
        #   1. subgraph_input_node.inputs
        #   2. subgraph_output_node.outputs
        # based on the values from subgraph_instance

        # prepend all node names with <subgraph_instance.id>:id
        # prepend 'id:' to:
        #   1. every subgraph_input_node.outputs link
        #   2. every subgraph_output_node.inputs link
        #   3. every node in/out link
        # bypass the special input and output nodes to force them to connect externally.


        pass

    # Must be called after you rename nodes
    def resolve_links(self):

        for source_node in self.nodes:
            for output_index, output in enumerate(source_node.outputs):
                for destination_node in self.nodes:
                    for link_input in [inp for inp in destination_node.inputs if isinstance(inp.value, Link)]:
                        if link_input.value.id in output.link_ids:
                            link_input.value.source_node_id = str(source_node.id)
                            link_input.value.source_output_id = output_index

    @classmethod
    def from_workflow_json_dict(cls, workflow_dict: dict, node_definitions_dict: dict) -> Self:
        workflow_json_version = workflow_dict.get('version', None)
        if workflow_json_version in [None, 0.4]:
            return cls.from_workflow_json_0_4_dict(workflow_dict, node_definitions_dict)
        raise Exception("Unsupported ComfyUI Workflow JSON version: {}".format(workflow_json_version))
    
    def get_output_by_link_id(self, link_id):
        for node in self.nodes:
            for output in node.outputs:
                if link_id in output.link_ids:
                    return output
        return None

    def get_muted_nodes(self):
        return [node for node in self.nodes if node.muted]
    
    def get_reroute_nodes(self):
        return [node for node in self.nodes if node.class_type == 'Reroute']

    @classmethod
    def from_workflow_json_0_4_dict(cls, workflow_dict: dict, node_definitions_dict: dict) -> Self:
        new_workflow = cls(
            id=workflow_dict.get('id', None),
            revision=workflow_dict.get('revision', None),
            frontendVersion=workflow_dict.get('frontendVersion', None),
            version=workflow_dict.get('version', None),
            nodes=[],
            subgraphs=[],
            inputs=[],
            outputs=[],
        )

        # Subgraph nightmare code
        for subgraph_dict in workflow_dict.get('definitions', {}).get('subgraphs', []):
            new_workflow.subgraphs.append(cls.from_workflow_json_0_4_dict(subgraph_dict, node_definitions_dict))

        for input_dict in workflow_dict.get('inputs', []):
            new_workflow.inputs.append(
                SlotDefinition(
                    input_dict.get('id', None),
                    input_dict.get('name', None),
                    input_dict.get('type', None),
                    input_dict.get('linkIds', []),
                ))

        for output_dict in workflow_dict.get('outputs', []):
            new_workflow.outputs.append(
                SlotDefinition(
                    output_dict.get('id', None),
                    output_dict.get('name', None),
                    output_dict.get('type', None),
                    output_dict.get('linkIds', []),
                ))

        subgraph_node_definitions_dict = {}
        for subgraph in new_workflow.subgraphs:
            subgraph_node_definitions_dict[subgraph.id] = subgraph.get_subgraph_node_definition_dict()

        for node_dict in workflow_dict.get('nodes', []):
            new_node = Node.from_node_json_dict(node_dict, {**node_definitions_dict, **subgraph_node_definitions_dict})
            new_workflow.nodes.append(new_node)

        # Bypass routes for, and remove all muted nodes
        while len(new_workflow.get_muted_nodes() + new_workflow.get_reroute_nodes()) > 0:
            node_to_bypass = (new_workflow.get_muted_nodes() + new_workflow.get_reroute_nodes())[0]
            bypass_map = node_to_bypass.get_bypass_map()
            for source_link_id in bypass_map.keys():
                output = new_workflow.get_output_by_link_id(source_link_id)
                if output:
                    output.link_ids.extend(bypass_map[source_link_id])
            
            new_workflow.nodes.remove(node_to_bypass)


        # Expand all Subgraph instances.
        nodes_to_delete = []
        for subgraph in new_workflow.subgraphs:
            for subgraph_instance in new_workflow.get_nodes_by_type(subgraph.id):
                nodes_to_delete.append(subgraph_instance)
                new_workflow.nodes.extend(subgraph.get_nodes_as_expanded_subgraph(subgraph_instance))
            
            # Now finda all the input and output links for this subgraph
            # and for each 

        for node in nodes_to_delete:
            new_workflow.nodes.remove(node)

        new_workflow.resolve_links()

        return new_workflow
    
    def collapse_external_links(self):
        """
        # TODO: DO THIS and use it when instantiating subgraphs.
        Create a map of external link to internal link.
        Then find all nodes that have that internal link and replace it with the external link
        This should probably be called in `get_subgraph_node_definition_dict` or at least be a subfunction of that one.

        """
        pass

    def to_api_prompt(self):
        api_prompt_dict = {}
        for node in self.nodes:
            api_prompt_dict[str(node.id)] = node.to_api_prompt()
        return api_prompt_dict
    
    def get_nodes_by_type(self, class_type: str) -> list[Node]:
        output_nodes: list[Node] = []
        for node in self.nodes:
            if node.class_type == class_type:
                output_nodes.append(node)
        return output_nodes
    
    def get_subgraph_node_definition_dict(self):
        """
        Returns a node definition dictionary describing this workflow as a Subgraph.
        """

        node_definition_dict = {
            "input": {
                "required": {}
            },
            "input_order": {
                "required": []
            },
            "output": []
            }
        
        for input_slot in self.inputs:
            node_definition_dict['input']['required'][input_slot.name] = [
                input_slot.type,
                {}
            ]

            node_definition_dict['input_order']['required'].append(
                input_slot.name
            )
        
        for output_slot in self.outputs:
            node_definition_dict['output'].append(
                output_slot.type
            )

        return node_definition_dict
    
    def get_input_link_ids(self):
        link_ids = []
        for input in self.inputs:
            link_ids.extend(input.linkIds)
        return link_ids
    
    def get_output_link_ids(self):
        link_ids=[]
        for output in self.outputs:
            link_ids.extend(output.linkIds)
        return link_ids
    

    def get_nodes_as_expanded_subgraph(self, subgraph_instance: Node):
        # For each Node in this subgraph
        # Create a copy of each node, but append `subgraph_instance.id:` to the front of each of their IDs.

        expanded_nodes = []
        for node in self.nodes:
            node_copy = copy.deepcopy(node)
            node_copy.id = "{subgraph_id}:{original_node_id}".format(subgraph_id=subgraph_instance.id, original_node_id=node.id)
            for input in node_copy.inputs:
                if isinstance(input.value, Link):
                    if input.value.id:
                        if input.value.id not in self.get_input_link_ids():
                            input.value.id = "{subgraph_id}:{original_link_id}".format(subgraph_id=subgraph_instance.id, original_link_id=input.value.id)
            for output in node_copy.outputs:
                new_output_link_ids = []
                for output_link_id in output.link_ids:
                    if output_link_id not in self.get_output_link_ids():
                        new_output_link_ids.append("{subgraph_id}:{original_link_id}".format(subgraph_id=subgraph_instance.id, original_link_id=output_link_id))
                    else:
                        new_output_link_ids.append(output_link_id)
            expanded_nodes.append(node_copy)

        return expanded_nodes

        expanded_nodes: list[Node] = []
        for node in self.nodes:
            new_node: Node = copy.deepcopy(node)
            new_node.id = "{subgraph_id}:{original_node_id}".format(subgraph_id=subgraph_instance.id, original_node_id=node.id)
            for input in new_node.inputs:
                if isinstance(input.value, Link):
                    if input.value.id in input_link_map.keys():
                        input.value.id = input_link_map[input.value.id]
                    else:
                        if input.value.id != None:
                            from_id = input.value.id
                            to_id = "{instance_id}:{original_id}".format(instance_id=subgraph_instance.id, original_id=input.value.id)
                            print("Changing input value id from {} to {}".format(from_id, to_id))
                            input.value.id = "{instance_id}:{original_id}".format(instance_id=subgraph_instance.id, original_id=input.value.id)

            expanded_nodes.append(new_node)
        

        # for i in range(len(self.outputs)):
        #     external_output_link_ids = subgraph_instance.outputs[i].link_ids
        #     for internal_link_id in self.outputs[i].linkIds:
        #         for node in expanded_nodes:
        #             print("Changing {} to {}".format(internal_link_id, external_output_link_ids))
        #             for external_output_link_id in external_output_link_ids:
        #                 node.change_link_id(internal_link_id, external_output_link_id)

        # Now go through all the outputs in the instance.
        # for each output, find which link it was connected to and then go through all these internal nodes and replace those links.
        for i in range(len(subgraph_instance.outputs)):
            instance_output = subgraph_instance.outputs[i]
            print("{} -> {}".format(self.outputs[i], instance_output))
            # Find all links with self.outputs[i].linkIds
                #replace it with instance_output.link_ids
            for node in expanded_nodes:
                for node_output in node.outputs:
                    for internal_link_id in node_output.link_ids:
                        if internal_link_id in self.outputs[i].linkIds:
                            node_output.link_ids = instance_output.link_ids
                       



        return expanded_nodes