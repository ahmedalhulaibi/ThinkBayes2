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
    # Distributions
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
    In the previous chapter we used Bayes's Theorem to solve a cookie problem; then we solved it again using a Bayes table.
    In this chapter, at the risk of testing your patience, we will solve it one more time using a `Pmf` object, which represents a "probability mass function".
    I'll explain what that means, and why it is useful for Bayesian statistics.

    We'll use `Pmf` objects to solve some more challenging problems and take one more step toward Bayesian statistics.
    But we'll start with distributions.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Distributions

    In statistics a **distribution** is a set of possible outcomes and their corresponding probabilities.
    For example, if you toss a coin, there are two possible outcomes with
    approximately equal probability.
    If you roll a six-sided die, the set of possible outcomes is the numbers 1 to 6, and the probability associated with each outcome is 1/6.

    To represent distributions, we'll use a library called `empiricaldist`.
    An "empirical" distribution is based on data, as opposed to a
    theoretical distribution.
    We'll use this library throughout the book.  I'll introduce the basic features in this chapter and we'll see additional features later.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Probability Mass Functions

    If the outcomes in a distribution are discrete, we can describe the distribution with a **probability mass function**, or PMF, which is a function that maps from each possible outcome to its probability.

    `empiricaldist` provides a class called `Pmf` that represents a
    probability mass function.
    To use `Pmf` you can import it like this:
    """)
    return


@app.cell
def _():
    from empiricaldist import Pmf

    return (Pmf,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    If that doesn't work, you might have to install `empiricaldist`; try running

    ```
    !pip install empiricaldist
    ```

    in a code cell or

    ```
    pip install empiricaldist
    ```

    in a terminal window.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The following example makes a `Pmf` that represents the outcome of a
    coin toss.
    """)
    return


@app.cell
def _(Pmf):
    coin = Pmf()
    coin['heads'] = 1/2
    coin['tails'] = 1/2
    coin
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    `Pmf` creates an empty `Pmf` with no outcomes.
    Then we can add new outcomes using the bracket operator.
    In this example, the two outcomes are represented with strings, and they have the same probability, 0.5.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    You can also make a `Pmf` from a sequence of possible outcomes.

    The following example uses `Pmf.from_seq` to make a `Pmf` that represents a six-sided die.
    """)
    return


@app.cell
def _(Pmf):
    die = Pmf.from_seq([1,2,3,4,5,6])
    die
    return (die,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    In this example, all outcomes in the sequence appear once, so they all have the same probability, $1/6$.

    More generally, outcomes can appear more than once, as in the following example:
    """)
    return


@app.cell
def _(Pmf):
    letters = Pmf.from_seq(list('Mississippi'))
    letters
    return (letters,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The letter `M` appears once out of 11 characters, so its probability is $1/11$.
    The letter `i` appears 4 times, so its probability is $4/11$.

    Since the letters in a string are not outcomes of a random process, I'll use the more general term "quantities" for the letters in the `Pmf`.

    The `Pmf` class inherits from a Pandas `Series`, so anything you can do with a `Series`, you can also do with a `Pmf`.

    For example, you can use the bracket operator to look up a quantity and get the corresponding probability.
    """)
    return


@app.cell
def _(letters):
    letters['s']
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    In the word "Mississippi", about 36% of the letters are "s".

    However, if you ask for the probability of a quantity that's not in the distribution, you get a `KeyError`.
    """)
    return


@app.cell
def _(letters):
    try:
        letters['t']
    except KeyError as e:
        print(type(e))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    You can also call a `Pmf` as if it were a function, with a letter in parentheses.
    """)
    return


@app.cell
def _(letters):
    letters('s')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    If the quantity is in the distribution the results are the same.
    But if it is not in the distribution, the result is `0`, not an error.
    """)
    return


