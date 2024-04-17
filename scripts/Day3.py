import pandas as pd  # A Python data analysis and manipulation tool
from plotnine import *  # Python equivalent of `ggplot2`
from functions import *
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

# Define plot directory
plot_dir = '/Users/couttsj/Desktop/Statistics_Course/outputs/'

# Define output text file
outfile = '/Users/couttsj/Desktop/Statistics_Course/outputs/day3-Output_File.txt'

# Load the data
exercise_py = pd.read_csv(f"{work_dir}data/CS4-exercise.csv")

# Visualise the data with a box plot, sex vs weight
bp_one_svw = (ggplot(exercise_py, aes("sex", "weight"))
              + geom_boxplot())
bp_one_svw.save(filename=f'{plot_dir}day3-bp_one_svw.png', height=15, width=20, units='cm', dpi=600)

# Visualise the data with a box plot, exercise vs weight
bp_two_evw = (ggplot(exercise_py, aes("exercise", "weight"))
              + geom_boxplot())
bp_two_evw.save(filename=f'{plot_dir}day3-bp_two_evw.png', height=15, width=20, units='cm', dpi=600)

# It's much better to visualise all groups
bp_three_combined = (ggplot(exercise_py, aes("sex", "weight", fill="exercise"))
                     + geom_boxplot()
                     + scale_fill_brewer(type="qual", palette="Dark2"))
bp_three_combined.save(filename=f'{plot_dir}day3-bp_three_combined.png', height=15, width=20, units='cm', dpi=600)

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
int_plot_one.save(filename=f'{plot_dir}day3-int_plot_one.png', height=15, width=20, units='cm', dpi=600)


"""
The choice of which categorical factor is plotted on the horizontal axis and which is plotted as different lines is 
completely arbitrary. Looking at the data both ways shouldn’t add anything but often you’ll find that you prefer one 
plot to another.

Plot the interaction plot the other way round:
"""

# Visualise data with the other interaction plot
int_plot_two = (ggplot(exercise_py, aes(x="exercise", y="weight", colour="sex", group="sex"))
                + geom_jitter(width=0.05)
                + stat_summary(fun_data="mean_cl_boot", geom="point", size=3)
                + stat_summary(fun_data="mean_cl_boot", geom="line")
                + scale_colour_brewer(type="qual", palette="Dark2"))
# Save Plot
int_plot_two.save(filename=f'{plot_dir}day3-int_plot_two.png', height=15, width=20, units='cm', dpi=600)

"""
By now you should have a good feeling for the data and could already provide some guesses to the following three questions:

1. Does there appear to be any interaction between the two categorical variables?

If not:
        2. Does exercise have an effect on weight?
        3. Does sex have an effect on weight?

We can now attempt to answer these three questions more formally using an ANOVA test. We have to test for three things: 
the interaction, the effect of exercise and the effect of sex.
"""

"""
Before we can formally test these things we first need to define the model and check the underlying assumptions. We use 
the following code to define the model:
"""

# Create a linear model
model = smf.ols(formula="weight ~ exercise * sex", data=exercise_py)
# Get the fitted parameters of the model
lm_exercise_py = model.fit()

"""
As the two-way ANOVA is a type of linear model we need to satisfy pretty much the same assumptions as we did for a 
simple linear regression or a one-way ANOVA:

1. The data must not have any systematic pattern to it
2. The residuals must be normally distributed
3. The residuals must have homogeneity of variance
4. The fit should not depend overly much on a single point (no point should have high leverage).

Again, we will check these assumptions visually by producing four key diagnostic plots.
"""

# Create the diagnostic plots
dgplots(plot_dir, 'day3-dg_plots', lm_exercise_py)

