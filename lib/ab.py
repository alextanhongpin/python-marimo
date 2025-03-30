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
    p1, p2, alpha=0.05, power=0.8, alternative="two-sided", ratio=1
):
    return math.ceil(
        sm.samplesize_proportions_2indep_onetail(
            p2 - p1, p1, power=power, alpha=alpha, alternative=alternative, ratio=ratio
        )
    )


def test_proportions_2indep(count1, count2, nobs1, nobs2, alternative="two-sided"):
    stat, p_value = sm.test_proportions_2indep(
        count1, nobs1, count2, nobs2, return_results=False, alternative=alternative
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