@app.cell
def _(letters):
    letters('t')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    With parentheses, you can also provide a sequence of quantities and get a sequence of probabilities.
    """)
    return


@app.cell
def _(die):
    die([1,4,7])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The quantities in a `Pmf` can be strings, numbers, or any other type that can be stored in the index of a Pandas `Series`.
    If you are familiar with Pandas, that will help you work with `Pmf` objects.
    But I will explain what you need to know as we go along.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## The Cookie Problem Revisited

    In this section I'll use a `Pmf` to solve the cookie problem from <<_TheCookieProblem>>.
    Here's the statement of the problem again:

    > Suppose there are two bowls of cookies.
    >
    > * Bowl 1 contains 30 vanilla cookies and 10 chocolate cookies.
    >
    > * Bowl 2 contains 20 vanilla cookies and 20 chocolate cookies.
    >
    > Now suppose you choose one of the bowls at random and, without looking, choose a cookie at random. If the cookie is vanilla, what is the probability that it came from Bowl 1?

    Here's a `Pmf` that represents the two hypotheses and their prior probabilities:
    """)
    return


@app.cell
def _(Pmf):
    prior = Pmf.from_seq(['Bowl 1', 'Bowl 2'])
    prior
    return (prior,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    This distribution, which contains the prior probability for each hypothesis, is called (wait for it) the **prior distribution**.

    To update the distribution based on new data (the vanilla cookie),
    we multiply the priors by the likelihoods. The likelihood
    of drawing a vanilla cookie from Bowl 1 is `3/4`. The likelihood
    for Bowl 2 is `1/2`.
    """)
    return


@app.cell
def _(prior):
    likelihood_vanilla = [0.75, 0.5]
    posterior = prior * likelihood_vanilla
    posterior
    return likelihood_vanilla, posterior


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The result is the unnormalized posteriors; that is, they don't add up to 1.
    To make them add up to 1, we can use `normalize`, which is a method provided by `Pmf`.
    """)
    return


@app.cell
def _(posterior):
    posterior.normalize()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The return value from `normalize` is the total probability of the data, which is $5/8$.

    `posterior`, which contains the posterior probability for each hypothesis, is called (wait now) the **posterior distribution**.
    """)
    return


@app.cell
def _(posterior):
    posterior
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    From the posterior distribution we can select the posterior probability for Bowl 1:
    """)
    return


@app.cell
def _(posterior):
    posterior('Bowl 1')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    And the answer is 0.6.

    One benefit of using `Pmf` objects is that it is easy to do successive updates with more data.
    For example, suppose you put the first cookie back (so the contents of the bowls don't change) and draw again from the same bowl.
    If the second cookie is also vanilla, we can do a second update like this:
    """)
    return


@app.cell
def _(likelihood_vanilla, posterior):
    posterior_1 = posterior * likelihood_vanilla
    posterior_1.normalize()
    posterior_1
    return (posterior_1,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Now the posterior probability for Bowl 1 is almost 70%.
    But suppose we do the same thing again and get a chocolate cookie.

    Here are the likelihoods for the new data:
    """)
    return


@app.cell
def _():
    likelihood_chocolate = [0.25, 0.5]
    return (likelihood_chocolate,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    And here's the update.
    """)
    return


@app.cell
def _(likelihood_chocolate, posterior_1):
    posterior_2 = posterior_1 * likelihood_chocolate
    posterior_2.normalize()
    posterior_2
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Now the posterior probability for Bowl 1 is about 53%.
    After two vanilla cookies and one chocolate, the posterior probabilities are close to 50/50.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 101 Bowls

    Next let's solve a cookie problem with 101 bowls:

    * Bowl 0 contains 0% vanilla cookies,

    * Bowl 1 contains 1% vanilla cookies,

    * Bowl 2 contains 2% vanilla cookies,

    and so on, up to

    * Bowl 99 contains 99% vanilla cookies, and

    * Bowl 100 contains all vanilla cookies.

    As in the previous version, there are only two kinds of cookies, vanilla and chocolate.  So Bowl 0 is all chocolate cookies, Bowl 1 is 99% chocolate, and so on.

    Suppose we choose a bowl at random, choose a cookie at random, and it turns out to be vanilla.  What is the probability that the cookie came from Bowl $x$, for each value of $x$?

    To solve this problem, I'll use `np.arange` to make an array that represents 101 hypotheses, numbered from 0 to 100.
    """)
    return


