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
    # Survival Analysis
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
    This chapter introduces "survival analysis", which is a set of statistical methods used to answer questions about the time until an event.
    In the context of medicine it is literally about survival, but it can be applied to the time until any kind of event, or instead of time it can be about space or other dimensions.

    Survival analysis is challenging because the data we have are often incomplete.  But as we'll see, Bayesian methods are particularly good at working with incomplete data.

    As examples, we'll consider two applications that are a little less serious than life and death: the time until light bulbs fail and the time until dogs in a shelter are adopted.
    To describe these "survival times", we'll use the Weibull distribution.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## The Weibull Distribution

    The [Weibull distribution](https://en.wikipedia.org/wiki/Weibull_distribution) is often used in survival analysis because it is a good model for the distribution of lifetimes for manufactured products, at least over some parts of the range.

    SciPy provides several versions of the Weibull distribution; the one we'll use is called `weibull_min`.
    To make the interface consistent with our notation, I'll wrap it in a function that takes as parameters $\lambda$, which mostly affects the location or "central tendency" of the distribution, and $k$, which affects the shape.
    """)
    return


@app.cell
def _():
    from scipy.stats import weibull_min

    def weibull_dist(lam, k):
        return weibull_min(k, scale=lam)

    return (weibull_dist,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    As an example, here's a Weibull distribution with parameters $\lambda=3$ and $k=0.8$.
    """)
    return


@app.cell
def _(weibull_dist):
    lam = 3
    k = 0.8
    actual_dist = weibull_dist(lam, k)
    return actual_dist, k, lam


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The result is an object that represents the distribution.
    Here's what the Weibull CDF looks like with those parameters.
    """)
    return


@app.cell
def _(actual_dist):
    import numpy as np
    from empiricaldist import Cdf
    from utils import decorate

    qs = np.linspace(0, 12, 101)
    ps = actual_dist.cdf(qs)
    cdf = Cdf(ps, qs)
    cdf.plot()

    decorate(xlabel='Duration in time', 
             ylabel='CDF',
             title='CDF of a Weibull distribution')
    return Cdf, decorate, np


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    `actual_dist` provides `rvs`, which we can use to generate a random sample from this distribution.
    """)
    return


@app.cell
def _(np):
    np.random.seed(17)
    return


@app.cell
def _(actual_dist):
    data = actual_dist.rvs(10)
    data
    return (data,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    So, given the parameters of the distribution, we can generate a sample.
    Now let's see if we can go the other way: given the sample, we'll estimate the parameters.

    Here's a uniform prior distribution for $\lambda$:
    """)
    return


@app.cell
def _(np):
    from utils import make_uniform
    _lams = np.linspace(0.1, 10.1, num=101)
    prior_lam = make_uniform(_lams, name='lambda')
    return make_uniform, prior_lam


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    And a uniform prior for $k$:
    """)
    return


@app.cell
def _(make_uniform, np):
    _ks = np.linspace(0.1, 5.1, num=101)
    prior_k = make_uniform(_ks, name='k')
    return (prior_k,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    I'll use `make_joint` to make a joint prior distribution for the two parameters.
    """)
    return


@app.cell
def _(prior_k, prior_lam):
    from utils import make_joint

    prior = make_joint(prior_lam, prior_k)
    return make_joint, prior


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The result is a `DataFrame` that represents the joint prior, with possible values of $\lambda$ across the columns and values of $k$ down the rows.

    Now I'll use `meshgrid` to make a 3-D mesh with $\lambda$ on the first axis (`axis=0`), $k$ on the second axis (`axis=1`), and the data on the third axis (`axis=2`).
    """)
    return


@app.cell
def _(data, np, prior):
    lam_mesh, k_mesh, data_mesh = np.meshgrid(
        prior.columns, prior.index, data)
    return data_mesh, k_mesh, lam_mesh


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Now we can use `weibull_dist` to compute the PDF of the Weibull distribution for each pair of parameters and each data point.
    """)
    return


@app.cell
def _(data_mesh, k_mesh, lam_mesh, weibull_dist):
    densities = weibull_dist(lam_mesh, k_mesh).pdf(data_mesh)
    densities.shape
    return (densities,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The likelihood of the data is the product of the probability densities along `axis=2`.
    """)
    return


