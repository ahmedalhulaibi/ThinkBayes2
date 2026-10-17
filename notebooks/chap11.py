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
    # Comparison
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
    This chapter introduces joint distributions, which are an essential tool for working with distributions of more than one variable.

    We'll use them to solve a silly problem on our way to solving a real problem.
    The silly problem is figuring out how tall two people are, given only that one is taller than the other.
    The real problem is rating chess players (or participants in other kinds of competition) based on the outcome of a game.

    To construct joint distributions and compute likelihoods for these problems, we will use outer products and similar operations.  And that's where we'll start.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Outer Operations

    Many useful operations can be expressed as the "outer product" of two sequences, or another kind of "outer" operation.
    Suppose you have sequences like `x` and `y`:
    """)
    return


@app.cell
def _():
    x = [1, 3, 5]
    y = [2, 4]
    return x, y


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The outer product of these sequences is an array that contains the product of every pair of values, one from each sequence.
    There are several ways to compute outer products, but the one I think is the most versatile is a "mesh grid".

    NumPy provides a function called `meshgrid` that computes a mesh grid.  If we give it two sequences, it returns two arrays.
    """)
    return


@app.cell
def _(x, y):
    import numpy as np

    X, Y = np.meshgrid(x, y)
    return X, Y, np


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The first array contains copies of `x` arranged in rows, where the number of rows is the length of `y`.
    """)
    return


@app.cell
def _(X):
    X
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The second array contains copies of `y` arranged in columns, where the number of columns is the length of `x`.
    """)
    return


@app.cell
def _(Y):
    Y
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Because the two arrays are the same size, we can use them as operands for arithmetic functions like multiplication.
    """)
    return


@app.cell
def _(X, Y):
    X * Y
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    This is result is the outer product of `x` and `y`.
    We can see that more clearly if we put it in a `DataFrame`:
    """)
    return


@app.cell
def _(X, Y, x, y):
    import pandas as pd

    df = pd.DataFrame(X * Y, columns=x, index=y)
    df
    return (pd,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The values from `x` appear as column names; the values from `y` appear as row labels.
    Each element is the product of a value from `x` and a value from `y`.

    We can use mesh grids to compute other operations, like the outer sum, which is an array that contains the *sum* of elements from `x` and elements from `y`.
    """)
    return


@app.cell
def _(X, Y):
    X + Y
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We can also use comparison operators to compare elements from `x` with elements from `y`.
    """)
    return


@app.cell
def _(X, Y):
    X > Y
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The result is an array of Boolean values.

    It might not be obvious yet why these operations are useful, but we'll see examples soon.
    With that, we are ready to take on a new Bayesian problem.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## How Tall Is A?

    Suppose I choose two people from the population of adult males in the U.S.; I'll call them A and B.  If we see that A taller than B, how tall is A?

    To answer this question:

    1. I'll use background information about the height of men in the U.S. to form a prior distribution of height,

    2. I'll construct a joint prior distribution of height for A and B (and I'll explain what that is),

    3. Then I'll update the prior with the information that A is taller, and

    4. From the joint posterior distribution I'll extract the posterior distribution of height for A.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    In the U.S. the average height of male adults is 178 cm and the standard deviation is 7.7 cm.  The distribution is not exactly normal, because nothing in the real world is, but the normal distribution is a pretty good model of the actual distribution, so we can use it as a prior distribution for A and B.

    Here's an array of equally-spaced values from 3 standard deviations below the mean to 3 standard deviations above (rounded up a little).
    """)
    return


@app.cell
def _(np):
    mean = 178
    qs = np.arange(mean-24, mean+24, 0.5)
    return mean, qs


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    SciPy provides a function called `norm` that represents a normal distribution with a given mean and standard deviation, and provides `pdf`, which evaluates the probability density function (PDF) of the normal distribution:
    """)
    return


