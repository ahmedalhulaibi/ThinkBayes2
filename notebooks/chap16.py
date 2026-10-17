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
    # Logistic Regression
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
    This chapter introduces two related topics: log odds and logistic regression.

    In <<_BayessRule>>, we rewrote Bayes's Theorem in terms of odds and derived Bayes's Rule, which can be a convenient way to do a Bayesian update on paper or in your head.
    In this chapter, we'll look at Bayes's Rule on a logarithmic scale, which provides insight into how we accumulate evidence through successive updates.

    That leads directly to logistic regression, which is based on a linear model of the relationship between evidence and the log odds of a hypothesis.
    As an example, we'll use data from the Space Shuttle to explore the relationship between temperature and the probability of damage to the O-rings.

    As an exercise, you'll have a chance to model the relationship between a child's age when they start school and their probability of being diagnosed with Attention Deficit Hyperactivity Disorder (ADHD).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Log Odds

    When I was in grad school, I signed up for a class on the Theory of Computation.
    On the first day of class, I was the first to arrive.
    A few minutes later, another student arrived.

    At the time, about 83% of the students in the computer science program [were male](https://www.aps.org/programs/education/statistics/fraction-phd.cfm), so I was mildly surprised to note that the other student was female.

    When another female student arrived a few minutes later, I started to think I was in the wrong room.
    When third female student arrived, I was confident I was in the wrong room.
    And as it turned out, I was.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    I'll use this anecdote to demonstrate Bayes's Rule on a logarithmic scale and show how it relates to logistic regression.

    Using $H$ to represent the hypothesis that I was in the right room, and $F$ to represent the observation that the first other student was female, we can write Bayes's Rule like this:

    $$O(H|F) = O(H) \frac{P(F|H)}{P(F|not H)}$$

    Before I saw the other students, I was confident I was in the right room, so I might assign prior odds of 10:1 in favor:

    $$O(H) = 10$$
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    If I was in the right room, the likelihood of the first female student was about 17%.
    If I was not in the right room, the likelihood of the first female student was more like 50%,

    $$\frac{P(F|H)}{P(F|not H)} = 17 / 50$$

    So the likelihood ratio is close to 1/3.  Applying Bayes's Rule, the posterior odds were

    $$O(H|F) = 10 / 3$$

    After two students, the posterior odds were

    $$O(H|FF) = 10 / 9$$

    And after three students:

    $$O(H|FFF) = 10 / 27$$

    At that point, I was right to suspect I was in the wrong room.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The following table shows the odds after each update, the corresponding probabilities, and the change in probability after each step, expressed in percentage points.
    """)
    return


@app.function
def prob(o):
    return o / (o+1)


@app.cell
def _():
    import pandas as pd

    index = ['prior', '1 student', '2 students', '3 students']

    table = pd.DataFrame(index=index)
    table['odds'] = [10, 10/3, 10/9, 10/27]
    table['prob'] = prob(table['odds'])
    table['prob diff'] = table['prob'].diff() * 100
    table.fillna('--')
    return pd, table


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Each update uses the same likelihood, but the changes in probability are not the same.  The first update decreases the probability by about 14 percentage points, the second by 24, and the third by 26.
    That's normal for this kind of update, and in fact it's necessary; if the changes were the same size, we would quickly get into negative probabilities.

    The odds follow a more obvious pattern.  Because each update multiplies the odds by the same likelihood ratio, the odds form a geometric sequence.
    And that brings us to consider another way to represent uncertainty: **log odds**, which is the logarithm of odds, usually expressed using the natural log (base $e$).

    Adding log odds to the table:
    """)
    return


