from circuits_parser.system import System


class Prediction:
    """ Represents the predicted output that a system should emit with the given inputs.

    Attributes:
        self.system (System): the system that receives the inputs
        self.inputs (dict): dictionary of the inputs in the format of:  key: io id (e.g. 'i1')
                                                                        value: bool value
        self.outputs (dict): dictionary of the predicted outputs in the format of:  key: io id (e.g. 'o3')
                                                                                    value: bool value
    """
    def __init__(self, system, inputs):
        self.system: System = system
        self.inputs: dict[str, bool] = inputs
        self.outputs: dict[str, bool] = system.predict_output(inputs=self.inputs)
