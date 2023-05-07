from circuits_parser.system import System


class Prediction:
    def __init__(self, system, inputs):
        self.system: System = system
        self.inputs: dict[str, bool] = inputs
        self.outputs: dict[str, bool] = system.predict_output(inputs=self.inputs)
