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
    # Conjugate Priors
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
    return


@app.cell
def _():
    from utils import set_pyplot_params
    set_pyplot_params()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    In the previous chapters we have used grid approximations to solve a variety of problems.
    One of my goals has been to show that this approach is sufficient to solve many real-world problems.
    And I think it's a good place to start because it shows clearly how the methods work.

    However, as we saw in the previous chapter, grid methods will only get you so far.
    As we increase the number of parameters, the number of points in the grid grows (literally) exponentially.
    With more than 3-4 parameters, grid methods become impractical.

    So, in the remaining three chapters, I will present three alternatives:

    1. In this chapter we'll use **conjugate priors** to speed up some of the computations we've already done.

    2. In the next chapter, I'll present Markov chain Monte Carlo (MCMC) methods, which can solve problems with tens of parameters, or even hundreds, in a reasonable amount of time.

    3. And in the last chapter we'll use Approximate Bayesian Computation (ABC) for problems that are hard to model with simple distributions.

    We'll start with the World Cup problem.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## The World Cup Problem Revisited

    In <<_PoissonProcesses>>, we solved the World Cup problem using a Poisson process to model goals in a soccer game as random events that are equally likely to occur at any point during a game.

    We used a gamma distribution to represent the prior distribution of $\lambda$, the goal-scoring rate.  And we used a Poisson distribution to compute the probability of $k$, the number of goals scored.

    Here's a gamma object that represents the prior distribution.
    """)
    return


@app.cell
def _():
    from scipy.stats import gamma

    alpha = 1.4
    dist = gamma(alpha)
    return dist, gamma


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    And here's a grid approximation.
    """)
    return


@app.cell
def _(dist):
    import numpy as np
    from utils import pmf_from_dist

    lams = np.linspace(0, 10, 101)
    prior = pmf_from_dist(dist, lams)
    return lams, np, pmf_from_dist, prior


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Here's the likelihood of scoring 4 goals for each possible value of `lam`.
    """)
    return


@app.cell
def _(lams):
    from scipy.stats import poisson
    _k = 4
    likelihood = poisson(lams).pmf(_k)
    return (likelihood,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    And here's the update.
    """)
    return


@app.cell
def _(likelihood, prior):
    posterior = prior * likelihood
    posterior.normalize()
    return (posterior,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    So far, this should be familiar.
    Now we'll solve the same problem using the conjugate prior.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## The Conjugate Prior

    In <<_TheGammaDistribution>>, I presented three reasons to use a gamma distribution for the prior and said there was a fourth reason I would reveal later.
    Well, now is the time.

    The other reason I chose the gamma distribution is that it is the "conjugate prior" of the Poisson distribution, so-called because the two distributions are connected or coupled, which is what "conjugate" means.

    In the next section I'll explain *how* they are connected, but first I'll show you the consequence of this connection, which is that there is a remarkably simple way to compute the posterior distribution.

    However, in order to demonstrate it, we have to switch from the one-parameter version of the gamma distribution to the two-parameter version.  Since the first parameter is called `alpha`, you might guess that the second parameter is called `beta`.

    The following function takes `alpha` and `beta` and makes an object that represents a gamma distribution with those parameters.
    """)
    return


@app.cell
def _(gamma):
    def make_gamma_dist(alpha, beta):
        """Makes a gamma object."""
        dist = gamma(alpha, scale=1/beta)
        dist.alpha = alpha
        dist.beta = beta
        return dist

    return (make_gamma_dist,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Here's the prior distribution with `alpha=1.4` again and `beta=1`.
    """)
    return


