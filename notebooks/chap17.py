# /// script
# dependencies = ["empiricaldist"]
# ///

import marimo

__generated_with = "0.25.1"
app = marimo.App()


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    You can order print and ebook versions of *Think Bayes 2e* from
    [Bookshop.org](https://bookshop.org/a/98697/9781492089469) and
    [Amazon](https://amzn.to/334eqGo) (affiliate links).

    If you find this book useful, please consider
    [supporting free, open educational materials](https://greenteapress.com/support/?book=tb2) from Green Tea Press.

    And you might like this new book-in-progress by Allen Downey, [*You Would Choose Now: Measuring America's Progress Toward Fairness and Tolerance*](https://leanpub.com/ywcn).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Regression
    """)
    return


@app.cell
def _():
    # install empiricaldist if necessary
    try:
        import empiricaldist
    except ImportError:
        pass  # packages added via marimo's package management: empiricaldist !pip install empiricaldist
    return


@app.cell
def _():
    # Get utils.py

    from os.path import basename, exists

    def download(url):
        filename = basename(url)
        if not exists(filename):
            from urllib.request import urlretrieve
            local, _ = urlretrieve(url, filename)
            print('Downloaded ' + local)
    
    download('https://github.com/AllenDowney/ThinkBayes2/raw/master/soln/utils.py')
    return (download,)


@app.cell
def _():
    from utils import set_pyplot_params
    set_pyplot_params()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    In the previous chapter we saw several examples of logistic regression, which is based on the assumption that the likelihood of an outcome, expressed in the form of log odds, is a linear function of some quantity (continuous or discrete).

    In this chapter we'll work on examples of simple linear regression, which models the relationship between two quantities.  Specifically, we'll look at changes over time in snowfall and the marathon world record.

    The models we'll use have three parameters, so you might want to review the tools we used for the three-parameter model in <<_MarkandRecapture>>.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## More Snow?

    I am under the impression that we don't get as much snow around here as we used to.  By "around here" I mean Norfolk County, Massachusetts, where I was born, grew up, and currently live.  And by "used to" I mean compared to when I was young, like in 1978 when we got [27 inches of snow](https://en.wikipedia.org/wiki/Northeastern_United_States_blizzard_of_1978) and I didn't have to go to school for a couple of weeks.

    Fortunately, we can test my conjecture with data.  Norfolk County happens to be the location of the [Blue Hill Meteorological Observatory](https://en.wikipedia.org/wiki/Blue_Hill_Meteorological_Observatory), which keeps the oldest continuous weather record in North America.

    Data from this and many other weather stations is available from the [National Oceanic and Atmospheric Administration](https://www.ncdc.noaa.gov/cdo-web/search) (NOAA).  I collected data from the Blue Hill Observatory from May 11, 1967 to May 11, 2020.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    To get more data, go to [National Oceanic and Atmospheric Administration](https://www.ncdc.noaa.gov/cdo-web/search), select daily summaries, choose a date range, and search for Stations with search term "Blue Hill Coop". Add it to the cart.

    Open cart and select "Custom GHCN-Daily CSV", then continue.

    Select all data types (but particularly Precipitation) and continue.

    Provide an email address and submit order.

    You'll get an email with a download link. Download the CSV file and move it into the current directory.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The following cell downloads the data as a CSV file.
    """)
    return


@app.cell
def _(download):
    download('https://github.com/AllenDowney/ThinkBayes2/raw/master/data/2239075.csv')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We can use Pandas to read the data into `DataFrame`:
    """)
    return


@app.cell
def _():
    import pandas as pd

    df = pd.read_csv('2239075.csv', parse_dates=[2])
    return df, pd


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Here's what the last few rows look like.
    """)
    return


@app.cell
def _(df):
    df.tail(3)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The columns we'll use are:

    * `DATE`, which is the date of each observation,

    * `SNOW`, which is the total snowfall in inches.

    I'll add a column that contains just the year part of the dates.
    """)
    return


@app.cell
def _(df):
    df['YEAR'] = df['DATE'].dt.year
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    And use `groupby` to add up the total snowfall in each year.
    """)
    return


@app.cell
def _(df):
    snow = df.groupby('YEAR')['SNOW'].sum()
    return (snow,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The first and last years are not complete, so I'll drop them.
    """)
    return


@app.cell
def _(snow):
    snow_1 = snow.iloc[1:-1]
    len(snow_1)
    return (snow_1,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The following figure shows total snowfall during each of the complete years in my lifetime.
    """)
    return


@app.cell
def _(snow_1):
    from utils import decorate
    snow_1.plot(ls='', marker='o', alpha=0.5)
    decorate(xlabel='Year', ylabel='Total annual snowfall (inches)', title='Total annual snowfall in Norfolk County, MA')
    return (decorate,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Looking at this plot, it's hard to say whether snowfall is increasing, decreasing, or unchanged.  In the last decade, we've had several years with more snow than 1978, including 2015, which was the snowiest winter in the Boston area in modern history, with a total of 141 inches.

    This kind of question -- looking at noisy data and wondering whether it is going up or down -- is precisely the question we can answer with Bayesian regression.
    """)
    return


@app.cell
def _(snow_1):
    snow_1.loc[[1978, 1996, 2015]]
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Regression Model

    The foundation of regression (Bayesian or not) is the assumption that a time series like this is the sum of two parts:

    1. A linear function of time, and

    2. A series of random values drawn from a distribution that is not changing over time.

    Mathematically, the regression model is

    $$y = a x + b + \epsilon$$

    where $y$ is the series of measurements (snowfall in this example), $x$ is the series of times (years) and $\epsilon$ is the series of random values.

    $a$ and $b$ are the slope and intercept of the line through the data.  They are unknown parameters, so we will use the data to estimate them.

    We don't know the distribution of $\epsilon$, so we'll make the additional assumption that it is a normal distribution with mean 0 and unknown standard deviation, $\sigma$.
    To see whether this assumption is reasonable, I'll plot the distribution of total snowfall and a normal model with the same mean and standard deviation.

    Here's a `Pmf` object that represents the distribution of snowfall.
    """)
    return


@app.cell
def _(snow_1):
    from empiricaldist import Pmf
    pmf_snowfall = Pmf.from_seq(snow_1)
    return Pmf, pmf_snowfall


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    And here are the mean and standard deviation of the data.
    """)
    return


@app.cell
def _(pmf_snowfall):
    mean, std = pmf_snowfall.mean(), pmf_snowfall.std()
    mean, std
    return mean, std


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    I'll use the `norm` object from SciPy to compute the CDF of a normal distribution with the same mean and standard deviation.
    """)
    return