@app.cell
def _(mean, qs):
    from scipy.stats import norm

    std = 7.7
    ps = norm(mean, std).pdf(qs)
    return (ps,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Probability densities are not probabilities, but if we put them in a `Pmf` and normalize it, the result is a discrete approximation of the normal distribution.
    """)
    return


@app.cell
def _(ps, qs):
    from empiricaldist import Pmf

    prior = Pmf(ps, qs)
    prior.normalize()
    return Pmf, prior


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Here's what it looks like.
    """)
    return


@app.cell
def _(prior):
    from utils import decorate

    prior.plot(style='--', color='C5')

    decorate(xlabel='Height in cm',
             ylabel='PDF',
             title='Approximate distribution of height for men in U.S.')
    return (decorate,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    This distribution represents what we believe about the heights of `A` and `B` before we take into account the data that `A` is taller.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Joint Distribution

    The next step is to construct a distribution that represents the probability of every pair of heights, which is called a joint distribution. The elements of the joint distribution are

    $$P(A_x~\mathrm{and}~B_y)$$

    which is the probability that `A` is $x$ cm tall and `B` is $y$ cm tall, for all values of $x$ and $y$.

    At this point all we know about `A` and `B` is that they are male residents of the U.S., so their heights are independent; that is, knowing the height of `A` provides no additional information about the height of `B`.

    In that case, we can compute the joint probabilities like this:

    $$P(A_x~\mathrm{and}~B_y) = P(A_x)~P(B_y)$$

    Each joint probability is the product of one element from the distribution of `x` and one element from the distribution of `y`.

    So if we have `Pmf` objects that represent the distribution of height for `A` and `B`, we can compute the joint distribution by computing the outer product of the probabilities in each `Pmf`.

    The following function takes two `Pmf` objects and returns a `DataFrame` that represents the joint distribution.
    """)
    return


@app.cell
def _(np, pd):
    def make_joint(pmf1, pmf2):
        """Compute the outer product of two Pmfs."""
        X, Y = np.meshgrid(pmf1, pmf2)
        return pd.DataFrame(X * Y, columns=pmf1.qs, index=pmf2.qs)

    return (make_joint,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The column names in the result are the quantities from `pmf1`; the row labels are the quantities from `pmf2`.

    In this example, the prior distributions for `A` and `B` are the same, so we can compute the joint prior distribution like this:
    """)
    return


@app.cell
def _(make_joint, prior):
    joint = make_joint(prior, prior)
    joint.shape
    return (joint,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The result is a `DataFrame` with possible heights of `A` along the columns, heights of `B` along the rows, and the joint probabilities as elements.

    If the prior is normalized, the joint prior is also be normalized.
    """)
    return


@app.cell
def _(joint):
    joint.to_numpy().sum()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    To add up all of the elements, we convert the `DataFrame` to a NumPy array before calling `sum`.  Otherwise, `DataFrame.sum` would compute the sums of the columns and return a `Series`.
    """)
    return


@app.cell
def _(joint):
    series = joint.sum()
    series.shape
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Visualizing the Joint Distribution

    The following function uses `pcolormesh` to plot the joint distribution.
    """)
    return


@app.cell
def _(decorate):
    import matplotlib.pyplot as plt

    def plot_joint(joint, cmap='Blues'):
        """Plot a joint distribution with a color mesh."""
        vmax = joint.to_numpy().max() * 1.1
        plt.pcolormesh(joint.columns, joint.index, joint, 
                       cmap=cmap,
                       vmax=vmax,
                       shading='nearest')
        plt.colorbar()
    
        decorate(xlabel='A height in cm',
                 ylabel='B height in cm')

    return plot_joint, plt


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Here's what the joint prior distribution looks like.
    """)
    return