@app.cell
def _(make_gamma_dist):
    alpha_1 = 1.4
    _beta = 1
    prior_gamma = make_gamma_dist(alpha_1, _beta)
    prior_gamma.mean()
    return (prior_gamma,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Now I claim without proof that we can do a Bayesian update with `k` goals just by making a gamma distribution with parameters `alpha+k` and `beta+1`.
    """)
    return


@app.cell
def _(make_gamma_dist):
    def update_gamma(prior, data):
        """Update a gamma prior."""
        k, t = data
        alpha = prior.alpha + k
        beta = prior.beta + t
        return make_gamma_dist(alpha, beta)

    return (update_gamma,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Here's how we update it with `k=4` goals in `t=1` game.
    """)
    return


@app.cell
def _(prior_gamma, update_gamma):
    _data = (4, 1)
    posterior_gamma = update_gamma(prior_gamma, _data)
    return (posterior_gamma,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    After all the work we did with the grid, it might seem absurd that we can do a Bayesian update by adding two pairs of numbers.
    So let's confirm that it works.

    I'll make a `Pmf` with a discrete approximation of the posterior distribution.
    """)
    return


@app.cell
def _(lams, pmf_from_dist, posterior_gamma):
    posterior_conjugate = pmf_from_dist(posterior_gamma, lams)
    return (posterior_conjugate,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The following figure shows the result along with the posterior we computed using the grid algorithm.
    """)
    return


@app.cell
def _():
    from utils import decorate

    def decorate_rate(title=''):
        decorate(xlabel='Goal scoring rate (lam)',
                 ylabel='PMF',
                 title=title)

    return decorate, decorate_rate


@app.cell
def _(decorate_rate, posterior, posterior_conjugate):
    posterior.plot(label='grid posterior', color='C1')
    posterior_conjugate.plot(label='conjugate posterior', 
                             color='C4', ls=':')

    decorate_rate('Posterior distribution')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    They are the same other than small differences due to floating-point approximations.
    """)
    return


@app.cell
def _(np, posterior, posterior_conjugate):
    np.allclose(posterior, posterior_conjugate)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## What the Actual?

    To understand how that works, we'll write the PDF of the gamma prior and the PMF of the Poisson likelihood, then multiply them together, because that's what the Bayesian update does.
    We'll see that the result is a gamma distribution, and we'll derive its parameters.

    Here's the PDF of the gamma prior, which is the probability density for each value of $\lambda$, given parameters $\alpha$ and $\beta$:

    $$\lambda^{\alpha-1} e^{-\lambda \beta}$$

    I have omitted the normalizing factor; since we are planning to normalize the posterior distribution anyway, we don't really need it.

    Now suppose a team scores $k$ goals in $t$ games.
    The probability of this data is given by the PMF of the Poisson distribution, which is a function of $k$ with $\lambda$ and $t$ as parameters.

    $$\lambda^k e^{-\lambda t}$$

    Again, I have omitted the normalizing factor, which makes it clearer that the gamma and Poisson distributions have the same functional form.
    When we multiply them together, we can pair up the factors and add up the exponents.
    The result is the unnormalized posterior distribution,

    $$\lambda^{\alpha-1+k} e^{-\lambda(\beta + t)}$$

    which we can recognize as an unnormalized gamma distribution with parameters $\alpha + k$ and $\beta + t$.

    This derivation provides insight into what the parameters of the posterior distribution mean: $\alpha$ reflects the number of events that have occurred; $\beta$ reflects the elapsed time.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Binomial Likelihood

    As a second example, let's look again at the Euro problem.
    When we solved it with a grid algorithm, we started with a uniform prior:
    """)
    return


@app.cell
def _(np):
    from utils import make_uniform

    xs = np.linspace(0, 1, 101)
    uniform = make_uniform(xs, 'uniform')
    return (uniform,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We used the binomial distribution to compute the likelihood of the data, which was 140 heads out of 250 attempts.
    """)
    return


@app.cell
def _(uniform):
    from scipy.stats import binom
    _k, _n = (140, 250)
    xs_1 = uniform.qs
    likelihood_1 = binom.pmf(_k, _n, xs_1)
    return binom, likelihood_1, xs_1


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Then we computed the posterior distribution in the usual way.
    """)
    return