@app.cell
def _(table):
    import numpy as np

    table['log odds'] = np.log(table['odds'])
    table['log odds diff'] = table['log odds'].diff()
    table.fillna('--')
    return (np,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    You might notice:

    * When probability is greater than 0.5, odds are greater than 1, and log odds are positive.

    * When probability is less than 0.5, odds are less than 1, and log odds are negative.

    You might also notice that the log odds are equally spaced.
    The change in log odds after each update is the logarithm of the likelihood ratio.
    """)
    return


@app.cell
def _(np):
    np.log(1/3)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    That's true in this example, and we can show that it's true in general by taking the log of both sides of Bayes's Rule.

    $$\log O(H|F) = \log O(H) + \log \frac{P(F|H)}{P(F|not H)}$$

    On a log odds scale, a Bayesian update is additive.  So if $F^x$ means that $x$ female students arrive while I am waiting, the posterior log odds that I am in the right room are:

    $$\log O(H|F^x) = \log O(H) + x \log \frac{P(F|H)}{P(F|not H)}$$

    This equation represents a linear relationship between the log likelihood ratio and the posterior log odds.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    In this example the linear equation is exact, but even when it's not, it is common to use a linear function to model the relationship between an explanatory variable, $x$, and a dependent variable expressed in log odds, like this:

    $$\log O(H | x) = \beta_0 + \beta_1 x$$

    where $\beta_0$ and $\beta_1$ are unknown parameters:

    * The intercept, $\beta_0$, is the log odds of the hypothesis when $x$ is 0.

    * The slope, $\beta_1$, is the log of the likelihood ratio.

    This equation is the basis of logistic regression.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## The Space Shuttle Problem

    As an example of logistic regression, I'll solve a problem from Cameron Davidson-Pilon's book, [*Bayesian Methods for Hackers*](http://nbviewer.jupyter.org/github/CamDavidsonPilon/Probabilistic-Programming-and-Bayesian-Methods-for-Hackers/blob/master/Chapter2_MorePyMC/Ch2_MorePyMC_PyMC2.ipynb).  He writes:

    > "On January 28, 1986, the twenty-fifth flight of the U.S. space shuttle program ended in disaster when one of the rocket boosters of the Shuttle Challenger exploded shortly after lift-off, killing all seven crew members. The presidential commission on the accident concluded that it was caused by the failure of an O-ring in a field joint on the rocket booster, and that this failure was due to a faulty design that made the O-ring unacceptably sensitive to a number of factors including outside temperature. Of the previous 24 flights, data were available on failures of O-rings on 23 (one was lost at sea), and these data were discussed on the evening preceding the Challenger launch, but unfortunately only the data corresponding to the 7 flights on which there was a damage incident were considered important and these were thought to show no obvious trend."

    The dataset is originally from [this paper](https://amstat.tandfonline.com/doi/abs/10.1080/01621459.1989.10478858), but also available from [Davidson-Pilon](https://raw.githubusercontent.com/CamDavidsonPilon/Probabilistic-Programming-and-Bayesian-Methods-for-Hackers/master/Chapter2_MorePyMC/data/challenger_data.csv).
    """)
    return


@app.cell
def _(download):
    download('https://raw.githubusercontent.com/CamDavidsonPilon/Probabilistic-Programming-and-Bayesian-Methods-for-Hackers/master/Chapter2_MorePyMC/data/challenger_data.csv')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    I'll read the data and do some cleaning.
    """)
    return


@app.cell
def _(pd):
    data = pd.read_csv('challenger_data.csv', parse_dates=[0])

    # avoiding column names with spaces
    data.rename(columns={'Damage Incident': 'Damage'}, inplace=True)

    # dropping row 3, in which Damage Incident is NaN,
    # and row 24, which is the record for the Challenger
    data.drop(labels=[3, 24], inplace=True)

    # convert the Damage column to integer
    data['Damage'] = data['Damage'].astype(int)

    data
    return (data,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Here are the first few rows:
    """)
    return


@app.cell
def _(data):
    data.head()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The columns are:

    * `Date`: The date of launch,

    * `Temperature`: Outside temperature in Fahrenheit, and

    * `Damage`: `1` if there was a damage incident and `0` otherwise.

    There are 23 launches in the dataset, 7 with damage incidents.
    """)
    return


@app.cell
def _(data):
    len(data), data['Damage'].sum()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The following figure shows the relationship between damage and temperature.
    """)
    return


@app.cell
def _():
    import matplotlib.pyplot as plt
    from utils import decorate

    def plot_data(data):
        """Plot damage as a function of temperature.
    
        data: DataFrame
        """
        plt.plot(data['Temperature'], data['Damage'], 'o', 
                 label='data', color='C0', alpha=0.4)

        decorate(ylabel="Probability of damage",
             xlabel="Outside temperature (deg F)",
             title="Damage to O-Rings vs Temperature")

    return decorate, plot_data, plt


