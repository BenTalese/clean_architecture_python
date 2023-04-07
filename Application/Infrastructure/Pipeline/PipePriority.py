class PipePriorityMeta(type):
    def __setattr__(cls, key, value):
        if any(getattr(cls, k) == value for k in cls.__dict__ if k != key):
            raise ValueError(f"Cannot assign pipe priority '{value}' to '{key}'. Priority '{value}' is in use by another pipe.")
        super().__setattr__(key, value)

class PipePriority(metaclass=PipePriorityMeta):
    pass