@app.cell
def _(densities):
    likelihood = densities.prod(axis=2)
    likelihood.sum()
    return (likelihood,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Now we can compute the posterior distribution in the usual way.
    """)
    return


@app.cell
def _(likelihood, prior):
    from utils import normalize

    posterior = prior * likelihood
    normalize(posterior)
    return (normalize,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The following function encapsulates these steps.
    It takes a joint prior distribution and the data, and returns a joint posterior distribution.
    """)
    return


@app.cell
def _(normalize, np, weibull_dist):
    def update_weibull(prior, data):
        """Update the prior based on data."""
        lam_mesh, k_mesh, data_mesh = np.meshgrid(
            prior.columns, prior.index, data)
    
        densities = weibull_dist(lam_mesh, k_mesh).pdf(data_mesh)
        likelihood = densities.prod(axis=2)

        posterior = prior * likelihood
        normalize(posterior)

        return posterior

    return (update_weibull,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Here's how we use it.
    """)
    return


@app.cell
def _(data, prior, update_weibull):
    posterior_1 = update_weibull(prior, data)
    return (posterior_1,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    And here's a contour plot of the joint posterior distribution.
    """)
    return


@app.cell
def _(decorate, posterior_1):
    from utils import plot_contour
    plot_contour(posterior_1)
    decorate(title='Posterior joint distribution of Weibull parameters')
    return (plot_contour,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    It looks like the range of likely values for $\lambda$ is about 1 to 4, which contains the actual value we used to generate the data, 3.
    And the range for $k$ is about 0.5 to 1.5, which contains the actual value, 0.8.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Marginal Distributions

    To be more precise about these ranges, we can extract the marginal distributions:
    """)
    return


@app.cell
def _(posterior_1):
    from utils import marginal
    posterior_lam = marginal(posterior_1, 0)
    posterior_k = marginal(posterior_1, 1)
    return marginal, posterior_k, posterior_lam


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    And compute the posterior means and 90% credible intervals.
    """)
    return


@app.cell
def _(decorate, posterior_lam):
    import matplotlib.pyplot as plt

    plt.axvline(3, color='C5')
    posterior_lam.plot(color='C4', label='lambda')
    decorate(xlabel='lam',
             ylabel='PDF', 
             title='Posterior marginal distribution of lam')
    return (plt,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The vertical gray line show the actual value of $\lambda$.

    Here's the marginal posterior distribution for $k$.
    """)
    return


@app.cell
def _(decorate, plt, posterior_k):
    plt.axvline(0.8, color='C5')
    posterior_k.plot(color='C12', label='k')
    decorate(xlabel='k',
             ylabel='PDF', 
             title='Posterior marginal distribution of k')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The posterior distributions are wide, which means that with only 10 data points we can't estimated the parameters precisely.
    But for both parameters, the actual value falls in the credible interval.
    """)
    return


@app.cell
def _(lam, posterior_lam):
    print(lam, posterior_lam.credible_interval(0.9))
    return


@app.cell
def _(k, posterior_k):
    print(k, posterior_k.credible_interval(0.9))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Incomplete Data

    In the previous example we were given 10 random values from a Weibull distribution, and we used them to estimate the parameters (which we pretended we didn't know).

    But in many real-world scenarios, we don't have complete data; in particular, when we observe a system at a point in time, we generally have information about the past, but not the future.

    As an example, suppose you work at a dog shelter and you are interested in the time between the arrival of a new dog and when it is adopted.
    Some dogs might be snapped up immediately; others might have to wait longer.
    The people who operate the shelter might want to make inferences about the distribution of these residence times.

    Suppose you monitor arrivals and departures over 8 weeks and 10 dogs arrive during that interval.
    I'll assume that their arrival times are distributed uniformly, so I'll generate random values like this.
    """)
    return


@app.cell
def _(np):
    np.random.seed(19)
    return


@app.cell
def _(np):
    start = np.random.uniform(0, 8, size=10)
    start
    return (start,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Now let's suppose that the residence times follow the Weibull distribution we used in the previous example.
    We can generate a sample from that distribution like this:
    """)
    return


@app.cell
def _(np):
    np.random.seed(17)
    return


@app.cell
def _(actual_dist):
    duration = actual_dist.rvs(10)
    duration
    return (duration,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    I'll use these values to construct a `DataFrame` that contains the arrival and departure times for each dog, called `start` and `end`.
    """)
    return


@app.cell
def _(duration, start):
    import pandas as pd

    d = dict(start=start, end=start+duration)
    obs = pd.DataFrame(d)
    return obs, pd


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    For display purposes, I'll sort the rows of the `DataFrame` by arrival time.
    """)
    return


