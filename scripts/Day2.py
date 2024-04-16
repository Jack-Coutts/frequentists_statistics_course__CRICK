import pandas as pd  # A Python data analysis and manipulation tool
import pingouin as pg  # Simple yet exhaustive stats functions.
from plotnine import *  # Python equivalent of `ggplot2`
from functions import *  # Import the functions we have written
import statsmodels.api as sm  # Statistical models, conducting tests and statistical data exploration
import statsmodels.formula.api as smf  # Convenience interface for specifying models using formula strings & DataFrames

# Categorical predictors #

# ANOVA #

'''
For example, suppose we measure the feeding rate of oyster catchers (shellfish per hour) 
at three sites characterised by their degree of shelter from the wind, imaginatively called exposed (E), 
partially sheltered (P) and sheltered (S). We want to test whether the data support the hypothesis that feeding 
rates don’t differ between locations. We form the following null and alternative hypotheses:

- The mean feeding rates at all three sites is the same. 
- The mean feeding rates are not all equal.

We will use a one-way ANOVA test to check this.

- We use a one-way ANOVA test because we only have one predictor variable (the categorical variable location).
- We’re using ANOVA because we have more than two groups and we don’t know any better yet with respect to the 
  exact assumptions.
'''
# Define working directory
work_dir = '/Users/couttsj/Desktop/Statistics_Course/'

# Load the data
oystercatcher_py = pd.read_csv(f"{work_dir}data/CS2-oystercatcher-feeding.csv")

# Look at the first 5 row of data
print("----")  # For clarity in Terminal
print(oystercatcher_py.head())

# Look at the descriptive stats per group - only looking at stats of feeding column
print("----")
print(oystercatcher_py.groupby("site")["feeding"].describe())

# Box plots of the data
bp_one = (ggplot(oystercatcher_py, aes("site", "feeding")) + geom_boxplot())
bp_one.show()  # This can be sued to display graphs when using an IDE

'''
To use an ANOVA test, we have to make three assumptions:

1. The parent distributions from which the samples are taken are normally distributed.
2. Each data point in the samples is independent of the others.
3. The parent distributions should have the same variance.
'''

# Create a dataframe for each group
exposed_group = oystercatcher_py[oystercatcher_py['site'] == 'exposed']
partial_group = oystercatcher_py[oystercatcher_py['site'] == 'partial']
sheltered_group = oystercatcher_py[oystercatcher_py['site'] == 'sheltered']

# Assess normality of groups with Q-Q plots - Never use Shapiro-Wilk test
# Exposed Group
qq_one_exposed = (ggplot(exposed_group, aes(sample=exposed_group.feeding))
                  + stat_qq()
                  + stat_qq_line(colour="blue")
                  + labs(title='Q-Q Plot of Feeding by Site - Exposed'))
qq_one_exposed.show()  # Points should lie on the line if distributions the same
# Partial Group
qq_one_partial = (ggplot(partial_group, aes(sample=partial_group.feeding))
                  + stat_qq()
                  + stat_qq_line(colour="blue")
                  + labs(title='Q-Q Plot of Feeding by Site - Partial'))
qq_one_partial.show()
# Sheltered Group
qq_one_sheltered = (ggplot(sheltered_group, aes(sample=sheltered_group.feeding))
                    + stat_qq()
                    + stat_qq_line(colour="blue")
                    + labs(title='Q-Q Plot of Feeding by Site - Sheltered'))
qq_one_sheltered.show()

'''
All groups appear normal enough.

HOWEVER an ANOVA actually uses the residuals rather than the data points themselves. 

This means we want to check the residuals are normally distributed rather than the data points themselves.

We only use the combined set of residuals because the ANOVA created a single linear model to describe the 
residuals. The residuals as a whole need to be normally distributed rather than within their groups as it 
is the success of the model fitting that is used to determine whether the groups are the same or not. The 
residuals are treated as one group for this. 
'''