@app.cell
def _():
    import numpy as np

    hypos = np.arange(101)
    return (hypos,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We can use this array to make the prior distribution:
    """)
    return


@app.cell
def _(Pmf, hypos):
    prior_1 = Pmf(1, hypos)
    prior_1.normalize()
    return (prior_1,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    As this example shows, we can initialize a `Pmf` with two parameters.
    The first parameter is the prior probability; the second parameter is a sequence of quantities.

    In this example, the probabilities are all the same, so we only have to provide one of them; it gets "broadcast" across the hypotheses.
    Since all hypotheses have the same prior probability, this distribution is **uniform**.

    Here are the first few hypotheses and their probabilities.
    """)
    return


@app.cell
def _(prior_1):
    prior_1.head()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The likelihood of the data is the fraction of vanilla cookies in each bowl, which we can calculate using `hypos`:
    """)
    return


@app.cell
def _(hypos):
    likelihood_vanilla_1 = hypos / 100
    likelihood_vanilla_1[:5]
    return (likelihood_vanilla_1,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Now we can compute the posterior distribution in the usual way:
    """)
    return


@app.cell
def _(likelihood_vanilla_1, prior_1):
    posterior1 = prior_1 * likelihood_vanilla_1
    posterior1.normalize()
    posterior1.head()
    return (posterior1,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The following figure shows the prior distribution and the posterior distribution after one vanilla cookie.
    """)
    return


@app.cell
def _():
    from utils import decorate

    def decorate_bowls(title):
        decorate(xlabel='Bowl #',
                 ylabel='PMF',
                 title=title)

    return (decorate_bowls,)


@app.cell
def _(decorate_bowls, posterior1, prior_1):
    prior_1.plot(label='prior', color='C5')
    posterior1.plot(label='posterior', color='C4')
    decorate_bowls('Posterior after one vanilla cookie')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The posterior probability of Bowl 0 is 0 because it contains no vanilla cookies.
    The posterior probability of Bowl 100 is the highest because it contains the most vanilla cookies.
    In between, the shape of the posterior distribution is a line because the likelihoods are proportional to the bowl numbers.

    Now suppose we put the cookie back, draw again from the same bowl, and get another vanilla cookie.
    Here's the update after the second cookie:
    """)
    return


@app.cell
def _(likelihood_vanilla_1, posterior1):
    posterior2 = posterior1 * likelihood_vanilla_1
    posterior2.normalize()
    return (posterior2,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    And here's what the posterior distribution looks like.
    """)
    return


@app.cell
def _(decorate_bowls, posterior2):
    posterior2.plot(label='posterior', color='C4')
    decorate_bowls('Posterior after two vanilla cookies')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    After two vanilla cookies, the high-numbered bowls have the highest posterior probabilities because they contain the most vanilla cookies; the low-numbered bowls have the lowest probabilities.

    But suppose we draw again and get a chocolate cookie.
    Here's the update:
    """)
    return


@app.cell
def _(hypos, posterior2):
    likelihood_chocolate_1 = 1 - hypos / 100
    posterior3 = posterior2 * likelihood_chocolate_1
    posterior3.normalize()
    return (posterior3,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    And here's the posterior distribution.
    """)
    return


@app.cell
def _(decorate_bowls, posterior3):
    posterior3.plot(label='posterior', color='C4')
    decorate_bowls('Posterior after 2 vanilla, 1 chocolate')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Now Bowl 100 has been eliminated because it contains no chocolate cookies.
    But the high-numbered bowls are still more likely than the low-numbered bowls, because we have seen more vanilla cookies than chocolate.

    In fact, the peak of the posterior distribution is at Bowl 67, which corresponds to the fraction of vanilla cookies in the data we've observed, $2/3$.

    The quantity with the highest posterior probability is called the **MAP**, which stands for "maximum a posteriori probability", where "a posteriori" is unnecessary Latin for "posterior".

    To compute the MAP, we can use the `Series` method `idxmax`:
    """)
    return