@app.cell
def _(obs):
    obs_1 = obs.sort_values(by='start', ignore_index=True)
    obs_1
    return (obs_1,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Notice that several of the lifelines extend past the observation window of 8 weeks.
    So if we observed this system at the beginning of Week 8, we would have incomplete information.
    Specifically, we would not know the future adoption times for Dogs 6, 7, and 8.

    I'll simulate this incomplete data by identifying the lifelines that extend past the observation window:
    """)
    return


@app.cell
def _(obs_1):
    censored = obs_1['end'] > 8
    return (censored,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    `censored` is a  Boolean Series that is `True` for lifelines that extend past Week 8.

    Data that is not available is sometimes called "censored" in the sense that it is hidden from us.
    But in this case it is hidden because we don't know the future, not because someone is censoring it.

    For the lifelines that are censored, I'll modify `end` to indicate when they are last observed and `status` to indicate that the observation is incomplete.
    """)
    return


@app.cell
def _(censored, obs_1):
    obs_1.loc[censored, 'end'] = 8
    obs_1.loc[censored, 'status'] = 0
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Now we can plot a "lifeline" for each dog, showing the arrival and departure times on a time line.
    """)
    return


@app.cell
def _(decorate, plt):
    def plot_lifelines(obs):
        """Plot a line for each observation.
    
        obs: DataFrame
        """
        for y, row in obs.iterrows():
            start = row['start']
            end = row['end']
            status = row['status']
        
            if status == 0:
                # ongoing
                plt.hlines(y, start, end, color='C0')
            else:
                # complete
                plt.hlines(y, start, end, color='C1')
                plt.plot(end, y, marker='o', color='C1')
            
        decorate(xlabel='Time (weeks)',
                 ylabel='Dog index',
                 title='Lifelines showing censored and uncensored observations')

        plt.gca().invert_yaxis()

    return (plot_lifelines,)


@app.cell
def _(obs_1, plot_lifelines):
    plot_lifelines(obs_1)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    And I'll add one more column to the table, which contains the duration of the observed parts of the lifelines.
    """)
    return


@app.cell
def _(obs_1):
    obs_1['T'] = obs_1['end'] - obs_1['start']
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    What we have simulated is the data that would be available at the beginning of Week 8.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Using Incomplete Data

    Now, let's see how we can use both kinds of data, complete and incomplete, to infer the parameters of the distribution of residence times.

    First I'll split the data into two sets: `data1` contains residence times for dogs whose arrival and departure times are known; `data2` contains incomplete residence times for dogs who were not adopted during the observation interval.
    """)
    return


@app.cell
def _(censored, obs_1):
    data1 = obs_1.loc[~censored, 'T']
    data2 = obs_1.loc[censored, 'T']
    return data1, data2


@app.cell
def _(data1):
    data1
    return


@app.cell
def _(data2):
    data2
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    For the complete data, we can use `update_weibull`, which uses the PDF of the Weibull distribution to compute the likelihood of the data.
    """)
    return


@app.cell
def _(data1, prior, update_weibull):
    posterior1 = update_weibull(prior, data1)
    return (posterior1,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    For the incomplete data, we have to think a little harder.
    At the end of the observation interval, we don't know what the residence time will be, but we can put a lower bound on it; that is, we can say that the residence time will be greater than `T`.

    And that means that we can compute the likelihood of the data using the survival function, which is the probability that a value from the distribution exceeds `T`.

    The following function is identical to `update_weibull` except that it uses `sf`, which computes the survival function, rather than `pdf`.
    """)
    return


@app.cell
def _(normalize, np, weibull_dist):
    def update_weibull_incomplete(prior, data):
        """Update the prior using incomplete data."""
        lam_mesh, k_mesh, data_mesh = np.meshgrid(
            prior.columns, prior.index, data)
    
        # evaluate the survival function
        probs = weibull_dist(lam_mesh, k_mesh).sf(data_mesh)
        likelihood = probs.prod(axis=2)

        posterior = prior * likelihood
        normalize(posterior)

        return posterior

    return (update_weibull_incomplete,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Here's the update with the incomplete data.
    """)
    return


