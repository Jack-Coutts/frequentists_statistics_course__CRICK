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

"""
The output n = 63.76 tells that we need 64 (rounding up) students in each group (so 128 in total) in order to carry out 
this study with sufficient power.
"""

"""
What is I need to calculate the effect size as my sample size is predetermined?

If I know in advance that I can only observe 30 students per group, what is the effect size that I should be able 
to observe with 80% power at a 5% significance level?
"""

# Calculate the effect size
effect_size = pg.power_ttest(n=30,
                             alpha=0.05,
                             power=0.80,
                             contrast="two-samples",
                             alternative="two-sided")
write_to_output('Effect Size', outfile, str(effect_size))


"""
This time we want to see what the effect size is so we look at the second line and we can see that an experiment with 
this many people would only be expected to detect a difference in means of d = 0.74 standard deviations. Is this good 
or bad? Well, it depends on the natural variation of your data; if your data is really noisy then it will have a large 
variation and a large standard deviation which will mean that 0.74 standard deviations might actually be quite a big 
difference between your groups. If on the other hand your data doesn’t vary very much, then 0.74 standard deviations 
might actually be a really small number and this test could pick up even quite small differences in mean.
"""


"""
In both of the previous two examples we were a little bit context-free in terms of effect size. Let’s look at how we 
can use a pilot study with real data to calculate effect sizes and perform a power analysis to inform a future study.

Let’s look again at the fishlength data we saw in the first practical relating to the lengths of fish from two 
separate rivers.
"""

# Read in the data
fishlength_py = pd.read_csv(f"{work_dir}data/CS1-twosample.csv")

# Visualise the data
fish_bp_one = (ggplot(fishlength_py, aes(x="river", y="length"))
               + geom_boxplot())
save_plot(f'{plot_dir}day4-fish_bp_one.png', fish_bp_one)

"""
From the plot we can see that the groups appear to have different means. This difference is significant, as per a 
two-sample t-test.
"""

# The ttest() function in pingouin needs two vectors as input, so we split the data
aripo = fishlength_py.query('river == "Aripo"')["length"]
guanapo = fishlength_py.query('river == "Guanapo"')["length"]

# Perform the t test
fish_ttest = pg.ttest(aripo, guanapo, correction=False).transpose()
write_to_output('Fish t-Test', outfile, fish_ttest.to_string())

"""
Can we use this information to design a more efficient experiment? One that we would be confident was powerful enough 
to pick up a difference in means as big as was observed in this study but with fewer observations?

Let’s first work out exactly what the effect size of this previous study really was by estimating Cohen’s d using this 
data.
"""

# Calculate effect size in the data we carried out the t-test on
fish_effect_size = pg.compute_effsize(aripo, guanapo, paired=False, eftype="cohen")
write_to_output('Fish Effect Size', outfile, str(fish_effect_size))

"""
So, the Cohen’s d value for these data are d = 0.94 .

We can now actually answer our question and see how many fish we really need to catch in the future:
"""
# Calculate Sample Size needed in future
future_fish_sample_size = pg.power_ttest(d=0.94, alpha=0.05, power=0.80, contrast="two-samples", alternative="two-sided")
write_to_output("Future Fish Sample Size", outfile, str(future_fish_sample_size))

"""
From this we can see that any future experiments would really only need to use 19 fish for each group (we always round 
this number up, so no fish will be harmed during the experiment…) if we wanted to be confident of detecting the 
difference we observed in the previous study.

This approach can also be used when the pilot study showed a smaller effect size that wasn’t observed to be significant 
(indeed arguably, a pilot study shouldn’t really concern itself with significance but should only really be used as a 
way of assessing potential effect sizes which can then be used in a follow-up study).
"""

# Linear Model Power Calculations

"""
Let’s read in data/CS2-lobsters.csv. This data set was used in an earlier practical and describes the effect of 
three different food sources on lobster weight.

As a quick reminder we’ll also plot the data and perform an ANOVA:
"""

# Read in the data
lobsters_py = pd.read_csv(f"{work_dir}data/CS2-lobsters.csv")

# Visualise the data in a box plot
lobsters_bp_one = (ggplot(lobsters_py, aes(x="diet", y="weight"))
                   + geom_boxplot())
save_plot(f'{plot_dir}day4-lobsters_bp_one.png', lobsters_bp_one)

# Create a linear model
model = smf.ols(formula="weight ~ C(diet)", data=lobsters_py)
# Get the fitted parameters of the model
lm_lobsters_py = model.fit()

# perform the anova on the fitted model
lobster_anova = sm.stats.anova_lm(lm_lobsters_py)
write_to_output('Lobster ANOVA', outfile, lobster_anova.to_string())


