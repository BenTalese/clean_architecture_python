from enum import Enum

class PipePriority(Enum):
    EntityExistenceChecker = 1
    InputPortValidator = 2
    AuthorisationEnforcer = 3
    BusinessRuleValidator = 4
    Interactor = 5
