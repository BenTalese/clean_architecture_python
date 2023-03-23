import os
import importlib
from typing import List, Type
from Application.Infrastructure.Pipes.IPipe import IPipe


#Get all pipes from pipes folder
def load_pipes() -> List[Type[IPipe]]:
    pipes = []
    for filename in os.listdir("pipes"):
        if filename.endswith(".py"):
            module_name = filename[:-3]
            module = importlib.import_module(f"pipes.{module_name}")
            for name in dir(module):
                obj = getattr(module, name)
                if isinstance(obj, type) and issubclass(obj, IPipe) and obj != IPipe:
                    pipes.append(obj)
    return pipes




from typing import List, Type
from Application.Infrastructure.Pipes.IPipe import IPipe


# Attempt 1
class PipelineOrderVerifier:
    @staticmethod
    def verify_order(pipes: List[Type[IPipe]], pipe_priority: List[Type[IPipe]]):
        """
        Verifies that the order of pipes matches the order in PIPE_PRIORITY
        :param pipes: List of pipe types
        :param pipe_priority: List of pipe types in the correct order
        :raises ValueError: If the order of pipes does not match the order in PIPE_PRIORITY
        """
        # Create a dictionary to hold the priority of each pipe type
        priority_dict = {pipe_type: i for i, pipe_type in enumerate(pipe_priority)}
        # Iterate over the list of pipes and compare their priority to the priority in PIPE_PRIORITY
        last_priority = -1
        for pipe in pipes:
            priority = priority_dict.get(pipe)
            if priority is None:
                raise ValueError(f"Pipe {pipe.__name__} is not in PIPE_PRIORITY")
            if priority < last_priority:
                raise ValueError(f"Pipes are out of order: {pipe.__name__} should not come before {last_pipe.__name__}")
            last_priority = priority
            last_pipe = pipe


# Attempt 2
class PipelineVerificationService:
    @staticmethod
    def verify(pipes: List[Type[IPipe]], pipe_priority: List[Type[IPipe]]):
        # Get the priority numbers of the pipes
        pipe_priorities = [p.Priority for p in pipes]
        
        # Get the priority numbers from PIPE_PRIORITY
        priority_order = {p.__name__: i for i, p in enumerate(pipe_priority, start=1)}
        
        # Verify that the priority order matches
        for i, priority in enumerate(pipe_priorities[:-1]):
            if priority_order[pipes[i].__name__] > priority_order[pipes[i+1].__name__]:
                raise Exception(f"Invalid priority order: {pipes[i]} has priority {priority}, but should be after {pipes[i+1]}")



# Attempt 3
class PipePriorityVerifier:
    @staticmethod
    def verify(pipe_types: List[Type[IPipe]], pipe_priority: List[Type[IPipe]]):
        pipe_priority_set = set(pipe_priority)
        if len(pipe_priority_set) != len(pipe_priority):
            raise ValueError("Duplicate pipe types found in PIPE_PRIORITY")
        for i, pipe_type in enumerate(pipe_priority):
            if pipe_type not in pipe_types:
                raise ValueError(f"{pipe_type.__name__} not found in available pipes")
            pipe_priority_index = pipe_priority.index(pipe_type)
            if i != pipe_priority_index:
                raise ValueError(f"{pipe_type.__name__} has a priority of {pipe_type.Priority}, but is not in the correct position in PIPE_PRIORITY")

"""
PIPE_PRIORITY: List[Type[IPipe]] = [
    IInputPortValidator,
    IBusinessRuleValidator,
    IInteractor
]

PipePriorityVerifier.verify(available_pipes, PIPE_PRIORITY)
"""