@app.cell
def _(mean, pmf_snowfall, std):
    from scipy.stats import norm

    dist = norm(mean, std)
    qs = pmf_snowfall.qs
    ps = dist.cdf(qs)
    return norm, ps, qs


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Here's what the distribution of the data looks like compared to the normal model.
    """)
    return


@app.cell
def _(decorate, pmf_snowfall, ps, qs):
    import matplotlib.pyplot as plt

    plt.plot(qs, ps, color='C5', label='model')
    pmf_snowfall.make_cdf().plot(label='data')

    decorate(xlabel='Total snowfall (inches)',
             ylabel='CDF',
             title='Normal model of variation in snowfall')
    return (plt,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We've had more winters below the mean than expected, but overall this looks like a reasonable model.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Least Squares Regression

    Our regression model has three parameters: slope, intercept, and standard deviation of $\epsilon$.
    Before we can estimate them, we have to choose priors.
    To help with that, I'll use StatsModel to fit a line to the data by [least squares regression](https://en.wikipedia.org/wiki/Least_squares).

    First, I'll use `reset_index` to convert `snow`, which is a `Series`, to a `DataFrame`.
    """)
    return


@app.cell
def _(snow_1):
    data = snow_1.reset_index()
    data.head(3)
    return (data,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The result is a `DataFrame` with two columns, `YEAR` and `SNOW`, in a format we can use with StatsModels.

    As we did in the previous chapter, I'll center the data by subtracting off the mean.
    """)
    return


@app.cell
def _(data):
    offset = round(data['YEAR'].mean())
    data['x'] = data['YEAR'] - offset
    offset
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    And I'll add a column to `data` so the dependent variable has a standard name.
    """)
    return


@app.cell
def _(data):
    data['y'] = data['SNOW']
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Now, we can use StatsModels to compute the least squares fit to the data and estimate `slope` and `intercept`.
    """)
    return


@app.cell
def _(data):
    import statsmodels.formula.api as smf
    _formula = 'y ~ x'
    results = smf.ols(_formula, data=data).fit()
    results.params
    return results, smf


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The intercept, about 64 inches, is the expected snowfall when `x=0`, which is the beginning of 1994.
    The estimated slope indicates that total snowfall is increasing at a rate of about 0.5 inches per year.

    `results` also provides `resid`, which is an array of residuals, that is, the differences between the data and the fitted line.
    The standard deviation of the residuals is an estimate of `sigma`.
    """)
    return


