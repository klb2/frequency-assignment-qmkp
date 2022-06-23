from typing import Any, Iterable, Union
import logging
from timeit import default_timer as timer

import numpy as np
from scipy import stats

import qmkphp
from single_frequency import min_rec_power_single_freq
from two_frequencies import min_rec_power_two_freq
from util import to_decibel

LOGGER = logging.getLogger(__name__)

def generate_random_assignment(num_users, num_freq):
    choices = np.random.choice(np.arange(num_freq), size=(num_users, 2),
                               replace=False)
    assignments = np.zeros((num_users, num_freq))
    for _user, _assignment in enumerate(choices):
        assignments[_user, _assignment] = 1
    assignments = assignments.T
    return assignments

def create_profit_matrix(d_min: float, d_max: float, frequencies: Iterable,
                         h_tx: float, h_rx: float):
    main_diag = [min_rec_power_single_freq(d_min, d_max, f, h_tx, h_rx)
                 for f in frequencies]
    idx_triu = np.triu_indices(len(frequencies), k=1)
    profits = np.zeros((len(frequencies), len(frequencies)))
    for i, j in zip(*idx_triu):
        _power_sum = min_rec_power_two_freq(d_min, d_max, frequencies[i],
                                            frequencies[j], h_tx, h_rx)
        profits[i, j] = profits[j, i] = _power_sum - main_diag[i] - main_diag[j]
        #profits[i, j] = profits[j, i] = 1
    profits[np.diag_indices_from(profits)] = main_diag
    #profits = to_decibel(profits)
    return profits


def generate_user_parameters(num_users: int, h_tx: float):
    h_rx = 2*np.random.rand(num_users)+1.
    d_min = 20*np.random.rand(num_users)+20
    _width = 90*np.random.rand(num_users) + 10
    d_max = d_min + _width
    users = [{"h_tx": h_tx, "h_rx": _h_rx, "d_min": _d_min, "d_max": _d_max}
             for _h_rx, _d_min, _d_max in zip(h_rx, d_min, d_max)]
    return users


def main(num_users: int = 3, num_frequencies: int = 10, h_tx: float = 10.,
         frequencies: Iterable = None,
         users: Union[Iterable[dict], None] = None, num_trials: int = 100):
    if users is not None:
        num_users = len(users)
        num_trials = 1
    else:
        users = generate_user_parameters(num_users, h_tx)

    if frequencies is None:
        frequencies = np.linspace(0, 100e6, num_frequencies) + 2.4e9 #np.arange(0, 100)*1e6 + 2.4e9
    num_frequencies = len(frequencies)
    LOGGER.info(f"Number of users: {num_users:d}")
    LOGGER.info(f"Number of frequencies: {num_frequencies:d}")

    capacities = [2]*num_users
    weights = np.ones(num_frequencies)

    results_qmkp = {"time": [], "profit": [], "time_total": []}
    results_random = {"time": [], "profit": []}

    for trial in range(num_trials):
        LOGGER.info(f"Working on trial {trial+1:d}/{num_trials:d}")

        start_profit = timer()
        profits = [create_profit_matrix(frequencies=frequencies, **user_info)
                   for user_info in users]
        profits = np.array(profits)
        LOGGER.debug(f"Profit shape: {np.shape(profits)}")


        start = timer()
        assignments = qmkphp.constructive_procedure(capacities=capacities,
                                                   weights=weights,
                                                   profits=profits)
        end = timer()
        total_profit = qmkphp.total_profit_qmkp(profits, assignments)
        results_qmkp["time_total"].append(end - start_profit)
        results_qmkp["time"].append(end - start)
        results_qmkp["profit"].append(total_profit/num_users)
        LOGGER.debug(f"QMKP Time: {end-start:.3f}")
        LOGGER.debug(f"QMKP Profit: {to_decibel(total_profit/num_users):.1f}")

        start = timer()
        assignments = generate_random_assignment(num_users, len(frequencies))
        end = timer()
        total_profit = qmkphp.total_profit_qmkp(profits, assignments)
        results_random["time"].append(end - start)
        results_random["profit"].append(total_profit/num_users)
        LOGGER.debug(f"Random Time: {end-start:.3f}")
        LOGGER.debug(f"Random Profit: {to_decibel(total_profit/num_users):.1f}")

        users = generate_user_parameters(num_users, h_tx)
    LOGGER.info("QMKP Times: {}".format(stats.describe(results_qmkp['time'])))
    LOGGER.info("QMKP Times Total: {}".format(stats.describe(results_qmkp['time_total'])))
    LOGGER.info("Random Times: {}".format(stats.describe(results_random['time'])))
    LOGGER.debug("QMKP Profit: {}".format(stats.describe(results_qmkp['profit'])))
    LOGGER.debug("Random Profit: {}".format(stats.describe(results_random['profit'])))
    LOGGER.info("QMKP Avg Profit: {} dB".format(to_decibel(np.mean(results_qmkp['profit']))))
    LOGGER.info("Random Avg Profit: {} dB".format(to_decibel(np.mean(results_random['profit']))))


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--num_users", type=int, default=3)
    parser.add_argument("-f", "--num_frequencies", type=int, default=10)
    parser.add_argument("-t", "--h_tx", type=float, default=10)
    parser.add_argument("-c", "--config",
                        help="Config file that contains the user definitions")
    parser.add_argument("-n", "--num_trials", type=int, default=100)
    parser.add_argument("-v", "--verbosity", action="count", default=0,
                        help="Increase output verbosity")
    args = vars(parser.parse_args())
    _config_file = args.pop("config")
    if _config_file is not None:
        import ast
        with open(_config_file, 'r') as _config:
            _config_string = _config.read()
        args['users'] = ast.literal_eval(_config_string)
    verb = args.pop("verbosity")
    logging.basicConfig(format="%(asctime)s - [%(levelname)8s]: %(message)s",
                        handlers=[
                            logging.FileHandler("main.log", encoding="utf-8"),
                            logging.StreamHandler()
                        ])
    loglevel = logging.WARNING - verb*10
    LOGGER.setLevel(loglevel)
    main(**args)
