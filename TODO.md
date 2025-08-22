## General TODO
Refactor the project so that there is a `Comfy_0_4_*` module which is JUST pydantic models for workflow v0.4.
We can do a little tiny bit of processing here, but don't do too much.

THEN, we transform that data into a general `Comfy*` which is much more tightly compacted.


In this format, NodeDefinition and SubgraphDefinition will both be passable to  `node.get_inputs(node_or_subgraph_definition)` so that we can treat Subgraph instances like real nodes without doing any horrible hack bullshit.

Also, all named children should be stored as dictionaries. No more mixing dicts and lists because the format decided it so.

All the resolution logic will be in the `Comfy*` classes.
This way when we want to support Workflow 1.0, we only need to write a new set of Pydantic model classes and some new functions to transform them into `Comfy*` formats. Much cleaner. This way the business logic never needs to change.

So let's spend a bit of time deciding what formats should look like and which abstract classes should exist.

- Workflow
- Node
    - SubgraphNode
- Input
- Output
- AbstractIODefinition
    - NodeDefinition
    - SubgraphDefinition
- InputDefinition [name, type, index]
- OutputDefinition [name, type, index]

/comcom
    /comfy_workflow
        /raw
            /version_0_4
                /models
                    workflow.py [Comfy_v0_4_Workflow] (Will have a `to_normalized_comfy_workflow()` function)
                    node.py     [Comfy_v0_4_Node]
                    ...

            /version_1_0
                ...

        /normalized         (responsible for resolving links, expanding subgraphs, etc. The code in here can be messy and redundant, as its whole job is to output a `ComfyWorkflow`)
            workflow.py     [NormalizedComfyWorkflow] (will have a `to_comfy_workflow()` method, which returns a  common.ComfyWorkflow)

        /common             (A clean, user-friendly representation of a comfy workflow. Ready to have its properties modified or be converted into an ApiPrompt)
            workflow.py     [ComfyWorkflow]
            ...

        converter.py        [Contains the entrypoint code for conversion. ]


NOTE:
the `inputs` in Subgraph Definitions are not actually `inputs` - they describe a bit of data flowing out. And `outputs` are really inputs. They accept a piece of data flowing in. We should call them something else. Maybe `incoming_slots: Output = []` and `outgoing_slots: Input = []` ? Yeah I like that.

/comcom
    /comfy_ui
        /graph
            /abstract
                /workflow
                /definitions
            /workflow_v0_4
            /workflow_v1_0+
            /definitions_v1_0
            /definitions_v2_0
        /api
            workflow.py
            