@app.cell
def _(likelihood_1, uniform):
    posterior_1 = uniform * likelihood_1
    posterior_1.normalize()
    return (posterior_1,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We can solve this problem more efficiently using the conjugate prior of the binomial distribution, which is the beta distribution.

    The beta distribution is bounded between 0 and 1, so it works well for representing the distribution of a probability like `x`.
    It has two parameters, called `alpha` and `beta`, that determine the shape of the distribution.

    SciPy provides an object called `beta` that represents a beta distribution.
    The following function takes `alpha` and `beta` and returns a new `beta` object.
    """)
    return


@app.cell
def _():
    import scipy.stats

    def make_beta(alpha, beta):
        """Makes a beta object."""
        dist = scipy.stats.beta(alpha, beta)
        dist.alpha = alpha
        dist.beta = beta
        return dist

    return (make_beta,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    It turns out that the uniform distribution, which we used as a prior, is the beta distribution with parameters `alpha=1` and `beta=1`.
    So we can make a `beta` object that represents a uniform distribution, like this:
    """)
    return


@app.cell
def _(make_beta):
    alpha_2 = 1
    _beta = 1
    prior_beta = make_beta(alpha_2, _beta)
    return (prior_beta,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Now let's figure out how to do the update.  As in the previous example, we'll write the PDF of the prior distribution and the PMF of the likelihood function, and multiply them together.  We'll see that the product has the same form as the prior, and we'll derive its parameters.

    Here is the PDF of the beta distribution, which is a function of $x$ with $\alpha$ and $\beta$ as parameters.

    $$x^{\alpha-1} (1-x)^{\beta-1}$$

    Again, I have omitted the normalizing factor, which we don't need because we are going to normalize the distribution after the update.

    And here's the PMF of the binomial distribution, which is a function of $k$ with $n$ and $x$ as parameters.

    $$x^{k} (1-x)^{n-k}$$

    Again, I have omitted the normalizing factor.
    Now when we multiply the beta prior and the binomial likelihood, the result is

    $$x^{\alpha-1+k} (1-x)^{\beta-1+n-k}$$

    which we recognize as an unnormalized beta distribution with parameters $\alpha+k$ and $\beta+n-k$.

    So if we observe `k` successes in `n` trials, we can do the update by making a beta distribution with parameters `alpha+k` and `beta+n-k`.
    That's what this function does:
    """)
    return


@app.cell
def _(make_beta):
    def update_beta(prior, data):
        """Update a beta distribution."""
        k, n = data
        alpha = prior.alpha + k
        beta = prior.beta + n - k
        return make_beta(alpha, beta)

    return (update_beta,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Again, the conjugate prior gives us insight into the meaning of the parameters; $\alpha$ is related to the number of observed successes; $\beta$ is related to the number of failures.

    Here's how we do the update with the observed data.
    """)
    return


@app.cell
def _(prior_beta, update_beta):
    _data = (140, 250)
    posterior_beta = update_beta(prior_beta, _data)
    return (posterior_beta,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    To confirm that it works, I'll evaluate the posterior distribution for the possible values of `xs` and put the results in a `Pmf`.
    """)
    return


@app.cell
def _(pmf_from_dist, posterior_beta, xs_1):
    posterior_conjugate_1 = pmf_from_dist(posterior_beta, xs_1)
    return (posterior_conjugate_1,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    And we can compare the posterior distribution we just computed with the results from the grid algorithm.
    """)
    return


@app.cell
def _(decorate):
    def decorate_euro(title):
        decorate(xlabel='Proportion of heads (x)',
                 ylabel='Probability',
                 title=title)

    return (decorate_euro,)