@app.cell
def _(posterior3):
    posterior3.idxmax()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Or `Pmf` provides a more memorable name for the same thing:
    """)
    return


@app.cell
def _(posterior3):
    posterior3.max_prob()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    As you might suspect, this example isn't really about bowls; it's about estimating proportions.
    Imagine that you have one bowl of cookies.
    You don't know what fraction of cookies are vanilla, but you think it is equally likely to be any fraction from 0 to 1.
    If you draw three cookies and two are vanilla, what proportion of cookies in the bowl do you think are vanilla?
    The posterior distribution we just computed is the answer to that question.

    We'll come back to estimating proportions in the next chapter.
    But first let's use a `Pmf` to solve the dice problem.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## The Dice Problem

    In the previous chapter we solved the dice problem using a Bayes table.
    Here's the statement of the problem:

    > Suppose I have a box with a 6-sided die, an 8-sided die, and a 12-sided die.
    > I choose one of the dice at random, roll it, and report that the outcome is a 1.
    > What is the probability that I chose the 6-sided die?

    Let's solve it using a `Pmf`.
    I'll use integers to represent the hypotheses:
    """)
    return


@app.cell
def _():
    hypos_1 = [6, 8, 12]
    return (hypos_1,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We can make the prior distribution like this:
    """)
    return


@app.cell
def _(Pmf, hypos_1):
    prior_2 = Pmf(1 / 3, hypos_1)
    prior_2
    return (prior_2,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    As in the previous example, the prior probability gets broadcast across the hypotheses.
    The `Pmf` object has two attributes:

    * `qs` contains the quantities in the distribution;

    * `ps` contains the corresponding probabilities.
    """)
    return


@app.cell
def _(prior_2):
    prior_2.qs
    return


@app.cell
def _(prior_2):
    prior_2.ps
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Now we're ready to do the update.
    Here's the likelihood of the data for each hypothesis.
    """)
    return


@app.cell
def _():
    likelihood1 = 1/6, 1/8, 1/12
    return (likelihood1,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    And here's the update.
    """)
    return


@app.cell
def _(likelihood1, prior_2):
    posterior_3 = prior_2 * likelihood1
    posterior_3.normalize()
    posterior_3
    return (posterior_3,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The posterior probability for the 6-sided die is $4/9$.

    Now suppose I roll the same die again and get a 7.
    Here are the likelihoods:
    """)
    return


@app.cell
def _():
    likelihood2 = 0, 1/8, 1/12
    return (likelihood2,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The likelihood for the 6-sided die is 0 because it is not possible to get a 7 on a 6-sided die.
    The other two likelihoods are the same as in the previous update.

    Here's the update:
    """)
    return