@app.cell
def _(results):
    results.resid.std()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We'll use these estimates to choose prior distributions for the parameters.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Priors

    I'll use uniform distributions for all three parameters.
    """)
    return


@app.cell
def _():
    import numpy as np
    from utils import make_uniform
    qs_1 = np.linspace(-0.5, 1.5, 51)
    prior_slope = make_uniform(qs_1, 'Slope')
    return make_uniform, np, prior_slope


@app.cell
def _(make_uniform, np):
    qs_2 = np.linspace(54, 75, 41)
    prior_inter = make_uniform(qs_2, 'Intercept')
    return (prior_inter,)


@app.cell
def _(make_uniform, np):
    qs_3 = np.linspace(20, 35, 31)
    prior_sigma = make_uniform(qs_3, 'Sigma')
    return (prior_sigma,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    I made the prior distributions different lengths for two reasons.  First, if we make a mistake and use the wrong distribution, it will be easier to catch the error if they are all different lengths.

    Second, it provides more precision for the most important parameter, `slope`, and spends less computational effort on the least important, `sigma`.

    In <<_ThreeParameterModel>> we made a joint distribution with three parameters.  I'll wrap that process in a function:
    """)
    return


@app.cell
def _(Pmf):
    from utils import make_joint

    def make_joint3(pmf1, pmf2, pmf3):
        """Make a joint distribution with three parameters."""
        joint2 = make_joint(pmf2, pmf1).stack()
        joint3 = make_joint(pmf3, joint2).stack()
        return Pmf(joint3)

    return (make_joint3,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    And use it to make a `Pmf` that represents the joint distribution of the three parameters.
    """)
    return


@app.cell
def _(make_joint3, prior_inter, prior_sigma, prior_slope):
    prior = make_joint3(prior_slope, prior_inter, prior_sigma)
    prior.head(3)
    return (prior,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The index of `Pmf` has three columns, containing values of `slope`, `inter`, and `sigma`, in that order.

    With three parameters, the size of the joint distribution starts to get big.  Specifically, it is the product of the lengths of the prior distributions.  In this example, the prior distributions have 51, 41, and 31 values, so the length of the joint prior is 64,821.
    """)
    return


@app.cell
def _(prior_inter, prior_sigma, prior_slope):
    len(prior_slope), len(prior_inter), len(prior_sigma)
    return


@app.cell
def _(prior_inter, prior_sigma, prior_slope):
    len(prior_slope) * len(prior_inter) * len(prior_sigma)
    return


@app.cell
def _(prior):
    len(prior)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Likelihood

    Now we'll compute the likelihood of the data.
    To demonstrate the process, let's assume temporarily that the parameters are known.
    """)
    return


@app.cell
def _():
    inter = 64
    slope = 0.51
    sigma = 25
    return inter, sigma, slope


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    I'll extract the `xs` and `ys` from `data` as `Series` objects:
    """)
    return


@app.cell
def _(data):
    xs = data['x']
    ys = data['y']
    return xs, ys


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    And compute the "residuals", which are the differences between the actual values, `ys`, and the values we expect based on `slope` and `inter`.
    """)
    return


@app.cell
def _(inter, slope, xs, ys):
    _expected = slope * xs + inter
    resid = ys - _expected
    return (resid,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    According to the model, the residuals should follow a normal distribution with mean 0 and standard deviation `sigma`.  So we can compute the likelihood of each residual value using `norm` from SciPy.
    """)
    return


@app.cell
def _(norm, resid, sigma):
    densities = norm(0, sigma).pdf(resid)
    return (densities,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The result is an array of probability densities, one for each element of the dataset; their product is the likelihood of the data.
    """)
    return


@app.cell
def _(densities):
    likelihood = densities.prod()
    likelihood
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    As we saw in the previous chapter, the likelihood of any particular dataset tends to be small.
    If it's too small, we might exceed the limits of floating-point arithmetic.
    When that happens, we can avoid the problem by computing likelihoods under a log transform.
    But in this example that's not necessary.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## The Update

    Now we're ready to do the update.  First, we need to compute the likelihood of the data for each possible set of parameters.
    """)
    return


@app.cell
def _(norm, prior, xs, ys):
    likelihood_1 = prior.copy()
    for slope_1, inter_1, sigma_1 in prior.index:
        _expected = slope_1 * xs + inter_1
        resid_1 = ys - _expected
        densities_1 = norm.pdf(resid_1, 0, sigma_1)
        likelihood_1[slope_1, inter_1, sigma_1] = densities_1.prod()
    return (likelihood_1,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    This computation takes longer than many of the previous examples.
    We are approaching the limit of what we can do with grid approximations.

    Nevertheless, we can do the update in the usual way:
    """)
    return


@app.cell
def _(likelihood_1, prior):
    posterior = prior * likelihood_1
    posterior.normalize()
    return (posterior,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The result is a `Pmf` with a three-level index containing values of `slope`, `inter`, and `sigma`.
    To get the marginal distributions from the joint posterior, we can use `Pmf.marginal`, which we saw in <<_ThreeParameterModel>>.
    """)
    return


