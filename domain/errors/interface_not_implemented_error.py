class InterfaceNotImplementedError(NotImplementedError):
    def __init__(self, module_name):
        super().__init__(f"{module_name} does not implement all interface members.")
        self.code = 5