@app.cell
def _(data, plot_data):
    plot_data(data)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    When the outside temperature was below 65 degrees, there was always damage to the O-rings.  When the temperature was above 65 degrees, there was usually no damage.

    Based on this figure, it seems plausible that the probability of damage is related to temperature.  If we assume this probability follows a logistic model, we can write:

    $$\log O(H | x) = \beta_0 + \beta_1 x$$

    where $H$ is the hypothesis that the O-rings will be damaged, $x$ is temperature, and $\beta_0$ and $\beta_1$ are the parameters we will estimate.
    For reasons I'll explain soon, I'll define $x$ to be temperature shifted by an offset so its mean is 0.
    """)
    return


@app.cell
def _(data):
    offset = data['Temperature'].mean().round()
    data['x'] = data['Temperature'] - offset
    offset
    return (offset,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    And for consistency I'll create a copy of the `Damage` columns called `y`.
    """)
    return


@app.cell
def _(data):
    data['y'] = data['Damage']
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Before doing a Bayesian update, I'll use `statsmodels` to run a conventional (non-Bayesian) logistic regression.
    """)
    return


@app.cell
def _(data):
    import statsmodels.formula.api as smf

    formula = 'y ~ x'
    results = smf.logit(formula, data=data).fit(disp=False)
    results.params
    return (results,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    `results` contains a "point estimate" for each parameter, that is, a single value rather than a posterior distribution.

    The intercept is about -1.2, and the estimated slope is about -0.23.
    To see what these parameters mean, I'll use them to compute probabilities for a range of temperatures.
    Here's the range:
    """)
    return


@app.cell
def _(np, offset, results):
    inter = results.params['Intercept']
    slope = results.params['x']
    xs = np.arange(53, 83) - offset
    return inter, slope, xs


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We can use the logistic regression equation to compute log odds:
    """)
    return


@app.cell
def _(inter, slope, xs):
    log_odds = inter + slope * xs
    return (log_odds,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    And then convert to probabilities.
    """)
    return


@app.cell
def _(log_odds, np):
    odds = np.exp(log_odds)
    ps = odds / (odds + 1)
    return (ps,)


@app.cell
def _(ps):
    ps.mean()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Converting log odds to probabilities is a common enough operation that it has a name, `expit`, and SciPy provides a function that computes it.
    """)
    return


@app.cell
def _(inter, slope, xs):
    from scipy.special import expit
    ps_1 = expit(inter + slope * xs)
    return expit, ps_1


@app.cell
def _(ps_1):
    ps_1.mean()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Here's what the logistic model looks like with these estimated parameters.
    """)
    return


@app.cell
def _(data, offset, plot_data, plt, ps_1, xs):
    plt.plot(xs + offset, ps_1, label='model', color='C1')
    plot_data(data)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    At low temperatures, the probability of damage is high; at high temperatures, it drops off to near 0.

    But that's based on conventional logistic regression.
    Now we'll do the Bayesian version.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Prior Distribution

    I'll use uniform distributions for both parameters, using the point estimates from the previous section to help me choose the upper and lower bounds.
    """)
    return


@app.cell
def _(np):
    from utils import make_uniform
    _qs = np.linspace(-5, 1, num=101)
    prior_inter = make_uniform(_qs, 'Intercept')
    return make_uniform, prior_inter


@app.cell
def _(make_uniform, np):
    _qs = np.linspace(-0.8, 0.1, num=101)
    prior_slope = make_uniform(_qs, 'Slope')
    return (prior_slope,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We can use `make_joint` to construct the joint prior distribution.
    """)
    return


@app.cell
def _(prior_inter, prior_slope):
    from utils import make_joint

    joint = make_joint(prior_inter, prior_slope)
    return (joint,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The values of `intercept` run across the columns, the values of `slope` run down the rows.

    For this problem, it will be convenient to "stack" the prior so the parameters are levels in a `MultiIndex`, and put the result in a `Pmf`.
    """)
    return


@app.cell
def _(joint):
    from empiricaldist import Pmf

    joint_pmf = Pmf(joint.stack())
    joint_pmf.head()
    return Pmf, joint_pmf


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    `joint_pmf` is a `Pmf` with two levels in the index, one for each parameter.  That makes it easy to loop through possible pairs of parameters, as we'll see in the next section.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Likelihood

    To do the update, we have to compute the likelihood of the data for each possible pair of parameters.

    To make that easier, I'm going to group the data by temperature, `x`, and count the number of launches and damage incidents at each temperature.
    """)
    return


