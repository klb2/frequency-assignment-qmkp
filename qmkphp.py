from typing import Iterable, Any

import numpy as np

from util import is_binary, is_feasible_solution


def total_profit_qmkp(profits: np.array, assignments: np.array, comb_func=sum):
    """
    Parameters
    ----------
    profits : array (K x N x N)
        Symmetric matrix containing the profits :math:`p_{ij}`

    assignments : array (N x K)
        Matrix with binary elements where column :math:`j` corresponds to the
        assignments of the :math:`N` items to knapsack :math:`j`.
    """
    if not is_binary(assignments):
        raise ValueError("The assignments matrix needs to be binary.")
    _profit_matrix = assignments.T @ profits @ assignments
    _double_main_diag = assignments.T @ np.diagonal(profits, axis1=1, axis2=2).T
    ks_profits = np.diag(_double_main_diag+np.diagonal(_profit_matrix, axis1=1, axis2=2))
    ks_profits = ks_profits / 2
    return comb_func(ks_profits)

def value_density(profits: np.array, assignments: np.array,
                  weights: Iterable[float], reduced_output: bool = False):
    """
    This function will always add object :math:`i` to the selected objects for
    the value of object :math:`i`.

    Parameters
    ----------
    profits : array (K x N x N)
        Symmetric matrix containing the profits :math:`p_{ij}`

    assignments : array (N x K)
        Set of current assignments

    weights : list (N)
        Weights of the objects

    Returns
    -------
    vd : array (N x K)
        Density values for all items and users
    """
    num_objects, num_users = np.shape(assignments)
    unassigned_items = np.where(np.all(assignments == 0, axis=1))[0]
    contributions = profits @ assignments
    contributions = np.diagonal(contributions, axis1=0, axis2=2)
    _main_diag = np.diagonal(profits, axis1=1, axis2=2).T
    _main_diag_contrib = (np.ones_like(assignments)-assignments)*_main_diag
    contributions = contributions + _main_diag_contrib
    weights = np.tile(weights, (num_users, 1)).T
    densities = contributions/weights
    if reduced_output:
        return densities[unassigned_items], unassigned_items
    return densities

def constructive_procedure(capacities: Iterable[float],
                           weights: Iterable[float],
                           profits: np.array,
                           starting_assignment: np.array = None):
    """Algorithm 1
    This is the implementation of the constructive procedure for the quadratic
    multiple knapsack problem with heterogeneous profits (QMKP-HP).


    Parameters
    ----------
    capacities : list (K)
        Capacities of the knapsacks

    weights : list (N)
        Weights of the objects

    profits : array (K x N x N)
        Symmetric matrix containing the profits :math:`p_{u,ij}`

    starting_assignments : array (N x K), optional
        Initial assignments of some objects to users. If this is `None`, no
        initial assignments are assumed.

    Returns
    -------
    assignments : array (N x K)
        Final assignments
    """
    capacities = np.array(capacities)
    weights = np.array(weights)
    num_items = len(weights)
    num_ks = len(capacities)

    # 1. Initialization
    if starting_assignment is None:
        starting_assignment = np.zeros((num_items, num_ks))
    if not is_binary(starting_assignment):
        raise ValueError("The starting assignment needs to be a binary matrix")
    if not np.all(np.shape(starting_assignment) == (num_items, num_ks)):
        raise ValueError("The shape of the starting assignment needs to be num_items x num_knapsacks")

    start_load = weights @ starting_assignment
    capacities = capacities - start_load

    dens_v, unassigned = value_density(profits, starting_assignment, weights,
                                       reduced_output=True)

    # 2. Iterative Step
    #solution = np.zeros((num_items, num_ks))
    solution = np.copy(starting_assignment)
    while len(unassigned) > 0 and np.min(weights[unassigned]) < np.max(capacities):
        idx_sort_v_flat = np.argsort(dens_v, axis=None)[::-1]
        idx_sort_v = np.unravel_index(idx_sort_v_flat, np.shape(dens_v))
        for idx_el_v, idx_user in zip(*idx_sort_v):
            idx_element = unassigned[idx_el_v]
            if weights[idx_element] <= capacities[idx_user]:
                solution[idx_element, idx_user] = 1
                capacities[idx_user] = capacities[idx_user] - weights[idx_element]
                break
        dens_v, unassigned = value_density(profits, solution, weights,
                                           reduced_output=True)
    return solution
