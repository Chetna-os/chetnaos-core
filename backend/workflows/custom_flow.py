class CustomWorkflow:
    def _init_(self, name="custom"):
        self.name = name
        self.steps = []

    def add_step(self, step_callable):
        self.steps.append(step_callable)

    def run(self, context: dict):
        result = context
        for step in self.steps:
            result = step(result)
        return result