# Create the residuals by fitting a linear model to the data
model = smf.ols(formula="feeding ~ C(site)", data=oystercatcher_py)
# Get the fitted parameters of the model
lm_oystercatcher_py = model.fit()
# Get the residuals from the fitted model parameters
resids = lm_oystercatcher_py.resid
# Create a Q-Q plot for the residuals
qq_resids_one = (ggplot(oystercatcher_py, aes(sample=resids))
                 + stat_qq()
                 + stat_qq_line(colour="blue")
                 + labs(title='Q-Q Residuals'))
qq_resids_one.show()

"""Q-Q plot for residuals looks normally distributed. Assumption met."""

# Now test for equality of variance using Bartlett's Test
print("----")
print(pg.homoscedasticity(dv="feeding",  # Homoscedasticity is refers to equality of variance
                          group="site",
                          method="bartlett",
                          data=oystercatcher_py))

""" P value is over 0.05 so we cannot reject the null hypothesis that variance across all groups is equal.
    This means that the variance across all groups IS equal. Assumption met."""

""" There are a series of diagnostic plots that can be used instead of doing everything individually.
    This is easy in R but the function to create this plots has been written manually for python, see the 
    functions package."""

# Diagnostic plots.
dgplots(lm_oystercatcher_py)

'''
1. The first graph plots the Residuals plot. If the data are best explained by a linear line then there should be 
   a uniform distribution of points above and below the horizontal blue line (and if there are sufficient points then 
   the red line, which is a smoother line, should be on top of the blue line). This plot looks pretty good.

2. The second graph shows the Q-Q plot which allows a visual inspection of normality. If the residuals are normally 
   distributed, then the points should lie on the diagonal blue line. This plot looks good.
   
3. The third graph shows the Location-Scale graph which allows us to investigate whether there is any correlation 
   between the residuals and the predicted values and whether the variance of the residuals changes significantly. If 
   not, then the red line should be horizontal. If there is any correlation or change in variance then the red line 
   will not be horizontal. This plot is fine.
   
4. The last graph shows the Influential points and tests if any one point has an unnecessarily large effect on the fit. 
   Here we’re using the Cook’s distance as a measure. A rule of thumb is that if any value is larger than 1.0, then it 
   might have a large effect on the model. If not, then no point has undue influence. This plot is good. There are 
   different ways to determine the threshold (apart from simply setting it to 1) and in this plot the blue dashed line 
   is at 4/n, with n being the number of samples. At this threshold there are some data points that may be influential, 
   but I personally find this threshold rather strict.
'''

# Implement the ANOVA
print('----')
print(pg.anova(dv="feeding",
               between="site",
               data=oystercatcher_py,
               detailed=True))

'''
This creates a linear model based on the data, i.e. finds the means of the three groups and calculates a load of 
intermediary data that we need for the statistical analysis.

In the output:

Source: Factor names - in our case these are the different sites (site)
SS: Sums of squares (we’ll get to that in a bit)
DF: Degrees of freedom (at the moment only used for reporting)
MS: Mean squares
F: Our F-statistic
p-unc: p-value (unc stands for “uncorrected” - more on multiple testing correction later)
np2: Partial eta-square effect sizes (more on this later)



Again, the p-value is what we’re most interested in here and shows us the probability of getting samples such as ours 
if the null hypothesis were actually true.

Since the p-value is very small (much smaller than the standard significance level of 0.05) we can say “that it is 
very unlikely that these three samples came from the same parent distribution” and as such we can reject our null 
hypothesis and state that:

        'A one-way ANOVA showed that the mean feeding rate of oystercatchers differed significantly 
         between locations (p = 4.13e-33).'

'''

# Post Hoc Testing (Tukey’s range test) #

'''
One drawback with using an ANOVA test is that it only tests to see if all of the means are the same. If we get a 
significant result using ANOVA then all we can say is that not all of the means are the same, rather than anything 
about how the pairs of groups differ.

Take the following example:

Each group is a random sample of 20 points from a normal distribution with variance 1. Groups 1 and 2 come from a 
parent population with mean 0 whereas group 3 come from a parent population with mean 2. The data clearly satisfy the 
assumptions of an ANOVA test so I won't check them below.
'''