@app.cell
def _(decorate, joint, plot_joint):
    plot_joint(joint)
    decorate(title='Joint prior distribution of height for A and B')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    As you might expect, the probability is highest (darkest) near the mean and drops off farther from the mean.

    Another way to visualize the joint distribution is a contour plot.
    """)
    return


@app.cell
def _(decorate, plt):
    def plot_contour(joint):
        """Plot a joint distribution with a contour."""
        plt.contour(joint.columns, joint.index, joint,
                    linewidths=2)
        decorate(xlabel='A height in cm',
                 ylabel='B height in cm')

    return (plot_contour,)


@app.cell
def _(decorate, joint, plot_contour):
    plot_contour(joint)
    decorate(title='Joint prior distribution of height for A and B')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Each line represents a level of equal probability.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Likelihood

    Now that we have a joint prior distribution, we can update it with the data, which is that `A` is taller than `B`.

    Each element in the joint distribution represents a hypothesis about the heights of `A` and `B`.
    To compute the likelihood of every pair of quantities, we can extract the column names and row labels from the prior, like this:
    """)
    return


@app.cell
def _(joint):
    x_1 = joint.columns
    y_1 = joint.index
    return x_1, y_1


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    And use them to compute a mesh grid.
    """)
    return


@app.cell
def _(np, x_1, y_1):
    X_1, Y_1 = np.meshgrid(x_1, y_1)
    return X_1, Y_1


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    `X` contains copies of the quantities in `x`, which are possible heights for `A`.   `Y` contains copies of the quantities in `y`, which are possible heights for `B`.

    If we compare `X` and `Y`, the result is a Boolean array:
    """)
    return


@app.cell
def _(X_1, Y_1):
    A_taller = X_1 > Y_1
    A_taller.dtype
    return (A_taller,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    To compute likelihoods, I'll use `np.where` to make an array with `1` where `A_taller` is `True` and 0 elsewhere.
    """)
    return


@app.cell
def _(A_taller, np):
    a = np.where(A_taller, 1, 0)
    return (a,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    To visualize this array of likelihoods, I'll put in a `DataFrame` with the values of `x` as column names and the values of `y` as row labels.
    """)
    return


@app.cell
def _(a, pd, x_1, y_1):
    likelihood = pd.DataFrame(a, index=x_1, columns=y_1)
    return (likelihood,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Here's what it looks like:
    """)
    return


@app.cell
def _(decorate, likelihood, plot_joint):
    plot_joint(likelihood, cmap='Oranges')
    decorate(title='Likelihood of A>B')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The likelihood of the data is 1 where `X > Y` and 0 elsewhere.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## The Update

    We have a prior, we have a likelihood, and we are ready for the update.  As usual, the unnormalized posterior is the product of the prior and the likelihood.
    """)
    return


@app.cell
def _(joint, likelihood):
    posterior = joint * likelihood
    return (posterior,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    I'll use the following function to normalize the posterior:
    """)
    return


@app.function
def normalize(joint):
    """Normalize a joint distribution."""
    prob_data = joint.to_numpy().sum()
    joint = joint / prob_data
    return prob_data


@app.cell
def _(posterior):
    normalize(posterior)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    And here's what it looks like.
    """)
    return


@app.cell
def _(decorate, plot_joint, posterior):
    plot_joint(posterior)
    decorate(title='Joint posterior distribution of height for A and B')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    All pairs where `B` is taller than `A` have been eliminated.  The rest of the posterior looks the same as the prior, except that it has been renormalized.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Marginal Distributions

    The joint posterior distribution represents what we believe about the heights of `A` and `B` given the prior distributions and the information that `A` is taller.

    From this joint distribution, we can compute the posterior distributions for `A` and `B`.  To see how, let's start with a simpler problem.

    Suppose we want to know the probability that `A` is 180 cm tall.  We can select the column from the joint distribution where `x=180`.
    """)
    return


@app.cell
def _(posterior):
    column = posterior[180]
    column.head()
    return (column,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    This column contains posterior probabilities for all cases where `x=180`; if we add them up, we get the total probability that `A` is 180 cm tall.
    """)
    return


@app.cell
def _(column):
    column.sum()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    It's about 3%.

    Now, to get the posterior distribution of height for `A`, we can add up all of the columns, like this:
    """)
    return


@app.cell
def _(posterior):
    column_sums = posterior.sum(axis=0)
    column_sums.head()
    return (column_sums,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The argument `axis=0` means we want to add up the columns.

    The result is a `Series` that contains every possible height for `A` and its probability.  In other words, it is the distribution of heights for `A`.

    We can put it in a `Pmf` like this:
    """)
    return


