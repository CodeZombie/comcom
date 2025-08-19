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
- AbstractIODefinition
    - NodeDefinition
    - SubgraphDefinition
- Node
- InputDefinition
- OutputDefinition
- Input
- Output

NOTE:
the `inputs` in Subgraph Definitions are not actually `inputs` - they describe a bit of data flowing out. And `outputs` are really inputs. They accept a piece of data flowing in. We should call them something else. Maybe `incoming_slots: Output = []` and `outgoing_slots: Input = []` ? Yeah I like that.