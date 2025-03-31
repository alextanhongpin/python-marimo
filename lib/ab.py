import math

import scipy.stats as st
import statsmodels.stats.api as sm
import statsmodels.stats.power as sp


def sample_size_for_mean_difference(delta, std, power=0.8, alpha=0.05, sides=1):
    return math.ceil(
        sp.normal_sample_size_one_tail(
            delta, power, alpha / sides, std_null=std, std_alternative=None
        )
    )


def sample_size_for_proportions(
    p1, p2, alpha=0.05, power=0.8, alternative="two-sided", ratio=1, **kwargs
):
    return math.ceil(
        sm.samplesize_proportions_2indep_onetail(
            p1 - p2,
            p2,
            power=power,
            alpha=alpha,
            alternative=alternative,
            ratio=ratio,
            **kwargs,
        )
    )


def confint_proportions_2indep(
    count1: int,
    nobs1: int,
    count2: int,
    nobs2: int,
    method="agresti-caffo",
    alpha=0.05,
    correction=True,
    **kwargs,
):
    return sm.confint_proportions_2indep(
        count1,
        nobs1,
        count2,
        nobs2,
        method=method,
        compare="diff",
        alpha=alpha,
        correction=correction,
        **kwargs,
    )


def power_proportions_2indep(
    p1,
    p2,
    nobs1,
    nobs2,
    alpha=0.05,
    alternative="two-sided",
    return_results=False,
    **kwargs,
):
    return sm.power_proportions_2indep(
        p1 - p2,
        p2,
        nobs1=nobs1,
        ratio=nobs2 / nobs1,
        alpha=alpha,
        alternative=alternative,
        return_results=return_results,
        **kwargs,
    )


def test_proportions_2indep(
    count1,
    nobs1,
    count2,
    nobs2,
    method="agresti-caffo",
    alternative="two-sided",
    return_results=False,
    **kwargs,
):
    stat, p_value = sm.test_proportions_2indep(
        count1,
        nobs1,
        count2,
        nobs2,
        method=method,
        return_results=return_results,
        alternative=alternative,
        **kwargs,
    )

    return stat, p_value


def test_mean_2indep(
    *, mean1, mean2, std1, std2, nobs1, nobs2, alternative="two-sided"
):
    res = st.ttest_ind_from_stats(
        mean1=mean1,
        mean2=mean2,
        nobs1=nobs1,
        nobs2=nobs2,
        std1=std1,
        std2=std2,
        alternative=alternative,
    )

    return res.statistic, res.pvalue


def proportions_confint(
    *,
    count1,
    count2,
    nobs1,
    nobs2,
    alpha=0.05,
    method="binom_test",
):
    ci1, ci2 = sm.proportion_confint(
        count=[count1, count2],
        nobs=[nobs1, nobs2],
        alpha=alpha,
        method=method,
    )
    ci_lower1, ci_upper1 = ci1
    ci_lower2, ci_upper2 = ci2

    return (ci_lower1, ci_upper1), (ci_lower2, ci_upper2)