@app.cell
def _(posterior):
    posterior_slope = posterior.marginal(0)
    posterior_inter = posterior.marginal(1)
    posterior_sigma = posterior.marginal(2)
    return posterior_inter, posterior_sigma, posterior_slope


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Here's the posterior distribution for `sigma`:
    """)
    return


@app.cell
def _(decorate, posterior_sigma):
    posterior_sigma.plot()

    decorate(xlabel='$\sigma$, standard deviation of $\epsilon$',
             ylabel='PDF',
             title='Posterior marginal distribution of $\sigma$')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The most likely values for `sigma` are near 26 inches, which is consistent with our estimate based on the standard deviation of the data.

    However, to say whether snowfall is increasing or decreasing, we don't really care about `sigma`.  It is a "nuisance parameter", so-called because we have to estimate it as part of the model, but we don't need it to answer the questions we are interested in.

    Nevertheless, it is good to check the marginal distributions to make sure

    * The location is consistent with our expectations, and

    * The posterior probabilities are near 0 at the extremes of the range, which indicates that the prior distribution covers all parameters with non-negligible probability.

    In this example, the posterior distribution of `sigma` looks fine.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Here's the posterior distribution of `inter`:
    """)
    return


@app.cell
def _(decorate, posterior_inter):
    posterior_inter.plot(color='C1')
    decorate(xlabel='intercept (inches)',
             ylabel='PDF',
             title='Posterior marginal distribution of intercept')
    return


@app.cell
def _(posterior_inter):
    from utils import summarize
    
    summarize(posterior_inter)
    return (summarize,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The posterior mean is about 64 inches, which is the expected amount of snow during the year at the midpoint of the range, 1994.

    And finally, here's the posterior distribution of `slope`:
    """)
    return


@app.cell
def _(decorate, posterior_slope):
    posterior_slope.plot(color='C4')
    decorate(xlabel='Slope (inches per year)',
             ylabel='PDF',
             title='Posterior marginal distribution of slope')
    return


@app.cell
def _(posterior_slope, summarize):
    summarize(posterior_slope)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The posterior mean is about 0.51 inches, which is consistent with the estimate we got from least squared regression.

    The 90% credible interval is from 0.1 to 0.9, which indicates that our uncertainty about this estimate is pretty high.  In fact, there is still a small posterior probability (about 2\%) that the slope is negative.
    """)
    return


@app.cell
def _(posterior_slope):
    posterior_slope.make_cdf()(0)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    However, it is more likely that my conjecture was wrong: we are actually getting more snow around here than we used to, increasing at a rate of about a half-inch per year, which is substantial.  On average, we get an additional 25 inches of snow per year than we did when I was young.

    This example shows that with slow-moving trends and noisy data, your instincts can be misleading.

    Now, you might suspect that I overestimate the amount of snow when I was young because I enjoyed it, and underestimate it now because I don't.  But you would be mistaken.

    During the Blizzard of 1978, we did not have a snowblower and my brother and I had to shovel.  My sister got a pass for no good reason.  Our driveway was about 60 feet long and three cars wide near the garage.  And we had to shovel Mr. Crocker's driveway, too, for which we were not allowed to accept payment.  Furthermore, as I recall it was during this excavation that I accidentally hit my brother with a shovel on the head, and it bled a lot because, you know, scalp wounds.

    Anyway, the point is that I don't think I overestimate the amount of snow when I was young because I have fond memories of it.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Optimization

    The way we computed the likelihood in the previous section was pretty slow.  The problem is that we looped through every possible set of parameters in the prior distribution, and there were more than 60,000 of them.

    If we can do more work per iteration, and run the loop fewer times, we expect it to go faster.

    In order to do that, I'll unstack the prior distribution:
    """)
    return


@app.cell
def _(prior):
    joint3 = prior.unstack()
    joint3.head(3)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The result is a `DataFrame` with `slope` and `intercept` down the rows and `sigmas` across the columns.

    The following is a version of `likelihood_regression` that takes the joint prior distribution in this form and returns the posterior distribution in the same form.
    """)
    return