@app.cell
def _(Pmf, column_sums):
    marginal_A = Pmf(column_sums)
    return (marginal_A,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    When we extract the distribution of a single variable from a joint distribution, the result is called a **marginal distribution**.
    The name comes from a common visualization that shows the joint distribution in the middle and the marginal distributions in the margins.

    Here's what the marginal distribution for `A` looks like:
    """)
    return


@app.cell
def _(decorate, marginal_A):
    marginal_A.plot(label='Posterior for A')

    decorate(xlabel='Height in cm',
             ylabel='PDF',
             title='Posterior distribution for A')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Similarly, we can get the posterior distribution of height for `B` by adding up the rows and putting the result in a `Pmf`.
    """)
    return


@app.cell
def _(Pmf, posterior):
    row_sums = posterior.sum(axis=1)
    marginal_B = Pmf(row_sums)
    return (marginal_B,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Here's what it looks like.
    """)
    return


@app.cell
def _(decorate, marginal_B):
    marginal_B.plot(label='Posterior for B', color='C1')

    decorate(xlabel='Height in cm',
             ylabel='PDF',
             title='Posterior distribution for B')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Let's put the code from this section in a function:
    """)
    return


@app.cell
def _(Pmf):
    def marginal(joint, axis):
        """Compute a marginal distribution."""
        return Pmf(joint.sum(axis=axis))

    return (marginal,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    `marginal` takes as parameters a joint distribution and an axis number:

    * If `axis=0`, it returns the marginal of the first variable (the one on the x-axis);

    * If `axis=1`, it returns the marginal of the second variable (the one on the y-axis).

    So we can compute both marginals like this:
    """)
    return


@app.cell
def _(marginal, posterior):
    marginal_A_1 = marginal(posterior, axis=0)
    marginal_B_1 = marginal(posterior, axis=1)
    return marginal_A_1, marginal_B_1


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Here's what they look like, along with the prior.
    """)
    return


@app.cell
def _(decorate, marginal_A_1, marginal_B_1, prior):
    prior.plot(style='--', label='Prior', color='C5')
    marginal_A_1.plot(label='Posterior for A')
    marginal_B_1.plot(label='Posterior for B')
    decorate(xlabel='Height in cm', ylabel='PDF', title='Prior and posterior distributions for A and B')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    As you might expect, the posterior distribution for `A` is shifted to the right and the posterior distribution for `B` is shifted to the left.

    We can summarize the results by computing the posterior means:
    """)
    return


@app.cell
def _(prior):
    prior.mean()
    return


@app.cell
def _(marginal_A_1, marginal_B_1):
    print(marginal_A_1.mean(), marginal_B_1.mean())
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Based on the observation that `A` is taller than `B`, we are inclined to believe that `A` is a little taller than average, and `B` is a little shorter.

    Notice that the posterior distributions are a little narrower than the prior.  We can quantify that by computing their standard deviations.
    """)
    return


@app.cell
def _(prior):
    prior.std()
    return


@app.cell
def _(marginal_A_1, marginal_B_1):
    print(marginal_A_1.std(), marginal_B_1.std())
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The standard deviations of the posterior distributions are a little smaller, which means we are more certain about the heights of `A` and `B` after we compare them.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Conditional Posteriors

    Now suppose we measure `A` and find that he is 170 cm tall.  What does that tell us about `B`?

    In the joint distribution, each column corresponds a possible height for `A`.  We can select the column that corresponds to height 170 cm like this:
    """)
    return


@app.cell
def _(posterior):
    column_170 = posterior[170]
    return (column_170,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The result is a `Series` that represents possible heights for `B` and their relative likelihoods.
    These likelihoods are not normalized, but we can normalize them like this:
    """)
    return