# Load the data
tukey_py = pd.read_csv(f"{work_dir}data/CS2-tukey.csv")

# Have a look at the data
print('----')
print(tukey_py.head())

# Plot the data
bp_two = (ggplot(tukey_py, aes("group", "response"))
          + geom_boxplot())
bp_two.show()

# Test for a significant difference in group means
print('----')
print(pg.anova(dv="response",
               between="group",
               data=tukey_py,
               detailed=True))

"""
Here we have a p-value of 2.39*10-7 and so the test has very conclusively rejected the hypothesis that all 
means are equal.

However, this was not due to all of the sample means being different, but rather just because one of the groups is very 
different from the others. In order to drill down and investigate this further we use a new test called Tukey’s range 
test.

This will compare all of the groups in a pairwise fashion and reports on whether a significant difference exists.
"""

# Perform Tukey’s test
print('----')
print(pg.pairwise_tukey(dv="response",
                        between="group",
                        data=tukey_py).transpose())

"""
As we can see that there isn’t a significant difference between sample1 and sample2 but there is a significant 
difference between sample1 and sample3, as well as sample2 and sample3. This matches with what we expected based on the 
box plot.

Tukey’s range test, when we decide to use it, requires the same three assumptions as an ANOVA test:

1. Normality of distributions
2. Equality of variance between groups
3. Independence of observations
"""

# Kruskal-Wallis #

"""
The Kruskal-Wallis one-way analysis of variance test is an analogue of ANOVA that can be used when the assumption of 
normality cannot be met. In this way it is an extension of the Mann-Whitney test for two groups.
"""


import scikit_posthocs as sp  # Post-hoc tests - includes Dunn's test not in pingouin


"""
Data

For example, suppose a behavioural ecologist records the rate at which spider monkeys behaved aggressively towards one 
another, as a function of how closely related the monkeys are. The familiarity of the two monkeys involved in each 
interaction is classified as high, low or none. We want to test if the data support the hypothesis that aggression 
rates differ according to strength of relatedness. We form the following null and alternative hypotheses:

H0: The median aggression rates for all types of familiarity are the same
H1: The median aggression rates are not all equal

We will use a Kruskal-Wallis test to check this.
"""

# Read in the data
spidermonkey_py = pd.read_csv(f"{work_dir}data/CS2-spidermonkey.csv")

# Look at the data
print('----')
print(spidermonkey_py.head())

# Summarise the data
print('----')
print(spidermonkey_py.describe()["aggression"])

# Create boxplot
bp_three = (ggplot(spidermonkey_py, aes("familiarity", "aggression"))
            + geom_boxplot())
bp_three.show()

"""
The data appear to show a very significant difference in aggression rates between the three types of familiarity. We 
would probably expect a reasonably significant result here.
"""

"""
To use the Kruskal-Wallis test we have to make three assumptions:

1. The parent distributions from which the samples are drawn have the same shape (if they’re normal then we should use a 
   one-way ANOVA)
2. Each data point in the samples is independent of the others
3. The parent distributions should have the same variance

Independence we’ll ignore as usual. Similar shape is best assessed from the earlier visualisation of the data. That 
means that we only need to check equality of variance.
"""

# Test equality of variance
print('----')
print(pg.homoscedasticity(dv="aggression",
                          group="familiarity",
                          method="levene",
                          data=spidermonkey_py))

"""There is equality of variance."""

# Perform a Kruskal-Wallis test
print('----')
print(pg.kruskal(dv="aggression",
                 between="familiarity",
                 data=spidermonkey_py))

"""
Since the p-value is very small (much smaller than the standard significance level of 0.05) we can say “that it is very 
unlikely that these three samples came from the same parent distribution and as such we can reject our null hypothesis” 
and state that:

            'A Kruskal-Wallis test showed that aggression rates between spidermonkeys depends upon the degree of 
            familiarity between them (p = 0.0011).'
"""

# Post-hoc testing (Dunn’s test) #