@app.cell
def _(norm, np):
    from utils import normalize

    def update_optimized(prior, data):
        """Posterior distribution of regression parameters
        `slope`, `inter`, and `sigma`.
    
        prior: Pmf representing the joint prior
        data: DataFrame with columns `x` and `y`
    
        returns: Pmf representing the joint posterior
        """
        xs = data['x']
        ys = data['y']
        sigmas = prior.columns    
        likelihood = prior.copy()

        for slope, inter in prior.index:
            expected = slope * xs + inter
            resid = ys - expected
            resid_mesh, sigma_mesh = np.meshgrid(resid, sigmas)
            densities = norm.pdf(resid_mesh, 0, sigma_mesh)
            likelihood.loc[slope, inter] = densities.prod(axis=1)
        
        posterior = prior * likelihood
        normalize(posterior)
        return posterior

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    This version loops through all possible pairs of `slope` and `inter`, so the loop runs about 2000 times.
    """)
    return


@app.cell
def _(prior_inter, prior_slope):
    len(prior_slope) * len(prior_inter)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Each time through the loop, it uses a grid mesh to compute the likelihood of the data for all values of `sigma`.  The result is an array with one column for each data point and one row for each value of `sigma`.  Taking the product across the columns (`axis=1`) yields the probability of the data for each value of sigma, which we assign as a row in `likelihood`.
    """)
    return


@app.cell
def _():
    # magic command not supported in marimo; please file an issue to add support
    # %time posterior_opt = update_optimized(joint3, data)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We get the same result either way.
    """)
    return


@app.cell
def _(np, posterior, posterior_opt):
    np.allclose(posterior, posterior_opt.stack())
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    But this version is about 25 times faster than the previous version.

    This optimization works because many functions in NumPy and SciPy are written in C, so they run fast compared to Python.  If you can do more work each time you call these functions, and less time running the loop in Python, your code will often run substantially faster.

    In this version of the posterior distribution, `slope` and `inter` run down the rows and `sigma` runs across the columns.  So we can use `marginal` to get the posterior joint distribution of `slope` and `intercept`.
    """)
    return


@app.cell
def _(posterior_opt):
    from utils import marginal

    posterior2 = marginal(posterior_opt, 1)
    posterior2.head(3)
    return (posterior2,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The result is a `Pmf` with two columns in the index.
    To plot it, we have to unstack it.
    """)
    return


@app.cell
def _(posterior2):
    joint_posterior = posterior2.unstack().transpose()
    joint_posterior.head(3)
    return (joint_posterior,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Here's what it looks like.
    """)
    return


@app.cell
def _(decorate, joint_posterior):
    from utils import plot_contour

    plot_contour(joint_posterior)
    decorate(title='Posterior joint distribution of slope and intercept')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The ovals in the contour plot are aligned with the axes, which indicates that there is no correlation between `slope` and `inter` in the posterior distribution, which is what we expect since we centered the values.

    In this example, the motivating question is about the slope of the line, so we answered it by looking at the posterior distribution of slope.

    In the next example, the motivating question is about prediction, so we'll use the joint posterior distribution to generate predictive distributions.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Marathon World Record

    For many running events, if you plot the world record pace over time, the result is a remarkably straight line.  People, [including me](http://allendowney.blogspot.com/2011/04/two-hour-marathon-in-2045.html), have speculated about possible reasons for this phenomenon.

    People have also speculated about when, if ever, the world record time for the marathon will be less than two hours.
    (Note: In 2019 Eliud Kipchoge ran the marathon distance in under two hours, which is an astonishing achievement that I fully appreciate, but for several reasons it did not count as a world record).

    So, as a second example of Bayesian regression, we'll consider the world record progression for the marathon (for male runners), estimate the parameters of a linear model, and use the model to predict when a runner will break the two-hour barrier.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The following cell downloads a web page from Wikipedia that includes a table of marathon world records, and uses Pandas to put the data in a `DataFrame`.
    """)
    return


@app.cell
def _():
    url = "https://github.com/AllenDowney/ThinkBayes2/raw/master/data/Marathon_world_record_progression.html"
    return (url,)


@app.cell
def _(pd, url):
    tables = pd.read_html(url)
    len(tables)
    return (tables,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The first table is the one we want.
    """)
    return


@app.cell
def _(tables):
    table = tables[0]
    table.tail(3)
    return (table,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We can use Pandas to parse the dates.
    A few of them include notes that cause parsing problems, but the argument `errors='coerce'` tells Pandas to fill invalid dates with `NaT`, which is a version of `NaN` that represents "not a time".
    """)
    return


@app.cell
def _(pd, table):
    table['date'] = pd.to_datetime(table['Date'], errors='coerce')
    table['date'].head()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We can also use Pandas to parse the record times.
    """)
    return


@app.cell
def _(pd, table):
    table['time'] = pd.to_timedelta(table['Time'])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    And convert the times to paces in miles per hour.
    """)
    return


@app.cell
def _(table):
    table['y'] = 26.2 / table['time'].dt.total_seconds() * 3600
    table['y'].head()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The following function plots the results.
    """)
    return


