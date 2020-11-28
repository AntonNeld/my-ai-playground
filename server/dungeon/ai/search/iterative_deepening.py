from .common import NoSolutionError
from .depth_first import (depth_first_graph, depth_first_tree,
                          depth_first_tree_check_path,
                          depth_first_recursive)


def iterative_deepening_graph(problem, iteration_limit=10000):
    depth_limit = 1
    iterations = 0
    while True:
        try:
            return depth_first_graph(
                problem, depth_limit=depth_limit,
                iteration_limit=iteration_limit - iterations
            )
        except NoSolutionError as e:
            iterations += e.iterations
            if not e.depth_limited:
                raise NoSolutionError(
                    iterations=iterations,
                    iteration_limited=e.iteration_limited
                )
            depth_limit += 1


def iterative_deepening_tree(problem, iteration_limit=10000):
    depth_limit = 1
    iterations = 0
    while True:
        try:
            return depth_first_tree(
                problem, depth_limit=depth_limit,
                iteration_limit=iteration_limit - iterations
            )
        except NoSolutionError as e:
            iterations += e.iterations
            if not e.depth_limited:
                raise NoSolutionError(
                    iterations=iterations,
                    iteration_limited=e.iteration_limited
                )
            depth_limit += 1


def iterative_deepening_tree_check_path(problem, iteration_limit=10000):
    depth_limit = 1
    iterations = 0
    while True:
        try:
            return depth_first_tree_check_path(
                problem,
                depth_limit=depth_limit,
                iteration_limit=iteration_limit - iterations
            )
        except NoSolutionError as e:
            iterations += e.iterations
            if not e.depth_limited:
                raise NoSolutionError(
                    iterations=iterations,
                    iteration_limited=e.iteration_limited
                )
            depth_limit += 1


def iterative_deepening_recursive(problem, iteration_limit=10000):
    depth_limit = 1
    iterations = 0
    while True:
        try:
            return depth_first_recursive(
                problem,
                depth_limit=depth_limit,
                iteration_limit=iteration_limit - iterations
            )
        except NoSolutionError as e:
            iterations += e.iterations
            if not e.depth_limited:
                raise NoSolutionError(
                    iterations=iterations,
                    iteration_limited=e.iteration_limited
                )
            depth_limit += 1
