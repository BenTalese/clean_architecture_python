class PipePriority:
    __initialized = False

    def __init__(self, **kwargs):
        if not self.__initialized:
            for key, value in self.__GetDefaultValues().items():
                setattr(self, key, value)
            for key, value in kwargs.items():
                setattr(self, key, value)
        self.__initialized = True

    def __GetDefaultValues(self):
        return {
            'IAuthenticationVerifier': 1,
            'IEntityExistenceChecker': 2,
            'IAuthorisationEnforcer': 3,
            'IBusinessRuleValidator': 4,
            'IInputPortValidator': 5,
            'IInteractor': 6,
        }
    """
            f'{IAuthenticationVerifier.__name__}': 1,
            f'{IEntityExistenceChecker.__name__}': 2,
            f'{IAuthorisationEnforcer.__name__}': 3,
            f'{IBusinessRuleValidator.__name__}': 4,
            f'{IInputPortValidator.__name__}': 5,
            f'{IInteractor.__name__}': 6,
    """

    def __setattr__(self, key, value):
        if self.__initialized and key not in self.__dict__: # TODO: Decide whether or not to let the user add new pipes whenever
            raise TypeError("Cannot add new values to an initialized CustomEnum")
        if key is not '_CustomEnum__initialized' and any(getattr(self, k) == value for k in self.__dict__):
            raise ValueError(f"Cannot assign pipe priority '{value}' to '{key}'. Priority '{value}' is in use by another pipe.")
        super().__setattr__(key, value)


"""
Example usage:

pp = PipePriorty(IExamplePipe=3) # add own pipes via constructor

print(pp.IAuthenticationVerifier) # get default value 1
print(pp.IEntityExistenceChecker) # get default value 2
pp.IExamplePipe = 4 # cannot change existing value

pp.FOO = 8
print(pp.FOO)
pp.BAA = 5
"""
