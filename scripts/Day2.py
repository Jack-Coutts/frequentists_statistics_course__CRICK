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





# Now test for equality of variance using Bartlett's Test
print("----")
print(pg.homoscedasticity(dv="feeding",
                          group="site",
                          method="bartlett",
                          data=oystercatcher_py))