@app.cell
def _(decorate_euro, posterior_1, posterior_conjugate_1):
    posterior_1.plot(label='grid posterior', color='C1')
    posterior_conjugate_1.plot(label='conjugate posterior', color='C4', ls=':')
    decorate_euro(title='Posterior distribution of x')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    They are the same other than small differences due to floating-point approximations.

    The examples so far are problems we have already solved, so let's try something new.
    """)
    return


@app.cell
def _(np, posterior_1, posterior_conjugate_1):
    np.allclose(posterior_1, posterior_conjugate_1)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Lions and Tigers and Bears

    Suppose we visit a wild animal preserve where we know that the only animals are lions and tigers and bears, but we don't know how many of each there are.
    During the tour, we see 3 lions, 2 tigers, and one bear. Assuming that every animal had an equal chance to appear in our sample, what is the probability that the next animal we see is a bear?

    To answer this question, we'll use the data to estimate the prevalence of each species, that is, what fraction of the animals belong to each species.
    If we know the prevalences, we can use the multinomial distribution to compute the probability of the data.
    For example, suppose we know that the fraction of lions, tigers, and bears is 0.4, 0.3, and 0.3, respectively.

    In that case the probability of the data is:
    """)
    return


@app.cell
def _(np):
    from scipy.stats import multinomial
    _data = (3, 2, 1)
    _n = np.sum(_data)
    ps = (0.4, 0.3, 0.3)
    multinomial.pmf(_data, _n, ps)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Now, we could choose a prior for the prevalences and do a Bayesian update using the multinomial distribution to compute the probability of the data.

    But there's an easier way, because the multinomial distribution has a conjugate prior: the Dirichlet distribution.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## The Dirichlet Distribution

    The Dirichlet distribution is a multivariate distribution, like the multivariate normal distribution we used in <<_MultivariateNormalDistribution>> to describe the distribution of penguin measurements.

    In that example, the quantities in the distribution are pairs of flipper length and culmen length, and the parameters of the distribution are a vector of means and a matrix of covariances.

    In a Dirichlet distribution, the quantities are vectors of probabilities, $\mathbf{x}$, and the parameter is a vector, $\mathbf{\alpha}$.

    An example will make that clearer.  SciPy provides a `dirichlet` object that represents a Dirichlet distribution.
    Here's an instance with $\mathbf{\alpha} = 1, 2, 3$.
    """)
    return


@app.cell
def _():
    from scipy.stats import dirichlet
    alpha_3 = (1, 2, 3)
    dist_1 = dirichlet(alpha_3)
    return alpha_3, dist_1


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Since we provided three parameters, the result is a distribution of three variables.
    If we draw a random value from this distribution, like this:
    """)
    return


@app.cell
def _(dist_1):
    dist_1.rvs()
    return


@app.cell
def _(dist_1):
    dist_1.rvs().sum()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The result is an array of three values.
    They are bounded between 0 and 1, and they always add up to 1, so they can be interpreted as the probabilities of a set of outcomes that are mutually exclusive and collectively exhaustive.

    Let's see what the distributions of these values look like.  I'll draw 1000 random vectors from this distribution, like this:
    """)
    return


@app.cell
def _(dist_1):
    sample = dist_1.rvs(1000)
    return (sample,)


@app.cell
def _(sample):
    sample.shape
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The result is an array with 1000 rows and three columns.  I'll compute the `Cdf` of the values in each column.
    """)
    return


@app.cell
def _(sample):
    from empiricaldist import Cdf

    cdfs = [Cdf.from_seq(col) 
            for col in sample.transpose()]
    return (cdfs,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The result is a list of `Cdf` objects that represent the marginal distributions of the three variables.  Here's what they look like.
    """)
    return


@app.cell
def _(cdfs, decorate):
    for _i, _cdf in enumerate(cdfs):
        _label = f'Column {_i}'
        _cdf.plot(label=_label)
    decorate()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Column 0, which corresponds to the lowest parameter, contains the lowest probabilities.
    Column 2, which corresponds to the highest parameter, contains the highest probabilities.

    As it turns out, these marginal distributions are beta distributions.
    The following function takes a sequence of parameters, `alpha`, and computes the marginal distribution of variable `i`:
    """)
    return