@app.cell
def _(data):
    grouped = data.groupby('x')['y'].agg(['count', 'sum'])
    grouped.head()
    return (grouped,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The result is a `DataFrame` with two columns: `count` is the number of launches at each temperature; `sum` is the number of damage incidents.
    To be consistent with the parameters of the binomial distributions, I'll assign them to variables named `ns` and `ks`.
    """)
    return


@app.cell
def _(grouped):
    ns = grouped['count']
    ks = grouped['sum']
    return ks, ns


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    To compute the likelihood of the data, let's assume temporarily that the parameters we just estimated, `slope` and `inter`,  are correct.

    We can use them to compute the probability of damage at each launch temperature, like this:
    """)
    return


@app.cell
def _(expit, grouped, inter, slope):
    xs_1 = grouped.index
    ps_2 = expit(inter + slope * xs_1)
    return ps_2, xs_1


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    `ps` contains the probability of damage for each launch temperature, according to the model.

    Now, for each temperature we have `ns`, `ps`, and `ks`;
    we can use the binomial distribution to compute the likelihood of the data.
    """)
    return


@app.cell
def _(ks, ns, ps_2):
    from scipy.stats import binom
    likes = binom.pmf(ks, ns, ps_2)
    likes
    return binom, likes


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Each element of `likes` is the probability of seeing `k` damage incidents in `n` launches if the probability of damage is `p`.
    The likelihood of the whole dataset is the product of this array.
    """)
    return


@app.cell
def _(likes):
    likes.prod()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    That's how we compute the likelihood of the data for a particular pair of parameters.
    Now we can compute the likelihood of the data for all possible pairs:
    """)
    return


@app.cell
def _(binom, expit, joint_pmf, ks, ns, xs_1):
    likelihood = joint_pmf.copy()
    for slope_1, inter_1 in joint_pmf.index:
        ps_3 = expit(inter_1 + slope_1 * xs_1)
        likes_1 = binom.pmf(ks, ns, ps_3)
        likelihood[slope_1, inter_1] = likes_1.prod()
    return (likelihood,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    To initialize `likelihood`, we make a copy of `joint_pmf`, which is a convenient way to make sure that `likelihood` has the same type, index, and data type as `joint_pmf`.

    The loop iterates through the parameters.  For each possible pair, it uses the logistic model to compute `ps`, computes the likelihood of the data, and assigns the result to a row in `likelihood`.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## The Update

    Now we can compute the posterior distribution in the usual way.
    """)
    return


@app.cell
def _(joint_pmf, likelihood):
    posterior_pmf = joint_pmf * likelihood
    posterior_pmf.normalize()
    return (posterior_pmf,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Because we used a uniform prior, the parameter pair with the highest likelihood is also the pair with maximum posterior probability:
    """)
    return


@app.cell
def _(pd, posterior_pmf):
    pd.Series(posterior_pmf.max_prob(),
              index=['slope', 'inter'])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    So we can confirm that the results of the Bayesian update are consistent with the maximum likelihood estimate computed by StatsModels:
    """)
    return


@app.cell
def _(results):
    results.params
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    They are approximately the same, within the precision of the grid we're using.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    If we unstack the posterior `Pmf` we can make a contour plot of the joint posterior distribution.
    """)
    return


@app.cell
def _(decorate, posterior_pmf):
    from utils import plot_contour

    joint_posterior = posterior_pmf.unstack()
    plot_contour(joint_posterior)
    decorate(title='Joint posterior distribution')
    return (joint_posterior,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The ovals in the contour plot are aligned along a diagonal, which indicates that there is some correlation between `slope` and `inter` in the posterior distribution.

    But the correlation is weak, which is one of the reasons we subtracted off the mean launch temperature when we computed `x`; centering the data minimizes the correlation between the parameters.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Exercise:** To see why this matters, go back and set `offset=60` and run the analysis again.
    The slope should be the same, but the intercept will be different.  And if you plot the joint distribution, the contours you get will be elongated, indicating stronger correlation between the estimated parameters.

    In theory, this correlation is not a problem, but in practice it is.  With uncentered data, the posterior distribution is more spread out, so it's harder to cover with the joint prior distribution.
    Centering the data maximizes the precision of the estimates; with uncentered data, we have to do more computation to get the same precision.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Marginal Distributions

    Finally, we can extract the marginal distributions.
    """)
    return


@app.cell
def _(joint_posterior):
    from utils import marginal

    marginal_inter = marginal(joint_posterior, 0)
    marginal_slope = marginal(joint_posterior, 1)
    return marginal_inter, marginal_slope


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Here's the posterior distribution of `inter`.
    """)
    return


@app.cell
def _(decorate, marginal_inter):
    marginal_inter.plot(label='intercept', color='C4')

    decorate(xlabel='Intercept',
             ylabel='PDF',
             title='Posterior marginal distribution of intercept')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    And here's the posterior distribution of `slope`.
    """)
    return


