import pandas as pd  # A Python data analysis and manipulation tool
import pingouin as pg  # Simple yet exhaustive stats functions.
from plotnine import *  # Python equivalent of `ggplot2`
from functions import *
import statsmodels.api as sm  # Statistical models, conducting tests and statistical data exploration
import statsmodels.formula.api as smf  # Convenience interface for specifying models using formula strings & DataFrames

# Power Analysis #

"""
All hypothesis tests can be wrong in two ways:

we can appear to have found a significant result when there really isn’t anything there: a false positive (or Type I
error), or we can fail to spot a significant result when there really is something interesting going on: a false
negative (or Type II error).

The probability of getting a false positive in our analysis is precisely the significance level we use in our analysis.
So, in order to reduce the likelihood of getting a false positive we simply reduce the significance level of our test
(from 0.05 down to 0.01 say). Easy as that.

Unfortunately, this has unintended consequences. It turns out that reducing the significance level means that we
increase the chance of getting false negatives. This should make sense; if we’re increasing the barrier to entry in
terms of acceptance then we’ll also accidentally miss out on some of the good stuff.

Power is the capacity of a test to detect significant different results. It is affected by three things:

1. the effect size: i.e. how big of a difference do you want to be able to detect, or alternatively what do you
   consider a meaningful effect/difference to be?
2. sample size
3. the significance level

In an ideal world we would want to be carrying out highly powerful tests using low significance levels, to both reduce
our chance of getting a false positive and maximise our chances of finding a true effect.

Power analysis allows us to design experiments to do just that. Given:

- a desired power (0.8 or 80% is considered pretty good)
- a significance level (0.05 or 5% is our trusty yet arbitrary steed once again)
- an effect size that we would like to detect

We can calculate the amount of data that we need to collect in our experiments.

The reality is that most of the easily usable power analysis functions all operate under the assumption that the data
that you will collect will meet all of the assumptions of your chosen statistical test perfectly. So, for example,
if you want to design an experiment investigating the effectiveness of a single drug compared to a placebo (so a simple
t-test) and you want to know how many patients to have in each group in order for the test to work, then the standard
power analysis techniques will still assume that all of the data that you end up collecting will meet the assumptions
of the t-test that you have to carry out.
"""

# Effect Size

"""
As we shall see the commands for carrying out power analyses are very simple to implement apart from the concept of 
effect size. This is a tricky issue for most people to get to grips with for two reasons:

1. Effect size is related to biological significance rather than statistical significance
2. The way in which we specify effect sizes

The key point about effect sizes and power analyses is that you need to specify an effect size that you would be 
interested in observing, or one that would be biologically relevant to see. There may well actually be a 0.1% 
difference in effectiveness of your drug over a placebo but designing an experiment to detect that would require 
markedly more individuals than an experiment that was trying to detect a 50% difference in effectiveness. In reality 
there are three places we can get a sense of effect sizes from:

- A pilot study
- Previous literature or theory
- Jacob Cohen

Jacob Cohen was an American statistician who developed a large set of measures for effect sizes (which we will use 
today). He came up with a rough set of numerical measures for “small”, “medium” and “large” effect sizes that are still 
in use today. These do come with some caveats though; Jacob was a psychologist and so his assessment of what was a 
large effect may be somewhat different from yours. They do form a useful starting point however.

There a lot of different ways of specifying effects sizes, but we can split them up into three distinct families of 
estimates:

Correlation estimates: these use as a measure of variance explained by a model (for linear models, anova etc. A large 
value would indicate that a lot of variance has been explained by our model and we would expect to see a lot of 
difference between groups, or a tight cluster of points around a line of best fit. The argument goes that we would need 
fewer data points to observe such a relationship with confidence. Trying to find a relationship with a low 
value would be trickier and would therefore require more data points for an equivalent power.

Difference between means: these look at how far apart the means of two groups are, measured in units of standard 
deviations (for t-tests). An effect size of 2 in this case would be interpreted as the two groups having means that 
were two standard deviations away from each other (quite a big difference), whereas an effect size of 0.2 would be 
harder to detect and would require more data to pick it up.

Difference between count data: these I freely admit I have no idea how to intuitively explain them. Mathematically they 
are based on the chi-squared statistic but that’s as good as I can tell you I’m afraid. They are, however, pretty easy 
to calculate.

For reference here are some of Cohen’s suggested values for effect sizes for different tests. You’ll probably be 
surprised by how small some of these are.

Test            Small	Medium	Large
t-tests	        0.2	    0.5	    0.8
anova	        0.1	    0.25	0.4
linear models	0.02	0.15	0.35
chi-squared	    0.1	    0.3	    0.5

We will look at how to carry out power analyses and estimate effect sizes in this section.
"""

# Power analysis t-test

"""
The first example we’ll look at is how to perform a power analysis on two groups of data.

Let’s assume that we want to design an experiment to determine whether there is a difference in the mean price of what 
male and female students pay at a cafe. How many male and female students would we need to observe in order to detect a 
“medium” effect size with 80% power and a significance level of 0.05?

We first need to think about which test we would use to analyse the data. Here we would have two groups of continuous 
response. Clearly a t-test.
"""

"""
First we need to determine what a medium effect size is. We can use the table above to determine that 0.5 is reasonable.

For this sort of study effect size is measured in terms of Cohen’s d statistic. This is simply a measure of how 
different the means of the two groups are expressed in terms of the number of standard deviations they are apart from 
each other. So, in this case we’re looking to detect two means that are 0.5 standard deviations away from each other. 
In a minute we’ll look at what this means for real data.

"""

# Define working directory
work_dir = '/Users/couttsj/Desktop/Statistics_Course/'

# Define plot directory
plot_dir = '/Users/couttsj/Desktop/Statistics_Course/outputs/'

# Define output text file
outfile = '/Users/couttsj/Desktop/Statistics_Course/outputs/day4-output_file.txt'

# Calculate the sample size
sample_size = pg.power_ttest(d=0.5,
                             alpha=0.05,
                             power=0.80)
write_to_output('Sample Size', outfile, str(sample_size))