@app.cell
def _(make_beta, np):
    def marginal_beta(alpha, i):
        """Compute the ith marginal of a Dirichlet distribution."""
        total = np.sum(alpha)
        return make_beta(alpha[i], total-alpha[i])

    return (marginal_beta,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We can use it to compute the marginal distribution for the three variables.
    """)
    return


@app.cell
def _(alpha_3, marginal_beta):
    marginals = [marginal_beta(alpha_3, i) for i in range(len(alpha_3))]
    return (marginals,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The following plot shows the CDF of these distributions as gray lines and compares them to the CDFs of the samples.
    """)
    return


@app.cell
def _(alpha_3, cdfs, decorate, marginals, np, pmf_from_dist):
    xs_2 = np.linspace(0, 1, 101)
    for _i in range(len(alpha_3)):
        _label = f'Column {_i}'
        pmf = pmf_from_dist(marginals[_i], xs_2)
        pmf.make_cdf().plot(color='C5')
        _cdf = cdfs[_i]
        _cdf.plot(label=_label, ls=':')
    decorate()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    This confirms that the marginals of the Dirichlet distribution are beta distributions.
    And that's useful because the Dirichlet distribution is the conjugate prior for the multinomial likelihood function.

    If the prior distribution is Dirichlet with parameter vector `alpha` and the data is a vector of observations, `data`, the posterior distribution is Dirichlet with parameter vector `alpha + data`.

    As an exercise at the end of this chapter, you can use this method to solve the Lions and Tigers and Bears problem.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Summary

    After reading this chapter, if you feel like you've been tricked, I understand.  It turns out that many of the problems in this book can be solved with just a few arithmetic operations.  So why did we go to all the trouble of using grid algorithms?

    Sadly, there are only a few problems we can solve with conjugate priors; in fact, this chapter includes most of the ones that are useful in practice.

    For the vast majority of problems, there is no conjugate prior and no shortcut to compute the posterior distribution.
    That's why we need grid algorithms and the methods in the next two chapters, Approximate Bayesian Computation (ABC) and Markov chain Monte Carlo methods (MCMC).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Exercises

    **Exercise:** In the second version of the World Cup problem, the data we use for the update is not the number of goals in a game, but the time until the first goal.
    So the probability of the data is given by the exponential distribution rather than the Poisson distribution.

    But it turns out that the gamma distribution is *also* the conjugate prior of the exponential distribution, so there is a simple way to compute this update, too.
    The PDF of the exponential distribution is a function of $t$ with $\lambda$ as a parameter.

    $$\lambda e^{-\lambda t}$$

    Multiply the PDF of the gamma prior by this likelihood, confirm that the result is an unnormalized gamma distribution, and see if you can derive its parameters.

    Write a few lines of code to update `prior_gamma` with the data from this version of the problem, which was a first goal after 11 minutes and a second goal after an additional 12 minutes.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Remember to express these quantities in units of games, which are approximately 90 minutes.
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
    **Exercise:** For problems like the Euro problem where the likelihood function is binomial, we can do a Bayesian update with just a few arithmetic operations, but only if the prior is a beta distribution.

    If we want a uniform prior, we can use a beta distribution with `alpha=1` and `beta=1`.
    But what can we do if the prior distribution we want is not a beta distribution?
    For example, in <<_TrianglePrior>> we also solved the Euro problem with a triangle prior, which is not a beta distribution.

    In these cases, we can often find a beta distribution that is a good-enough approximation for the prior we want.
    See if you can find a beta distribution that fits the triangle prior, then update it using `update_beta`.

    Use `pmf_from_dist` to make a `Pmf` that approximates the posterior distribution and compare it to the posterior we just computed using a grid algorithm.  How big is the largest difference between them?
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Here's the triangle prior again.
    """)
    return


@app.cell
def _(np, uniform):
    from empiricaldist import Pmf
    ramp_up = np.arange(50)
    ramp_down = np.arange(50, -1, -1)
    a = np.append(ramp_up, ramp_down)
    xs_3 = uniform.qs
    triangle = Pmf(a, xs_3, name='triangle')
    triangle.normalize()
    return triangle, xs_3


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    And here's the update.
    """)
    return