@app.cell
def _(data2, posterior1, update_weibull_incomplete):
    posterior2 = update_weibull_incomplete(posterior1, data2)
    return (posterior2,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    And here's what the joint posterior distribution looks like after both updates.
    """)
    return


@app.cell
def _(decorate, plot_contour, posterior2):
    plot_contour(posterior2)
    decorate(title='Posterior joint distribution, incomplete data')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Compared to the previous contour plot, it looks like the range of likely values for $\lambda$ is substantially wider.
    We can see that more clearly by looking at the marginal distributions.
    """)
    return


@app.cell
def _(marginal, posterior2):
    posterior_lam2 = marginal(posterior2, 0)
    posterior_k2 = marginal(posterior2, 1)
    return posterior_k2, posterior_lam2


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Here's the posterior marginal distribution for $\lambda$ compared to the distribution we got using all complete data.
    """)
    return


@app.cell
def _(decorate, posterior_lam, posterior_lam2):
    posterior_lam.plot(color='C5', label='All complete',
                       linestyle='dashed')
    posterior_lam2.plot(color='C2', label='Some censored')

    decorate(xlabel='lambda',
             ylabel='PDF', 
             title='Marginal posterior distribution of lambda')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The distribution with some incomplete data is substantially wider.

    As an aside, notice that the posterior distribution does not come all the way to 0 on the right side.
    That suggests that the range of the prior distribution is not wide enough to cover the most likely values for this parameter.
    If I were concerned about making this distribution more accurate, I would go back and run the update again with a wider prior.

    Here's the posterior marginal distribution for $k$:
    """)
    return


@app.cell
def _(decorate, posterior_k, posterior_k2):
    posterior_k.plot(color='C5', label='All complete',
                       linestyle='dashed')
    posterior_k2.plot(color='C12', label='Some censored')

    decorate(xlabel='k',
             ylabel='PDF', 
             title='Posterior marginal distribution of k')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    In this example, the marginal distribution is shifted to the left when we have incomplete data, but it is not substantially wider.

    In summary, we have seen how to combine complete and incomplete data to estimate the parameters of a Weibull distribution, which is useful in many real-world scenarios where some of the data are censored.

    In general, the posterior distributions are wider when we have incomplete data, because less information leads to more uncertainty.

    This example is based on data I generated; in the next section we'll do a similar analysis with real data.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Light Bulbs

    In 2007 [researchers ran an experiment](https://www.researchgate.net/publication/225450325_Renewal_Rate_of_Filament_Lamps_Theory_and_Experiment) to characterize the distribution of lifetimes for light bulbs.
    Here is their description of the experiment:

    > An assembly of 50 new Philips (India) lamps with the rating 40 W, 220 V (AC) was taken and installed in the horizontal orientation and uniformly distributed over a lab area 11 m x 7 m.
    >
    > The assembly was monitored at regular intervals of 12 h to look for failures. The instants of recorded failures were [recorded] and a total of 32 data points were obtained such that even the last bulb failed.
    """)
    return


@app.cell
def _(download):
    download('https://gist.github.com/epogrebnyak/7933e16c0ad215742c4c104be4fbdeb1/raw/c932bc5b6aa6317770c4cbf43eb591511fec08f9/lamps.csv')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We can load the data into a `DataFrame` like this:
    """)
    return


@app.cell
def _(pd):
    df = pd.read_csv('lamps.csv', index_col=0)
    df.head()
    return (df,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Column `h` contains the times when bulbs failed in hours; Column `f` contains the number of bulbs that failed at each time.
    We can represent these values and frequencies using a `Pmf`, like this:
    """)
    return


@app.cell
def _(df):
    from empiricaldist import Pmf

    pmf_bulb = Pmf(df['f'].to_numpy(), df['h'])
    pmf_bulb.normalize()
    return (pmf_bulb,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Because of the design of this experiment, we can consider the data to be a representative sample from the distribution of lifetimes, at least for light bulbs that are lit continuously.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The average lifetime is about 1400 h.
    """)
    return


@app.cell
def _(pmf_bulb):
    pmf_bulb.mean()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Assuming that these data are well modeled by a Weibull distribution, let's estimate the parameters that fit the data.
    Again, I'll start with uniform priors for $\lambda$ and $k$:
    """)
    return


@app.cell
def _(make_uniform, np):
    _lams = np.linspace(1000, 2000, num=51)
    prior_lam_1 = make_uniform(_lams, name='lambda')
    return (prior_lam_1,)


@app.cell
def _(make_uniform, np):
    _ks = np.linspace(1, 10, num=51)
    prior_k_1 = make_uniform(_ks, name='k')
    return (prior_k_1,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    For this example, there are 51 values in the prior distribution, rather than the usual 101.  That's because we are going to use the posterior distributions to do some computationally-intensive calculations.
    They will run faster with fewer values, but the results will be less precise.

    As usual, we can use `make_joint` to make the prior joint distribution.
    """)
    return


