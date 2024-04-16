import pandas as pd  # A Python data analysis and manipulation tool
import pingouin as pg  # Simple yet exhaustive stats functions.
from plotnine import *  # Python equivalent of `ggplot2`
from functions import *
import statsmodels.api as sm  # Statistical models, conducting tests and statistical data exploration
import statsmodels.formula.api as smf  # Convenience interface for specifying models using formula strings & DataFrames

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