@app.cell
def _(decorate, marginal_slope):
    marginal_slope.plot(label='slope', color='C2')

    decorate(xlabel='Slope',
             ylabel='PDF',
             title='Posterior marginal distribution of slope')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Here are the posterior means.
    """)
    return


@app.cell
def _(marginal_inter, marginal_slope, pd):
    pd.Series([marginal_inter.mean(), marginal_slope.mean()],
              index=['inter', 'slope'])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Both marginal distributions are moderately skewed, so the posterior means are somewhat different from the point estimates.
    """)
    return


@app.cell
def _(results):
    results.params
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Transforming Distributions

    Let's interpret these parameters.  Recall that the intercept is the log odds of the hypothesis when $x$ is 0, which is when temperature is about 70 degrees F (the value of `offset`).
    So we can interpret the quantities in `marginal_inter` as log odds.

    To convert them to probabilities, I'll use the following function, which transforms the quantities in a `Pmf` by applying a given function:
    """)
    return


@app.cell
def _(Pmf):
    def transform(pmf, func):
        """Transform the quantities in a Pmf."""
        ps = pmf.ps
        qs = func(pmf.qs)
        return Pmf(ps, qs, copy=True)

    return (transform,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    If we call `transform` and pass `expit` as a parameter, it transforms the log odds in `marginal_inter` into probabilities and returns the posterior distribution of `inter` expressed in terms of probabilities.
    """)
    return


@app.cell
def _(expit, marginal_inter, transform):
    marginal_probs = transform(marginal_inter, expit)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    `Pmf` provides a `transform` method that does the same thing.
    """)
    return


@app.cell
def _(expit, marginal_inter):
    marginal_probs_1 = marginal_inter.transform(expit)
    return (marginal_probs_1,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Here's the posterior distribution for the probability of damage at 70 degrees F.
    """)
    return


@app.cell
def _(decorate, marginal_probs_1):
    marginal_probs_1.plot(color='C1')
    decorate(xlabel='Probability of damage at 70 deg F', ylabel='PDF', title='Posterior marginal distribution of probabilities')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The mean of this distribution is about 22%, which is the probability of damage at 70 degrees F, according to the model.
    """)
    return


@app.cell
def _(marginal_probs_1):
    mean_prob = marginal_probs_1.mean()
    mean_prob
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    This result shows the second reason I defined `x` to be zero when temperature is 70 degrees F; this way, the intercept corresponds to the probability of damage at a relevant temperature, rather than 0 degrees F.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Now let's look more closely at the estimated slope.  In the logistic model, the parameter $\beta_1$ is the log of the likelihood ratio.

    So we can interpret the quantities in `marginal_slope` as log likelihood ratios, and we can use `exp` to transform them to likelihood ratios (also known as Bayes factors).
    """)
    return


@app.cell
def _(marginal_slope, np):
    marginal_lr = marginal_slope.transform(np.exp)
    return (marginal_lr,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The result is the posterior distribution of likelihood ratios; here's what it looks like.
    """)
    return


@app.cell
def _(decorate, marginal_lr):
    marginal_lr.plot(color='C3')

    decorate(xlabel='Likelihood ratio of 1 deg F',
             ylabel='PDF',
             title='Posterior marginal distribution of likelihood ratios')
    return


@app.cell
def _(marginal_lr):
    mean_lr = marginal_lr.mean()
    mean_lr
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The mean of this distribution is about 0.75, which means that each additional degree Fahrenheit provides evidence against the possibility of damage, with a likelihood ratio (Bayes factor) of 0.75.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Notice:

    * I computed the posterior mean of the probability of damage at 70 deg F by transforming the marginal distribution of the intercept to the marginal distribution of probability, and then computing the mean.

    * I computed the posterior mean of the likelihood ratio by transforming the marginal distribution of slope to the marginal distribution of likelihood ratios, and then computing the mean.

    This is the correct order of operations, as opposed to computing the posterior means first and then transforming them.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    To see the difference, let's compute both values the other way around.
    Here's the posterior mean of `marginal_inter`, transformed to a probability, compared to the mean of `marginal_probs`.
    """)
    return