@app.cell
def _(decorate, plt):
    def plot_speeds(df):
        """Plot marathon world record speed as a function of time.
    
        df: DataFrame with date and mph
        """
        plt.axhline(13.1, color='C5', ls='--')
        plt.plot(df['date'], df['y'], 'o', 
                 label='World record speed', 
                 color='C1', alpha=0.5)
    
        decorate(xlabel='Date',
                 ylabel='Speed (mph)')

    return (plot_speeds,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Here's what the results look like.
    The dashed line shows the speed required for a two-hour marathon, 13.1 miles per hour.
    """)
    return


@app.cell
def _(plot_speeds, table):
    plot_speeds(table)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    It's not a perfectly straight line.  In the early years of the marathon, the record speed increased quickly; since about 1970, it has been increasing more slowly.

    For our analysis, let's focus on the recent progression, starting in 1970.
    """)
    return


@app.cell
def _(pd, table):
    recent = table['date'] > pd.to_datetime('1970')
    data_1 = table.loc[recent].copy()
    data_1.head()
    return (data_1,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    In the notebook for this chapter, you can see how I loaded and cleaned the data.  The result is a `DataFrame` that contains the following columns (and additional information we won't use):

    * `date`, which is a Pandas `Timestamp` representing the date when the world record was broken, and

    * `speed`, which records the record-breaking pace in mph.

    Here's what the results look like, starting in 1970:
    """)
    return


@app.cell
def _(data_1, plot_speeds):
    plot_speeds(data_1)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The data points fall approximately on a line, although it's possible that the slope is increasing.

    To prepare the data for regression, I'll subtract away the approximate midpoint of the time interval, 1995.
    """)
    return


@app.cell
def _(pd, table):
    offset_1 = pd.to_datetime('1995')
    timedelta = table['date'] - offset_1
    return offset_1, timedelta


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    When we subtract two `Timestamp` objects, the result is a "time delta", which we can convert to seconds and then to years.
    """)
    return


@app.cell
def _(data_1, timedelta):
    data_1['x'] = timedelta.dt.total_seconds() / 3600 / 24 / 365.24
    return


@app.cell
def _(data_1):
    data_1['x'].describe()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    As in the previous example, I'll use least squares regression to compute point estimates for the parameters, which will help with choosing priors.
    """)
    return


@app.cell
def _(data_1, smf):
    _formula = 'y ~ x'
    results_1 = smf.ols(_formula, data=data_1).fit()
    results_1.params
    return (results_1,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The estimated intercept is about 12.5 mph, which is the interpolated world record pace for 1995.  The estimated slope is about 0.015 mph per year, which is the rate the world record pace is increasing, according to the model.

    Again, we can use the standard deviation of the residuals as a point estimate for `sigma`.
    """)
    return


@app.cell
def _(results_1):
    results_1.resid.std()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    These parameters give us a good idea where we should put the prior distributions.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## The Priors

    Here are the prior distributions I chose for `slope`, `intercept`, and `sigma`.
    """)
    return


@app.cell
def _(make_uniform, np):
    qs_4 = np.linspace(0.012, 0.018, 51)
    prior_slope_1 = make_uniform(qs_4, 'Slope')
    return (prior_slope_1,)


@app.cell
def _(make_uniform, np):
    qs_5 = np.linspace(12.4, 12.5, 41)
    prior_inter_1 = make_uniform(qs_5, 'Intercept')
    return (prior_inter_1,)


@app.cell
def _(make_uniform, np):
    qs_6 = np.linspace(0.01, 0.21, 31)
    prior_sigma_1 = make_uniform(qs_6, 'Sigma')
    return (prior_sigma_1,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    And here's the joint prior distribution.
    """)
    return


@app.cell
def _(make_joint3, prior_inter_1, prior_sigma_1, prior_slope_1):
    prior_1 = make_joint3(prior_slope_1, prior_inter_1, prior_sigma_1)
    prior_1.head()
    return (prior_1,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Now we can compute likelihoods as in the previous example:
    """)
    return


@app.cell
def _(data_1, norm, prior_1):
    xs_1 = data_1['x']
    ys_1 = data_1['y']
    likelihood_2 = prior_1.copy()
    for slope_2, inter_2, sigma_2 in prior_1.index:
        _expected = slope_2 * xs_1 + inter_2
        resid_2 = ys_1 - _expected
        densities_2 = norm.pdf(resid_2, 0, sigma_2)
        likelihood_2[slope_2, inter_2, sigma_2] = densities_2.prod()
    return (likelihood_2,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Now we can do the update in the usual way.
    """)
    return


@app.cell
def _(likelihood_2, prior_1):
    posterior_1 = prior_1 * likelihood_2
    posterior_1.normalize()
    return (posterior_1,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    And unpack the marginals:
    """)
    return


