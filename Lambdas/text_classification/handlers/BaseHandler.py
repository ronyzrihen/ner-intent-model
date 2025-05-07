class BaseHandler:
    def __init__(self, event, model_output):
        self.event = event
        self.model_output = model_output

    def handle(self):
        raise NotImplementedError("handle is not implemented")
