from typing import List, Tuple, Type


"""

PIPE_PRIORITY: List[Tuple[Type[IPipe], int]] = [
    (IInputPortValidator, 1),
    (IBusinessRuleValidator, 2)
]


#Using:
from typing import Type

def create_pipeline(use_case: str) -> Pipeline:
    # Get the list of pipes for the use case
    pipes = get_pipes_for_use_case(use_case)

    # Sort the pipes according to the pipeline order
    sorted_pipes = sorted(pipes, key=lambda pipe: next(order[1] for order in PIPELINE_ORDER if isinstance(pipe, order[0])))

    # Create the pipeline
    pipeline = Pipeline()
    for pipe in sorted_pipes:
        pipeline.add_pipe(pipe)

    return pipeline



"""