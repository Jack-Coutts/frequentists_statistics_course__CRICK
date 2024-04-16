import pandas as pd  # A Python data analysis and manipulation tool
import pingouin as pg  # Simple yet exhaustive stats functions.
from plotnine import *  # Python equivalent of `ggplot2`
import statsmodels.api as sm  # Statistical models, conducting tests and statistical data exploration
import statsmodels.formula.api as smf  # Convenience interface for specifying models using formula strings & DataFrames

# ANOVA #

'''
For example, suppose we measure the feeding rate of oyster catchers (shellfish per hour) 
at three sites characterised by their degree of shelter from the wind, imaginatively called exposed (E), 
partially sheltered (P) and sheltered (S). We want to test whether the data support the hypothesis that feeding 
rates don’t differ between locations. We form the following null and alternative hypotheses:

- The mean feeding rates at all three sites is the same 
- The mean feeding rates are not all equal.

We will use a one-way ANOVA test to check this.

- We use a one-way ANOVA test because we only have one predictor variable (the categorical variable location).
- We’re using ANOVA because we have more than two groups and we don’t know any better yet with respect to the 
  exact assumptions.
'''