@app.cell
def _(likelihood2, posterior_3):
    posterior_4 = posterior_3 * likelihood2
    posterior_4.normalize()
    posterior_4
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    After rolling a 1 and a 7, the posterior probability of the 8-sided die is about 69%.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Updating Dice

    The following function is a more general version of the update in the previous section:
    """)
    return


@app.function
def update_dice(pmf, data):
    """Update pmf based on new data."""
    hypos = pmf.qs
    likelihood = 1 / hypos
    impossible = data > hypos
    likelihood[impossible] = 0
    pmf = pmf * likelihood
    pmf.normalize()


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The first parameter is a `Pmf` that represents the possible dice and their probabilities.
    The second parameter is the outcome of rolling a die.

    The first line selects quantities from the `Pmf` which represent the hypotheses.
    Since the hypotheses are integers, we can use them to compute the likelihoods.
    In general, if there are `n` sides on the die, the probability of any possible outcome is `1/n`.

    However, we have to check for impossible outcomes!
    If the outcome exceeds the hypothetical number of sides on the die, the probability of that outcome is 0.

    `impossible` is a Boolean `Series` that is `True` for each impossible outcome.
    I use it as an index into `likelihood` to set the corresponding probabilities to 0.

    Finally, I multiply `pmf` by the likelihoods and normalize.

    Here's how we can use this function to compute the updates in the previous section.
    I start with a fresh copy of the prior distribution:
    """)
    return


@app.cell
def _(prior_2):
    pmf = prior_2.copy()
    pmf
    return (pmf,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    And use `update_dice` to do the updates.
    """)
    return


@app.cell
def _(pmf):
    update_dice(pmf, 1)
    update_dice(pmf, 7)
    pmf
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The result is the same.  We will see a version of this function in the next chapter.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Summary

    This chapter introduces the `empiricaldist` module, which provides `Pmf`, which we use to represent a set of hypotheses and their probabilities.

    `empiricaldist` is based on Pandas; the `Pmf` class inherits from the Pandas `Series` class and provides additional features specific to probability mass functions.
    We'll use `Pmf` and other classes from `empiricaldist` throughout the book because they simplify the code and make it more readable.
    But we could do the same things directly with Pandas.

    We use a `Pmf` to solve the cookie problem and the dice problem, which we saw in the previous chapter.
    With a `Pmf` it is easy to perform sequential updates with multiple pieces of data.

    We also solved a more general version of the cookie problem, with 101 bowls rather than two.
    Then we computed the MAP, which is the quantity with the highest posterior probability.

    In the next chapter, I'll introduce the Euro problem, and we will use the binomial distribution.
    And, at last, we will make the leap from using Bayes's Theorem to doing Bayesian statistics.

    But first you might want to work on the exercises.
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
    **Exercise:** Suppose I have a box with a 6-sided die, an 8-sided die, and a 12-sided die.
    I choose one of the dice at random, roll it four times, and get 1, 3, 5, and 7.
    What is the probability that I chose the 8-sided die?

    You can use the `update_dice` function or do the update yourself.
    """)
    return


@app.cell
def _():
    # Solution goes here
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Exercise:** In the previous version of the dice problem, the prior probabilities are the same because the box contains one of each die.
    But suppose the box contains 1 die that is 4-sided, 2 dice that are 6-sided, 3 dice that are 8-sided, 4 dice that are 12-sided, and 5 dice that are 20-sided.
    I choose a die, roll it, and get a 7.
    What is the probability that I chose an 8-sided die?

    Hint: To make the prior distribution, call `Pmf` with two parameters.
    """)
    return


@app.cell
def _():
    # Solution goes here
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Exercise:** Suppose I have two sock drawers.
    One contains equal numbers of black and white socks.
    The other contains equal numbers of red, green, and blue socks.
    Suppose I choose a drawer at random, choose two socks at random, and I tell you that I got a matching pair.
    What is the probability that the socks are white?

    For simplicity, let's assume that there are so many socks in both drawers that removing one sock makes a negligible change to the proportions.
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
    **Exercise:** Here's a problem from [Bayesian Data Analysis](http://www.stat.columbia.edu/~gelman/book/):

    > Elvis Presley had a twin brother (who died at birth). What is the probability that Elvis was an identical twin?

    Hint: In 1935, about 2/3 of twins were fraternal and 1/3 were identical.
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
    *Think Bayes*, Second Edition

    Copyright 2020 Allen B. Downey

    License: [Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)](https://creativecommons.org/licenses/by-nc-sa/4.0/)
    """)
    return


if __name__ == "__main__":
    app.run()
