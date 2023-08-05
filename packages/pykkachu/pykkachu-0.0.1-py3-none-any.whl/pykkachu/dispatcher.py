class Dispatcher:
    funcs = {}

    def add(self, func, event_type=None, event_name=None, state=None):
        if (event_type, event_name, state) in self.funcs:
            raise Exception("Can't have two event processors with the same trigger")

        self.funcs[(event_type, event_name, state)] = func

    def get(self, event_type=None, event_name=None, state=None):
        if (event_type, event_name, state) in self.funcs:
            return self.funcs[(event_type, event_name, state)]
        elif (event_type, event_name, None) in self.funcs:
            return self.funcs[(event_type, event_name, None)]
        elif (event_type, None, state) in self.funcs:
            return self.funcs[(event_type, None, state)]
        elif (None, event_name, state) in self.funcs:
            return self.funcs[(None, event_name, state)]
        elif (event_type, None, None) in self.funcs:
            return self.funcs[(event_type, None, None)]
        elif (None, event_name, None) in self.funcs:
            return self.funcs[(None, event_name, None)]
        elif (None, None, state) in self.funcs:
            return self.funcs[(None, None, state)]
        elif (None, None, None) in self.funcs:
            return self.funcs[(None, None, None)]
        else:
            raise Exception("No function to dispatch to")
