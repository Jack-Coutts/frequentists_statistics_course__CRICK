import pandas as pd  # A Python data analysis and manipulation tool
from plotnine import *  # Python equivalent of `ggplot2`
import statsmodels.api as sm  # Statistical models, conducting tests and statistical data exploration
import statsmodels.formula.api as smf  # Convenience interface for specifying models using formula strings & DataFrames


# Two-Way ANOVA #

"""
A two-way analysis of variance is used when we have two categorical predictor variables (or factors) and a single 
continuous response variable. 

For example, when we are looking at how body weight (continuous response variable in kilograms) is affected by sex 
(categorical variable, male or female) and exercise type (categorical variable, control or runner).


When analysing these type of data there are two things we want to know:

1. Does either of the predictor variables have an effect on the response variable i.e. does sex affect body weight? Or 
   does being a runner affect body weight?
   
2. Is there any interaction between the two predictor variables? An interaction would mean that the effect that 
   exercise has on your weight depends on whether you are male or female rather than being independent of your sex. 
   For example if being male means that runners weigh more than non-runners, but being female means that runners weight 
   less than non-runners then we would say that there was an interaction.
   
We will first consider how to visualise the data before then carrying out an appropriate statistical test.
"""

# Define working directory
work_dir = '/Users/couttsj/Desktop/Statistics_Course/'

# Load the data
exercise_py = pd.read_csv(f"{work_dir}data/CS4-exercise.csv")

# Visualise the data with a box plot, sex vs weight
bp_one_svw = (ggplot(exercise_py, aes("sex", "weight"))
              + geom_boxplot())
bp_one_svw.show()

# Visualise the data with a box plot, exercise vs weight
bp_two_evw = (ggplot(exercise_py, aes("exercise", "weight"))
              + geom_boxplot())
bp_two_evw.show()

# It's much better to visualise all groups
bp_three_combined = (ggplot(exercise_py, aes("sex", "weight", fill="exercise"))
                     + geom_boxplot()
                     + scale_fill_brewer(type="qual", palette="Dark2"))
bp_three_combined.show()

"""
In this example there are only four box plots and so it is relatively easy to compare them and look for any 
interactions between variables, but if there were more than two groups per categorical variable, it would become harder 
to spot what was going on.

To compare categorical variables more easily we can just plot the group means which aids our ability to look for 
interactions and the main effects of each predictor variable. This is called an interaction plot.
"""

# Visualise data with an interaction plot
int_plot_one = (ggplot(exercise_py, aes(x="sex", y="weight", colour="exercise", group="exercise"))
                + geom_jitter(width=0.05)
                + stat_summary(fun_data="mean_cl_boot", geom="point", size=3)
                + stat_summary(fun_data="mean_cl_boot", geom="line")
                + scale_colour_brewer(type="qual", palette="Dark2"))
int_plot_one.show()





