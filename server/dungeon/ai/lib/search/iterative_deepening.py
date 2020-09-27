from .common import NoSolutionError
from .depth_limited import (depth_limited_graph, depth_limited_tree,
                            depth_limited_tree_check_path)


def iterative_deepening_graph(problem):
    depth_limit = 1
    while True:
        try:
            return depth_limited_graph(problem, depth_limit)
        except NoSolutionError as e:
            if not e.depth_limited:
                raise NoSolutionError(iteration_limit=e.iteration_limit)
            depth_limit += 1


def iterative_deepening_tree(problem):
    depth_limit = 1
    while True:
        try:
            return depth_limited_tree(problem, depth_limit)
        except NoSolutionError as e:
            if not e.depth_limited:
                raise NoSolutionError(iteration_limit=e.iteration_limit)
            depth_limit += 1


def iterative_deepening_tree_check_path(problem):
    depth_limit = 1
    while True:
        try:
            return depth_limited_tree_check_path(problem, depth_limit)
        except NoSolutionError as e:
            if not e.depth_limited:
                raise NoSolutionError(iteration_limit=e.iteration_limit)
            depth_limit += 1
