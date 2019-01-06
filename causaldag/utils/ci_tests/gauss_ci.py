import numpy as np
from typing import Dict
from scipy.stats import norm


def gauss_ci_test(suffstat: Dict, i, j, cond_set=None, alpha=0.05):
    """
    Test the null hypothesis that i and j are conditionally independent given cond_set via Fisher's z-transform.

    :param suffstat: dictionary containing 'n': number of samples, and 'C': correlation matrix
    :param i: position of first variable in correlation matrix.
    :param j: position of second variable in correlation matrix.
    :param alpha: Significance level.
    :param cond_set: positions of conditioning set in correlation matrix.
    :return: dictionary containing statistic, crit_val, p_value, and reject.
    """
    n = suffstat['n']
    C = suffstat['C']
    n_cond = 0 if cond_set is None else len(cond_set)

    if cond_set is None:
        r = C[i, j]
    else:
        theta = np.linalg.inv(C[np.ix_([i, j, *cond_set], [i, j, *cond_set])])
        r = -theta[0, 1]/(theta[0, 0] * theta[1, 1])  # Theta_{ij}/(Theta_{ii}*Theta_{jj})

    statistic = np.sqrt(n - n_cond - 3) * np.abs(.5 * np.log1p(2*r/(1 - r)))
    # NOTE: log1p(2r/(1-r)) = log((1+r)/(1-r)) but is more numerically stable for r near 0

    crit_val = norm.ppf(1 - alpha/2)
    p_value = norm.cdf(statistic)

    return dict(statistic=statistic, crit_val=crit_val, p_value=p_value, reject=statistic > crit_val)


