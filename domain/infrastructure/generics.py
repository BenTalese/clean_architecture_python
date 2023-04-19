from typing import TypeVar

TAuthorisationFailure = TypeVar("TAuthorisationFailure")
#TAuthorisationFailure = TypeVar("TAuthorisationFailure", bound=IAuthorisationResult) # TODO: Investigate if IAuthorisationResult is worth doing
TEntity = TypeVar("TEntity")
TInputPort = TypeVar("TInputPort")
TInteractor = TypeVar("TInteractor")
TOutputPort = TypeVar("TOutputPort")
TServiceType = TypeVar("TServiceType")
TValidationFailure = TypeVar("TValidationFailure")
#TValidationFailure = TypeVar("TValidationFailure", bound=IValidationResult) # TODO: Investigate if IValidationResult is worth doing