@app.cell
def _(expit, marginal_inter, marginal_probs_1):
    (expit(marginal_inter.mean()), marginal_probs_1.mean())
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    And here's the posterior mean of `marginal_slope`, transformed to a likelihood ratio, compared to the mean `marginal_lr`.
    """)
    return


@app.cell
def _(marginal_lr, marginal_slope, np):
    np.exp(marginal_slope.mean()), marginal_lr.mean()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    In this example, the differences are not huge, but they can be.
    As a general rule, transform first, then compute summary statistics.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Predictive Distributions

    In the logistic model, the parameters are interpretable, at least after transformation.  But often what we care about are predictions, not parameters.  In the Space Shuttle problem, the most important prediction is, "What is the probability of O-ring damage if the outside temperature is 31 degrees F?"

    To make that prediction, I'll draw a sample of parameter pairs from the posterior distribution.
    """)
    return


@app.cell
def _(np):
    np.random.seed(17)
    return


@app.cell
def _(posterior_pmf):
    sample = posterior_pmf.choice(101)
    return (sample,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The result is an array of 101 tuples, each representing a possible pair of parameters.
    I chose this sample size to make the computation fast.
    Increasing it would not change the results much, but they would be a little more precise.
    """)
    return


@app.cell
def _(sample):
    sample.shape
    return


@app.cell
def _(sample):
    sample.dtype
    return


@app.cell
def _(sample):
    type(sample[0])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    To generate predictions, I'll use a range of temperatures from 31 degrees F (the temperature when the Challenger launched) to 82 degrees F (the highest observed temperature).
    """)
    return


@app.cell
def _(np, offset):
    temps = np.arange(31, 83)
    xs_2 = temps - offset
    return temps, xs_2


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The following loop uses `xs` and the sample of parameters to construct an array of predicted probabilities.
    """)
    return


@app.cell
def _(expit, np, sample, xs_2):
    pred = np.empty((len(sample), len(xs_2)))
    for i, (slope_2, inter_2) in enumerate(sample):
        pred[i] = expit(inter_2 + slope_2 * xs_2)
    return (pred,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The result has one column for each value in `xs` and one row for each element of `sample`.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    To get a quick sense of what the predictions look like, we can loop through the rows and plot them.
    """)
    return


@app.cell
def _(data, plot_data, plt, pred, temps):
    for ps_4 in pred:
        plt.plot(temps, ps_4, color='C1', lw=0.5, alpha=0.4)
    plot_data(data)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The overlapping lines in this figure give a sense of the most likely value at each temperature and the degree of uncertainty.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    In each column, I'll compute the median to quantify the central tendency and a 90% credible interval to quantify the uncertainty.

    `np.percentile` computes the given percentiles; with the argument `axis=0`, it computes them for each column.
    """)
    return


@app.cell
def _(np, pred):
    low, median, high = np.percentile(pred, [5, 50, 95], axis=0)
    return high, low, median


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The results are arrays containing predicted probabilities for the lower bound of the 90% CI, the median, and the upper bound of the CI.

    Here's what they look like:
    """)
    return