@app.cell
def _(Pmf, column_170):
    cond_B = Pmf(column_170)
    cond_B.normalize()
    return (cond_B,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Making a `Pmf` copies the data by default, so we can normalize `cond_B` without affecting `column_170` or `posterior`.
    The result is the conditional distribution of height for `B` given that `A` is 170 cm tall.

    Here's what it looks like:
    """)
    return


@app.cell
def _(cond_B, decorate, marginal_B_1, prior):
    prior.plot(style='--', label='Prior', color='C5')
    marginal_B_1.plot(label='Posterior for B', color='C1')
    cond_B.plot(label='Conditional posterior for B', color='C4')
    decorate(xlabel='Height in cm', ylabel='PDF', title='Prior, posterior and conditional distribution for B')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The conditional posterior distribution is cut off at 170 cm, because we have established that `B` is shorter than `A`, and `A` is 170 cm.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Dependence and Independence

    When we constructed the joint prior distribution, I said that the heights of `A` and `B` were independent, which means that knowing one of them provides no information about the other.
    In other words, the conditional probability $P(A_x | B_y)$ is the same as the unconditional probability $P(A_x)$.

    But in the posterior distribution, $A$ and $B$ are not independent.
    If we know that `A` is taller than `B`, and we know how tall `A` is, that gives us information about `B`.

    The conditional distribution we just computed demonstrates this dependence.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Summary

    In this chapter we started with the "outer" operations, like outer product, which we used to construct a joint distribution.

    In general, you cannot construct a joint distribution from two marginal distributions, but in the special case where the distributions are independent, you can.

    We extended the Bayesian update process and applied it to a joint distribution.  Then from the posterior joint distribution we extracted marginal posterior distributions and conditional posterior distributions.

    As an exercise, you'll have a chance to apply the same process to a problem that's a little more difficult and a lot more useful, updating a chess player's rating based on the outcome of a game.
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
    **Exercise:** Based on the results of the previous example, compute the posterior conditional distribution for `A` given that `B` is 180 cm.

    Hint: Use `loc` to select a row from a `DataFrame`.
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


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Exercise:** Suppose we have established that `A` is taller than `B`, but we don't know how tall `B` is.
    Now we choose a random woman, `C`, and find that she is shorter than `A` by at least 15 cm.  Compute posterior distributions for the heights of `A` and `C`.

    The average height for women in the U.S. is 163 cm; the standard deviation is 7.3 cm.
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
    **Exercise:** [The Elo rating system](https://en.wikipedia.org/wiki/Elo_rating_system) is a way to quantify the skill level of players for games like chess.

    It is based on a model of the relationship between the ratings of players and the outcome of a game.  Specifically, if $R_A$ is the rating of player `A` and $R_B$ is the rating of player `B`, the probability that `A` beats `B` is given by the [logistic function](https://en.wikipedia.org/wiki/Logistic_function):

    $$P(\mathrm{A~beats~B}) = \frac{1}{1 + 10^{(R_B-R_A)/400}}$$

    The parameters 10 and 400 are arbitrary choices that determine the range of the ratings.  In chess, the range is from 100 to 2800.

    Notice that the probability of winning depends only on the difference in rankings.  As an example, if $R_A$ exceeds $R_B$ by 100 points, the probability that `A` wins is
    """)
    return


@app.cell
def _():
    1 / (1 + 10**(-100/400))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Suppose `A` has a current rating of 1600, but we are not sure it is accurate.  We could describe their true rating with a normal distribution with mean 1600 and standard deviation 100, to indicate our uncertainty.

    And suppose `B` has a current rating of 1800, with the same level of uncertainty.

    Then `A` and `B` play and `A` wins.  How should we update their ratings?
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    To answer this question:

    1. Construct prior distributions for `A` and `B`.

    2. Use them to construct a joint distribution, assuming that the prior distributions are independent.

    3. Use the logistic function above to compute the likelihood of the outcome under each joint hypothesis.

    4. Use the joint prior and likelihood to compute the joint posterior.

    5. Extract and plot the marginal posteriors for `A` and `B`.

    6. Compute the posterior means for `A` and `B`.  How much should their ratings change based on this outcome?
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