@app.cell
def _(binom, triangle, xs_3):
    _k, _n = (140, 250)
    likelihood_2 = binom.pmf(_k, _n, xs_3)
    posterior_2 = triangle * likelihood_2
    posterior_2.normalize()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    To get you started, here's the beta distribution that we used as a uniform prior.
    """)
    return


@app.cell
def _(make_beta):
    alpha_4 = 1
    _beta = 1
    prior_beta_1 = make_beta(alpha_4, _beta)
    prior_beta_1.mean()
    return (prior_beta_1,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    And here's what it looks like compared to the triangle prior.
    """)
    return


@app.cell
def _(decorate_euro, pmf_from_dist, prior_beta_1, triangle, xs_3):
    prior_pmf = pmf_from_dist(prior_beta_1, xs_3)
    triangle.plot(label='triangle')
    prior_pmf.plot(label='beta')
    decorate_euro('Prior distributions')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Now you take it from there.
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
    **Exercise:**  [3Blue1Brown](https://en.wikipedia.org/wiki/3Blue1Brown) is a YouTube channel about math; if you are not already aware of it, I recommend it highly.
    In [this video](https://www.youtube.com/watch?v=8idr1WZ1A7Q) the narrator presents this problem:

    > You are buying a product online and you see three sellers offering the same product at the same price.  One of them has a 100% positive rating, but with only 10 reviews.  Another has a 96% positive rating with 50 total reviews.  And yet another has a 93% positive rating, but with 200 total reviews.
    >
    >Which one should you buy from?

    Let's think about how to model this scenario.  Suppose each seller has some unknown probability, `x`, of providing satisfactory service and getting a positive rating, and we want to choose the seller with the highest value of `x`.

    This is not the only model for this scenario, and it is not necessarily the best.  An alternative would be something like item response theory, where sellers have varying ability to provide satisfactory service and customers have varying difficulty of being satisfied.

    But the first model has the virtue of simplicity, so let's see where it gets us.

    1. As a prior, I suggest a beta distribution with `alpha=8` and `beta=2`.  What does this prior look like and what does it imply about sellers?

    2. Use the data to update the prior for the three sellers and plot the posterior distributions.  Which seller has the highest posterior mean?

    3. How confident should we be about our choice?  That is, what is the probability that the seller with the highest posterior mean actually has the highest value of `x`?

    4. Consider a beta prior with `alpha=0.7` and `beta=0.5`.  What does this prior look like and what does it imply about sellers?

    5. Run the analysis again with this prior and see what effect it has on the results.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Note: When you evaluate the beta distribution, you should restrict the range of `xs` so it does not include 0 and 1.  When the parameters of the beta distribution are less than 1, the probability density goes to infinity at 0 and 1.  From a mathematical point of view, that's not a problem; it is still a proper probability distribution.  But from a computational point of view, it means we have to avoid evaluating the PDF at 0 and 1.
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


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Exercise:** Use a Dirichlet prior with parameter vector `alpha = [1, 1, 1]` to solve the Lions and Tigers and Bears problem:

    >Suppose we visit a wild animal preserve where we know that the only animals are lions and tigers and bears, but we don't know how many of each there are.
    >
    >During the tour, we see three lions, two tigers, and one bear. Assuming that every animal had an equal chance to appear in our sample, estimate the prevalence of each species.
    >
    >What is the probability that the next animal we see is a bear?
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