@app.cell
def _(make_joint, prior_k_1, prior_lam_1):
    prior_bulb = make_joint(prior_lam_1, prior_k_1)
    return (prior_bulb,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Although we have data for 50 light bulbs, there are only 32 unique lifetimes in the dataset.  For the update, it is convenient to express the data in the form of 50 lifetimes, with each lifetime repeated the given number of times.
    We can use `np.repeat` to transform the data.
    """)
    return


@app.cell
def _(df, np):
    data_bulb = np.repeat(df['h'], df['f'])
    len(data_bulb)
    return (data_bulb,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Now we can use `update_weibull` to do the update.
    """)
    return


@app.cell
def _(data_bulb, prior_bulb, update_weibull):
    posterior_bulb = update_weibull(prior_bulb, data_bulb)
    return (posterior_bulb,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Here's what the posterior joint distribution looks like:
    """)
    return


@app.cell
def _(decorate, plot_contour, posterior_bulb):
    plot_contour(posterior_bulb)
    decorate(title='Joint posterior distribution, light bulbs')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    To summarize this joint posterior distribution, we'll compute the posterior mean lifetime.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Posterior Means

    To compute the posterior mean of a joint distribution, we'll make a mesh that contains the values of $\lambda$ and $k$.
    """)
    return


@app.cell
def _(np, prior_bulb):
    lam_mesh_1, k_mesh_1 = np.meshgrid(prior_bulb.columns, prior_bulb.index)
    return k_mesh_1, lam_mesh_1


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Now for each pair of parameters we'll use `weibull_dist` to compute the mean.
    """)
    return


@app.cell
def _(k_mesh_1, lam_mesh_1, weibull_dist):
    means = weibull_dist(lam_mesh_1, k_mesh_1).mean()
    means.shape
    return (means,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The result is an array with the same dimensions as the joint distribution.

    Now we need to weight each mean with the corresponding probability from the joint posterior.
    """)
    return


@app.cell
def _(means, posterior_bulb):
    prod = means * posterior_bulb
    return (prod,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Finally we compute the sum of the weighted means.
    """)
    return


@app.cell
def _(prod):
    prod.to_numpy().sum()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Based on the posterior distribution, we think the mean lifetime is about 1413 hours.

    The following function encapsulates these steps:
    """)
    return


@app.cell
def _(np, weibull_dist):
    def joint_weibull_mean(joint):
        """Compute the mean of a joint distribution of Weibulls."""
        lam_mesh, k_mesh = np.meshgrid(
            joint.columns, joint.index)
        means = weibull_dist(lam_mesh, k_mesh).mean()
        prod = means * joint
        return prod.to_numpy().sum()

    return (joint_weibull_mean,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Incomplete Information

    The previous update was not quite right, because it assumed each light bulb died at the instant we observed it.
    According to the report, the researchers only checked the bulbs every 12 hours.  So if they see that a bulb has died, they know only that it died during the 12 hours since the last check.

    It is more strictly correct to use the following update function, which uses the CDF of the Weibull distribution to compute the probability that a bulb dies during a given 12 hour interval.
    """)
    return


@app.cell
def _(normalize, np, weibull_dist):
    def update_weibull_between(prior, data, dt=12):
        """Update the prior based on data."""
        lam_mesh, k_mesh, data_mesh = np.meshgrid(
            prior.columns, prior.index, data)
        dist = weibull_dist(lam_mesh, k_mesh)
        cdf1 = dist.cdf(data_mesh)
        cdf2 = dist.cdf(data_mesh-12)
        likelihood = (cdf1 - cdf2).prod(axis=2)

        posterior = prior * likelihood
        normalize(posterior)

        return posterior

    return (update_weibull_between,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The probability that a value falls in an interval is the difference between the CDF at the beginning and end of the interval.

    Here's how we run the update.
    """)
    return