@app.cell
def _(data, high, low, median, plot_data, plt, temps):
    plt.fill_between(temps, low, high, color='C1', alpha=0.2)
    plt.plot(temps, median, color='C1', label='logistic model')

    plot_data(data)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    According to these results, the probability of damage to the O-rings at 80 degrees F is near 2%, but there is some uncertainty about that prediction; the upper bound of the CI is around 10%.

    At 60 degrees, the probability of damage is near 80%, but the CI is even wider, from 48% to 97%.

    But the primary goal of the model is to predict the probability of damage at 31 degrees F, and the answer is at least 97%, and more likely to be more than 99.9%.
    """)
    return


@app.cell
def _(high, low, median, pd, temps):
    low_1 = pd.Series(low, temps)
    median_1 = pd.Series(median, temps)
    high_1 = pd.Series(high, temps)
    return high_1, low_1, median_1


@app.cell
def _(high_1, low_1, median_1):
    _t = 80
    print(median_1[_t], (low_1[_t], high_1[_t]))
    return


@app.cell
def _(high_1, low_1, median_1):
    _t = 60
    print(median_1[_t], (low_1[_t], high_1[_t]))
    return


@app.cell
def _(high_1, low_1, median_1):
    _t = 31
    print(median_1[_t], (low_1[_t], high_1[_t]))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    One conclusion we might draw is this:  If the people responsible for the Challenger launch had taken into account all of the data, and not just the seven damage incidents, they could have predicted that the probability of damage at 31 degrees F was nearly certain.  If they had, it seems likely they would have postponed the launch.

    At the same time, if they considered the previous figure, they might have realized that the model makes predictions that extend far beyond the data.  When we extrapolate like that, we have to remember not just the uncertainty quantified by the model, which we expressed as a credible interval; we also have to consider the possibility that the model itself is unreliable.

    This example is based on a logistic model, which assumes that each additional degree of temperature contributes the same amount of evidence in favor of (or against) the possibility of damage.  Within a narrow range of temperatures, that might be a reasonable assumption, especially if it is supported by data.  But over a wider range, and beyond the bounds of the data, reality has no obligation to stick to the model.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Empirical Bayes

    In this chapter I used StatsModels to compute the parameters that maximize the probability of the data, and then used those estimates to choose the bounds of the uniform prior distributions.
    It might have occurred to you that this process uses the data twice, once to choose the priors and again to do the update.  If that bothers you, you are not alone.
    The process I used is an example of what's called the [Empirical Bayes method](https://en.wikipedia.org/wiki/Empirical_Bayes_method), although I don't think that's a particularly good name for it.

    Although it might seem problematic to use the data twice, in these examples, it is not.  To see why, consider an alternative: instead of using the estimated parameters to choose the bounds of the prior distribution, I could have used uniform distributions with much wider ranges.
    In that case, the results would be the same; the only difference is that I would spend more time computing likelihoods for parameters where the posterior probabilities are negligibly small.

    So you can think of this version of Empirical Bayes as an optimization that minimizes computation by putting the prior distributions where the likelihood of the data is worth computing.
    This optimization doesn't affect the results, so it doesn't "double-count" the data.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Summary

    So far we have seen three ways to represent degrees of confidence in a hypothesis: probability, odds, and log odds.
    When we write Bayes's Rule in terms of log odds, a Bayesian update is the sum of the prior and the likelihood; in this sense, Bayesian statistics is the arithmetic of hypotheses and evidence.

    This form of Bayes's Theorem is also the foundation of logistic regression, which we used to infer parameters and make predictions.  In the Space Shuttle problem, we modeled the relationship between temperature and the probability of damage, and showed that the Challenger disaster might have been predictable.  But this example is also a warning about the hazards of using a model to extrapolate far beyond the data.

    In the exercises below you'll have a chance to practice the material in this chapter, using log odds to evaluate a political pundit and using logistic regression to model diagnosis rates for Attention Deficit Hyperactivity Disorder (ADHD).

    In the next chapter we'll move from logistic regression to linear regression, which we will use to model changes over time in temperature, snowfall, and the marathon world record.
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
    **Exercise:** Suppose a political pundit claims to be able to predict the outcome of elections, but instead of picking a winner, they give each candidate a probability of winning.
    With that kind of prediction, it can be hard to say whether it is right or wrong.

    For example, suppose the pundit says that Alice has a 70% chance of beating Bob, and then Bob wins the election.  Does that mean the pundit was wrong?
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    One way to answer this question is to consider two hypotheses:

    * `H`: The pundit's algorithm is legitimate; the probabilities it produces are correct in the sense that they accurately reflect the candidates' probabilities of winning.

    * `not H`: The pundit's algorithm is bogus; the probabilities it produces are random values with a mean of 50%.

    If the pundit says Alice has a 70% chance of winning, and she does, that provides evidence in favor of `H` with likelihood ratio 70/50.

    If the pundit says Alice has a 70% chance of winning, and she loses, that's evidence against `H` with a likelihood ratio of 50/30.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Suppose we start with some confidence in the algorithm, so the prior odds are 4 to 1.  And suppose the pundit generates predictions for three elections:

    * In the first election, the pundit says Alice has a 70% chance of winning and she does.

    * In the second election, the pundit says Bob has a 30% chance of winning and he does.

    * In the third election, the pundit says Carol has an 90% chance of winning and she does.

    What is the log likelihood ratio for each of these outcomes?  Use the log-odds form of Bayes's Rule to compute the posterior log odds for `H` after these outcomes.  In total, do these outcomes increase or decrease your confidence in the pundit?

    If you are interested in this topic, you can [read more about it in this blog post](http://allendowney.blogspot.com/2016/11/why-are-we-so-surprised.html).
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


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Exercise:**  An article in the *New England Journal of Medicine* reports results from a study that looked at the diagnosis rate of Attention Deficit Hyperactivity Disorder (ADHD) as a function of birth month: ["Attention Deficit–Hyperactivity Disorder and Month of School Enrollment"](https://www.nejm.org/doi/10.1056/NEJMoa1806828).

    They found that children born in June, July, and August were substantially more likely to be diagnosed with ADHD, compared to children born in September, but only in states that use a September cutoff for children to enter kindergarten.  In these states, children born in August start school almost a year younger than children born in September.  The authors of the study suggest that the cause is "age-based variation in behavior that may be attributed to ADHD rather than to the younger age of the children".

    Use the methods in this chapter to estimate the probability of diagnosis as a function of birth month.
    The notebook for this chapter provides the data and some suggestions for getting started.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The paper includes this figure:

    <img width="500" src="https://www.nejm.org/na101/home/literatum/publisher/mms/journals/content/nejm/2018/nejm_2018.379.issue-22/nejmoa1806828/20190131/images/img_xlarge/nejmoa1806828_f1.jpeg">

    In my opinion, this representation of the data does not show the effect as clearly as it could.

    But the figure includes the raw data, so we can analyze it ourselves.

    Note: there is an error in the figure, confirmed by personal correspondence:

    > The May and June [diagnoses] are reversed. May should be 317 (not 287) and June should be 287 (not 317).

    So here is the corrected data, where `n` is the number of children born in each month, starting with January, and `k` is the number of children diagnosed with ADHD.
    """)
    return


