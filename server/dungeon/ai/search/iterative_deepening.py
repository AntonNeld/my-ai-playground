from .common import NoSolutionError
from .depth_first import (depth_first_graph, depth_first_tree,
                          depth_first_tree_check_path)


def iterative_deepening_graph(problem, iteration_limit=10000):
    depth_limit = 1
    while True:
        try:
            return depth_first_graph(problem, depth_limit=depth_limit,
                                     iteration_limit=iteration_limit)
        except NoSolutionError as e:
            if not e.depth_limited:
                raise NoSolutionError(iteration_limit=e.iteration_limit)
            depth_limit += 1


def iterative_deepening_tree(problem, iteration_limit=10000):
    depth_limit = 1
    while True:
        try:
            return depth_first_tree(problem, depth_limit=depth_limit,
                                    iteration_limit=iteration_limit)
        except NoSolutionError as e:
            if not e.depth_limited:
                raise NoSolutionError(iteration_limit=e.iteration_limit)
            depth_limit += 1


def iterative_deepening_tree_check_path(problem, iteration_limit=10000):
    depth_limit = 1
    while True:
        try:
            return depth_first_tree_check_path(
                problem,
                depth_limit=depth_limit,
                iteration_limit=iteration_limit
            )
        except NoSolutionError as e:
            if not e.depth_limited:
                raise NoSolutionError(iteration_limit=e.iteration_limit)
            depth_limit += 1