"""
The equivalent of Tukey’s range test for non-normal data is Dunn’s test.

Dunn’s test is used to check for significant differences in group medians.
"""

# Perform Dunn’s test
print('----')
print(sp.posthoc_dunn(spidermonkey_py,
                      val_col="aggression",
                      group_col="familiarity"))

"""
The p-values of the pairwise comparisons are reported in the table. This table shows that there isn’t a significant 
difference between the high and low groups, as the p-value (0.1598) is too high. The other two comparisons between the 
high familiarity and no familiarity groups and between the low and no groups are significant though.
"""


# Continuous Predictors #

# Linear regression #

"""
Regression analysis not only tests for an association between two or more variables, but also allows you to investigate 
quantitatively the nature of any relationship which is present. This can help you determine if one variable may be used 
to predict values of another. Simple linear regression essentially models the dependence of a scalar dependent variable 
(y) on an independent (or explanatory) variable (x) according to the relationship:

y=B0+B1x

where B0 is the value of the intercept and B1 is the slope of the fitted line. A linear regression analysis assesses if 
the coefficient of the slope, B1, is actually different from zero. If it is different from zero then we can say that 
x has a significant effect on y (since changing x leads to a predicted change in y). If it isn’t significantly 
different from zero, then we say that there isn’t sufficient evidence of such a relationship. To assess whether the 
slope is significantly different from zero we first need to calculate the values of B0 and B1.
"""

"""
Data

We will perform a simple linear regression analysis on the two variables murder and assault from the USArrests data 
set. This rather bleak data set contains statistics on arrests per 100,000 residents for assault, murder and robbery in 
each of the 50 US states in 1973, alongside the proportion of the population who lived in urban areas at that time. We 
wish to determine whether the assault variable is a significant predictor of the murder variable.

Murder = B0 + B1 * Assault

We will be testing the following null and alternative hypotheses:

H0: assault is not a significant predictor of murder, B1 = 0
H1: assault is a significant predictor of murder, B1 != 0
"""

# Read in the data
USArrests_py = pd.read_csv(f"{work_dir}data/CS3-usarrests.csv")

# Create a scatterplot of the data
# create scatterplot of the data
scatt_one = (ggplot(USArrests_py, aes("assault", "murder"))
             + geom_point())
scatt_one.show()

"""
The following four assumptions need to be met:

1. The data must be linear (it is entirely possible to calculate a straight line through data that is not straight - it 
   doesn’t mean that you should!)
2. The residuals must be normally distributed
3. The residuals must not be correlated with their fitted values (i.e. they should be independent).
4. The fit should not depend overly much on a single point (no point should have high leverage).
"""

# Create a linear model
model = smf.ols(formula="murder ~ assault", data=USArrests_py)
# Get the fitted parameters of the model
lm_USArrests_py = model.fit()

# Create the diagnostic plots
dgplots(lm_USArrests_py)

"""
Diagnostic plots look okay.
"""

# We have already implemented the model, so we just need to look at it
print('----')
print(lm_USArrests_py.summary())

"""
We are after the coef values, where the intercept is 0.6317 and the slope is 0.0419.

So here we have found that the line of best fit is given by:

Murder = 0.63 + 0.042 x Assault.

Next we can assess whether the slope is significantly different from zero:
"""
# Perform the ANOVA
print('----')
print(sm.stats.anova_lm(lm_USArrests_py, typ = 2))

"""
The p-value is what we’re most interested in here and shows us the probability of getting data such as ours if the 
null hypothesis were actually true and the slope of the line were actually zero. Since the p-value is excruciatingly 
tiny we can reject our null hypothesis and state that:

            'A simple linear regression showed that the assault rate in US states was a significant predictor of the 
             number of murders (p = 2.60x10-12).'

The p value is used here is better than the above output as it will be considered for each predictor.
"""


# It can be useful to plot the regression line for visual expression
scatt_two = (ggplot(USArrests_py, aes("assault", "murder"))
             + geom_point()
             + geom_smooth(method="lm", se=False, colour="blue"))
scatt_two.show()