@app.cell
def _(data_bulb, prior_bulb, update_weibull_between):
    posterior_bulb2 = update_weibull_between(prior_bulb, data_bulb)
    return (posterior_bulb2,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    And here are the results.
    """)
    return


@app.cell
def _(decorate, plot_contour, posterior_bulb2):
    plot_contour(posterior_bulb2)
    decorate(title='Joint posterior distribution, light bulbs')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Visually this result is almost identical to what we got using the PDF.
    And that's good news, because it suggests that using the PDF can be a good approximation even if it's not strictly correct.

    To see whether it makes any difference at all, let's check the posterior means.
    """)
    return


@app.cell
def _(joint_weibull_mean, posterior_bulb):
    joint_weibull_mean(posterior_bulb)
    return


@app.cell
def _(joint_weibull_mean, posterior_bulb2):
    joint_weibull_mean(posterior_bulb2)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    When we take into account the 12-hour interval between observations, the posterior mean is about 6 hours less.
    And that makes sense: if we assume that a bulb is equally likely to expire at any point in the interval, the average would be the midpoint of the interval.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Posterior Predictive Distribution

    Suppose you install 100 light bulbs of the kind in the previous section, and you come back to check on them after 1000 hours.  Based on the posterior distribution we just computed, what is the distribution of the number of bulbs you find dead?

    If we knew the parameters of the Weibull distribution for sure, the answer would be a binomial distribution.

    For example, if we know that $\lambda=1550$ and $k=4.25$, we can use `weibull_dist` to compute the probability that a bulb dies before you return:
    """)
    return


@app.cell
def _(weibull_dist):
    lam_1 = 1550
    k_1 = 4.25
    t = 1000
    prob_dead = weibull_dist(lam_1, k_1).cdf(t)
    prob_dead
    return prob_dead, t


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    If there are 100 bulbs and each has this probability of dying, the number of dead bulbs follows a binomial distribution.
    """)
    return


@app.cell
def _(prob_dead):
    from utils import make_binomial

    n = 100
    p = prob_dead
    dist_num_dead = make_binomial(n, p)
    return dist_num_dead, make_binomial, n


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    And here's what it looks like.
    """)
    return


@app.cell
def _(decorate, dist_num_dead):
    dist_num_dead.plot(label='known parameters')

    decorate(xlabel='Number of dead bulbs',
             ylabel='PMF',
             title='Predictive distribution with known parameters')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    But that's based on the assumption that we know $\lambda$ and $k$, and we don't.
    Instead, we have a posterior distribution that contains possible values of these parameters and their probabilities.

    So the posterior predictive distribution is not a single binomial; instead it is a mixture of binomials, weighted with the posterior probabilities.

    We can use `make_mixture` to compute the posterior predictive distribution.
    It doesn't work with joint distributions, but we can convert the `DataFrame` that represents a joint distribution to a `Series`, like this:
    """)
    return


@app.cell
def _(posterior_bulb):
    posterior_series = posterior_bulb.stack()
    posterior_series.head()
    return (posterior_series,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The result is a `Series` with a `MultiIndex` that contains two "levels": the first level contains the values of `k`; the second contains the values of `lam`.

    With the posterior in this form, we can iterate through the possible parameters and compute a predictive distribution for each pair.
    """)
    return


@app.cell
def _(make_binomial, n, posterior_series, t, weibull_dist):
    pmf_seq = []
    for k_2, lam_2 in posterior_series.index:
        prob_dead_1 = weibull_dist(lam_2, k_2).cdf(t)
        pmf = make_binomial(n, prob_dead_1)
        pmf_seq.append(pmf)
    return (pmf_seq,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Now we can use `make_mixture`, passing as parameters the posterior probabilities in `posterior_series` and the sequence of binomial distributions in `pmf_seq`.
    """)
    return