@app.cell
def _(posterior_1):
    posterior_slope_1 = posterior_1.marginal(0)
    posterior_inter_1 = posterior_1.marginal(1)
    posterior_sigma_1 = posterior_1.marginal(2)
    return posterior_inter_1, posterior_sigma_1, posterior_slope_1


@app.cell
def _(posterior_sigma_1):
    posterior_sigma_1.plot()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Here's the posterior distribution of `inter`:
    """)
    return


@app.cell
def _(decorate, posterior_inter_1):
    posterior_inter_1.plot(color='C1')
    decorate(xlabel='intercept', ylabel='PDF', title='Posterior marginal distribution of intercept')
    return


@app.cell
def _(posterior_inter_1, summarize):
    summarize(posterior_inter_1)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The posterior mean is about 12.5 mph, which is the world record marathon pace the model predicts for the midpoint of the date range, 1994.

    And here's the posterior distribution of `slope`.
    """)
    return


@app.cell
def _(decorate, posterior_slope_1):
    posterior_slope_1.plot(color='C4')
    decorate(xlabel='Slope', ylabel='PDF', title='Posterior marginal distribution of slope')
    return


@app.cell
def _(posterior_slope_1, summarize):
    summarize(posterior_slope_1)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The posterior mean is about 0.015 mph per year, or 0.15 mph per decade.

    That's interesting, but it doesn't answer the question we're interested in: When will there be a two-hour marathon? To answer that, we have to make predictions.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Prediction

    To generate predictions, I'll draw a sample from the posterior distribution of parameters, then use the regression equation to combine the parameters with the data.

    `Pmf` provides `choice`, which we can use to draw a random sample with replacement, using the posterior probabilities as weights.
    """)
    return


@app.cell
def _(np):
    np.random.seed(17)
    return


@app.cell
def _(posterior_1):
    sample = posterior_1.choice(101)
    return (sample,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The result is an array of tuples.  Looping through the sample, we can use the regression equation to generate predictions for a range of `xs`.
    """)
    return


@app.cell
def _(norm, np, sample):
    xs_2 = np.arange(-25, 50, 2)
    pred = np.empty((len(sample), len(xs_2)))
    for i, (slope_3, inter_3, sigma_3) in enumerate(sample):
        epsilon = norm(0, sigma_3).rvs(len(xs_2))
        pred[i] = inter_3 + slope_3 * xs_2 + epsilon
    return pred, xs_2


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Each prediction is an array with the same length as `xs`, which I store as a row in `pred`.  So the result has one row for each sample and one column for each value of `x`.

    We can use `percentile` to compute the 5th, 50th, and 95th percentiles in each column.
    """)
    return


@app.cell
def _(np, pred):
    low, median, high = np.percentile(pred, [5, 50, 95], axis=0)
    return high, low, median


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    To show the results, I'll plot the median of the predictions as a line and the 90% credible interval as a shaded area.
    """)
    return


@app.cell
def _(data_1, high, low, median, offset_1, pd, plot_speeds, plt, xs_2):
    times = pd.to_timedelta(xs_2 * 365.24, unit='days') + offset_1
    plt.fill_between(times, low, high, color='C2', alpha=0.1)
    plt.plot(times, median, color='C2')
    plot_speeds(data_1)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The dashed line shows the two-hour marathon pace, which is 13.1 miles per hour.
    Visually we can estimate that the prediction line hits the target pace between 2030 and 2040.

    To make this more precise, we can use interpolation to see when the predictions cross the finish line.  SciPy provides `interp1d`, which does linear interpolation by default.
    """)
    return


@app.cell
def _(high, low, median, np, xs_2):
    from scipy.interpolate import interp1d
    future = np.array([interp1d(high, xs_2)(13.1), interp1d(median, xs_2)(13.1), interp1d(low, xs_2)(13.1)])
    return (future,)


@app.cell
def _(future, offset_1, pd):
    dts = pd.to_timedelta(future * 365.24, unit='day') + offset_1
    pd.DataFrame(dict(datetime=dts), index=['early', 'median', 'late'])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The median prediction is 2036, with a 90% credible interval from 2032 to 2043.  So there is about a 5% chance we'll see a two-hour marathon before 2032.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Summary

    This chapter introduces Bayesian regression, which is based on the same model as least squares regression; the difference is that it produces a posterior distribution for the parameters rather than point estimates.

    In the first example, we looked at changes in snowfall in Norfolk County, Massachusetts, and concluded that we get more snowfall now than when I was young, contrary to my expectation.

    In the second example, we looked at the progression of world record pace for the men's marathon, computed the joint posterior distribution of the regression parameters, and used it to generate predictions for the next 20 years.

    These examples have three parameters, so it takes a little longer to compute the likelihood of the data.
    With more than three parameters, it becomes impractical to use grid algorithms.

    In the next few chapters, we'll explore other algorithms that reduce the amount of computation we need to do a Bayesian update, which makes it possible to use models with more parameters.

    But first, you might want to work on these exercises.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Exercises
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Exercise:** I am under the impression that it is warmer around here than it used to be.  In this exercise, you can put my conjecture to the test.

    We'll use the same dataset we used to model snowfall; it also includes daily low and high temperatures in Norfolk County, Massachusetts during my lifetime.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Here's the data.
    """)
    return


