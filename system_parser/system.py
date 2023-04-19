from dataclasses import dataclass

from system_parser.components import Component


@dataclass
class Input:
    id: int
    value: bool


@dataclass
class Output(Input):
    pass


@dataclass
class Gate:
    logical_type: Component
    id: int
    output: Output
    inputs: list[Input]


@dataclass
class System:
    id: int
    inputs: list[Input]
    outputs: list[Output]
    gates: list[Gate]