@app.cell
def _(pmf_seq, posterior_series):
    from utils import make_mixture

    post_pred = make_mixture(posterior_series, pmf_seq)
    return (post_pred,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Here's what the posterior predictive distribution looks like, compared to the binomial distribution we computed with known parameters.
    """)
    return


@app.cell
def _(decorate, dist_num_dead, post_pred):
    dist_num_dead.plot(label='known parameters')
    post_pred.plot(label='unknown parameters')
    decorate(xlabel='Number of dead bulbs',
             ylabel='PMF',
             title='Posterior predictive distribution')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The posterior predictive distribution is wider because it represents our uncertainty about the parameters as well as our uncertainty about the number of dead bulbs.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Summary

    This chapter introduces survival analysis, which is used to answer questions about the time until an event, and the Weibull distribution, which is a good model for "lifetimes" (broadly interpreted) in a number of domains.

    We used joint distributions to represent prior probabilities for the parameters of the Weibull distribution, and we updated them three ways: knowing the exact duration of a lifetime, knowing a lower bound, and knowing that a lifetime fell in a given interval.

    These examples demonstrate a feature of Bayesian methods: they can be adapted to handle incomplete, or "censored", data with only small changes.  As an exercise, you'll have a chance to work with one more type of censored data, when we are given an upper bound on a lifetime.

    The methods in this chapter work with any distribution with two parameters.
    In the exercises, you'll have a chance to estimate the parameters of a two-parameter gamma distribution, which is used to describe a variety of natural phenomena.

    And in the next chapter we'll move on to models with three parameters!
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
    **Exercise:** Using data about the lifetimes of light bulbs, we computed the posterior distribution from the parameters of a Weibull distribution, $\lambda$ and $k$, and the posterior predictive distribution for the number of dead bulbs, out of 100, after 1000 hours.

    Now suppose you do the experiment:  You install 100 light bulbs, come back after 1000 hours, and find 20 dead light bulbs.
    Update the posterior distribution based on this data.
    How much does it change the posterior mean?
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Suggestions:

    1. Use a mesh grid to compute the probability of finding a bulb dead after 1000 hours for each pair of parameters.

    2. For each of those probabilities, compute the likelihood of finding 20 dead bulbs out of 100.

    3. Use those likelihoods to update the posterior distribution.
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


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Exercise:** In this exercise, we'll use one month of data to estimate the parameters of a distribution that describes daily rainfall in Seattle.
    Then we'll compute the posterior predictive distribution for daily rainfall and use it to estimate the probability of a rare event, like more than 1.5 inches of rain in a day.

    According to hydrologists, the distribution of total daily rainfall (for days with rain) is well modeled by a two-parameter
    gamma distribution.

    When we worked with the one-parameter gamma distribution in <<_TheGammaDistribution>>, we used the Greek letter $\alpha$ for the parameter.

    For the two-parameter gamma distribution, we will use $k$ for the "shape parameter", which determines the shape of the distribution, and the Greek letter $\theta$ or `theta` for the "scale parameter".
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The following function takes these parameters and returns a `gamma` object from SciPy.
    """)
    return


@app.cell
def _():
    import scipy.stats

    def gamma_dist(k, theta):
        """Makes a gamma object.
    
        k: shape parameter
        theta: scale parameter
    
        returns: gamma object
        """
        return scipy.stats.gamma(k, scale=theta)

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Now we need some data.
    The following cell downloads data I collected from the National Oceanic and Atmospheric Administration ([NOAA](http://www.ncdc.noaa.gov/cdo-web/search)) for Seattle, Washington in May 2020.
    """)
    return


@app.cell
def _(download):
    # Load the data file

    download('https://github.com/AllenDowney/ThinkBayes2/raw/master/data/2203951.csv')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Now we can load it into a `DataFrame`:
    """)
    return


@app.cell
def _(pd):
    weather = pd.read_csv('2203951.csv')
    weather.head()
    return (weather,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    I'll make a Boolean Series to indicate which days it rained.
    """)
    return


@app.cell
def _(weather):
    rained = weather['PRCP'] > 0
    rained.sum()
    return (rained,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    And select the total rainfall on the days it rained.
    """)
    return


@app.cell
def _(rained, weather):
    prcp = weather.loc[rained, 'PRCP']
    prcp.describe()
    return (prcp,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Here's what the CDF of the data looks like.
    """)
    return


@app.cell
def _(Cdf, decorate, prcp):
    cdf_data = Cdf.from_seq(prcp)
    cdf_data.plot()
    decorate(xlabel='Total rainfall (in)',
             ylabel='CDF',
             title='Distribution of rainfall on days it rained')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The maximum is 1.14 inches of rain is one day.
    To estimate the probability of more than 1.5 inches, we need to extrapolate from the data we have, so our estimate will depend on whether the gamma distribution is really a good model.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    I suggest you proceed in the following steps:

    1. Construct a prior distribution for the parameters of the gamma distribution.  Note that $k$ and $\theta$ must be greater than 0.

    2. Use the observed rainfalls to update the distribution of parameters.

    3. Compute the posterior predictive distribution of rainfall, and use it to estimate the probability of getting more than 1.5 inches of rain in one day.
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