@app.cell
def _(pd):
    df_1 = pd.read_csv('2239075.csv', parse_dates=[2])
    df_1.head(3)
    return (df_1,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Again, I'll create a column that contains the year part of the dates.
    """)
    return


@app.cell
def _(df_1):
    df_1['YEAR'] = df_1['DATE'].dt.year
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    This dataset includes `TMIN` and `TMAX`, which are the daily low and high temperatures in degrees F.
    I'll create a new column with the daily midpoint of the low and high temperatures.
    """)
    return


@app.cell
def _(df_1):
    df_1['TMID'] = (df_1['TMIN'] + df_1['TMAX']) / 2
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Now we can group by year and compute the mean of these daily temperatures.
    """)
    return


@app.cell
def _(df_1):
    tmid = df_1.groupby('YEAR')['TMID'].mean()
    len(tmid)
    return (tmid,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Again, I'll drop the first and last years, which are incomplete.
    """)
    return


@app.cell
def _(tmid):
    complete = tmid.iloc[1:-1]
    len(complete)
    return (complete,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Here's what the time series looks like.
    """)
    return


@app.cell
def _(complete, decorate):
    complete.plot(ls='', marker='o', alpha=0.5)

    decorate(xlabel='Year',
             ylabel='Annual average of daily temperature (deg F)')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    As we did with the snow data, I'll convert the `Series` to a `DataFrame` to prepare it for regression.
    """)
    return


@app.cell
def _(complete):
    data_2 = complete.reset_index()
    data_2.head()
    return (data_2,)


@app.cell
def _(data_2):
    offset_2 = round(data_2['YEAR'].mean())
    offset_2
    return (offset_2,)


@app.cell
def _(data_2, offset_2):
    data_2['x'] = data_2['YEAR'] - offset_2
    data_2['x'].mean()
    return


@app.cell
def _(data_2):
    data_2['y'] = data_2['TMID']
    data_2['y'].std()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Now we can use StatsModels to estimate the parameters.
    """)
    return


@app.cell
def _(data_2, smf):
    _formula = 'y ~ x'
    results_2 = smf.ols(_formula, data=data_2).fit()
    results_2.params
    return (results_2,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    And compute the standard deviation of the parameters.
    """)
    return


@app.cell
def _(results_2):
    results_2.resid.std()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    According to the least squares regression model, annual average temperature is increasing by about 0.044 degrees F per year.

    To quantify the uncertainty of these parameters and generate predictions for the future, we can use Bayesian regression.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    1. Use StatsModels to generate point estimates for the regression parameters.

    2. Choose priors for `slope`, `intercept`, and `sigma` based on these estimates, and use `make_joint3` to make a joint prior distribution.

    3. Compute the likelihood of the data and compute the posterior distribution of the parameters.

    4. Extract the posterior distribution of `slope`.  How confident are we that temperature is increasing?

    5. Draw a sample of parameters from the posterior distribution and use it to generate predictions up to 2067.

    6. Plot the median of the predictions and a 90% credible interval along with the observed data.

    Does the model fit the data well?  How much do we expect annual average temperatures to increase over my (expected) lifetime?
    """)
    return


@app.cell
def _():
    # Solution goes here
    return


@app.cell
def _():
    # Solution goes here
    return


@app.cell
def _():
    # Solution goes here
    return


@app.cell
def _():
    # Solution goes here
    return


@app.cell
def _():
    # Solution goes here
    return


@app.cell
def _():
    # Solution goes here
    return


@app.cell
def _():
    # Solution goes here
    return


@app.cell
def _():
    # Solution goes here
    return


@app.cell
def _():
    # Solution goes here
    return


@app.cell
def _():
    # Solution goes here
    return


@app.cell
def _():
    # Solution goes here
    return


@app.cell
def _():
    # Solution goes here
    return


@app.cell
def _():
    # Solution goes here
    return


@app.cell
def _():
    # Solution goes here
    return


@app.cell
def _():
    # Solution goes here
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    *Think Bayes*, Second Edition

    Copyright 2020 Allen B. Downey

    License: [Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)](https://creativecommons.org/licenses/by-nc-sa/4.0/)
    """)
    return


if __name__ == "__main__":
    app.run()