@app.cell
def _(np):
    n = np.array([32690, 31238, 34405, 34565, 34977, 34415, 
                       36577, 36319, 35353, 34405, 31285, 31617])

    k = np.array([265, 280, 307, 312, 317, 287, 
                          320, 309, 225, 240, 232, 243])
    return k, n


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    First, I'm going to "roll" the data so it starts in September rather than January.
    """)
    return


@app.cell
def _(k, n, np):
    x = np.arange(12)
    n_1 = np.roll(n, -8)
    k_1 = np.roll(k, -8)
    return k_1, n_1, x


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    And I'll put it in a `DataFrame` with one row for each month and the diagnosis rate per 10,000.
    """)
    return


@app.cell
def _(k_1, n_1, pd, x):
    adhd = pd.DataFrame(dict(x=x, k=k_1, n=n_1))
    adhd['rate'] = adhd['k'] / adhd['n'] * 10000
    adhd
    return (adhd,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Here's what the diagnosis rates look like.
    """)
    return


@app.cell
def _(decorate, plt):
    def plot_adhd(adhd):
        plt.plot(adhd['x'], adhd['rate'], 'o', 
                 label='data', color='C0', alpha=0.4)
    
        plt.axvline(5.5, color='gray', alpha=0.2)
        plt.text(6, 64, 'Younger than average')
        plt.text(5, 64, 'Older than average', horizontalalignment='right')

        decorate(xlabel='Birth date, months after cutoff',
                 ylabel='Diagnosis rate per 10,000')

    return (plot_adhd,)


@app.cell
def _(adhd, plot_adhd):
    plot_adhd(adhd)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    For the first 9 months, from September to May, we see what we would expect if some of the excess diagnoses are due to "age-based variation in behavior".  For each month of difference in age, we see an increase in the number of diagnoses.

    This pattern breaks down for the last three months, June, July, and August.  This might be explained by random variation, but it also might be due to parental manipulation; if some parents hold back children born near the deadline, the observations for these month would include a mixture of children who are relatively old for their grade and therefore less likely to be diagnosed.

    Unfortunately, the dataset includes only month of birth, not year, so we don't know the actual ages of these students when they started school.  However, we can use the first nine months to estimate the effect of age on diagnosis rate; then we can think about what to do with the other three months.

    Use the methods in this chapter to estimate the probability of diagnosis as a function of birth month.
    Start with the following prior distributions.
    """)
    return


@app.cell
def _(make_uniform, np):
    _qs = np.linspace(-5.2, -4.6, num=51)
    prior_inter_1 = make_uniform(_qs, 'Intercept')
    return


@app.cell
def _(make_uniform, np):
    _qs = np.linspace(0.0, 0.08, num=51)
    prior_slope_1 = make_uniform(_qs, 'Slope')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    1. Make a joint prior distribution and update it using the data for the first nine months.

    2. Then draw a sample from the posterior distribution and use it to compute the median probability of diagnosis for each month and a 90% credible interval.

    3. As a bonus exercise, do a second update using the data from the last three months, but treating the observed number of diagnoses as a lower bound on the number of diagnoses there would be if no children were kept back.
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
