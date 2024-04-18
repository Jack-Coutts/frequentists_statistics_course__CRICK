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
outfile = '/Users/couttsj/Desktop/Statistics_Course/outputs/day3-output_file.txt'

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
dgplots(plot_dir, 'day3-dg_plots_one', lm_exercise_py)

"""
The assumptions appear to be met well enough, meaning we can implement the ANOVA.
"""

# Run the ANOVA to the outputs file
tb_title_one = 'Two-Way ANOVA: Exercise/Sex on Weight'
anova_results_one = sm.stats.anova_lm(lm_exercise_py, typ=2)
anova_one_string = anova_results_one.to_string()  # Convert DataFrame to string

# Write to output file
write_to_output(tb_title_one, outfile, anova_one_string)


"""
We have a row in the table for each of the different effects that we’ve asked Python to consider. The last column is 
the important one as this contains the p-values. We need to look at the interaction row first.

sex:exercise has a p-value of about 4.89e-08 (which is smaller than 0.05) and so we can conclude that the interaction 
between sex and exercise is significant.

This is where we must stop.

The top two lines (corresponding to the effects of sex and exercise) are meaningless now. This is because the 
interaction means that we cannot interpret the main effects independently. In this case, weight depends on and the sex 
and the exercise regime. This means the effect of sex on weight is dependent on exercise (and vice-versa).

We would report this as follows:

            'A two-way ANOVA test showed that there was a significant interaction between the effects of sex and 
             exercise on weight (p = 4.89e-08). Exercise was associated with a small loss of weight in males but 
             a larger loss of weight in females.'
"""

# Linear Regression with grouped data #

"""
A linear regression analysis with grouped data is used when we have one categorical predictor variable (or factor), and 
one continuous predictor variable. The response variable must still be continuous however.

Data:

    For example in an experiment that looks at light intensity in woodland, how is light intensity (continuous: lux) 
    affected by the height at which the measurement is taken, recorded as depth measured from the top of the canopy 
    (continuous: meters) and by the type of woodland (categorical: Conifer or Broad leaf).

When analysing these type of data we want to know:

1. Is there a difference between the groups?
2. Does the continuous predictor variable affect the continuous response variable (does canopy depth affect measured 
   light intensity?)
3. Is there any interaction between the two predictor variables? Here an interaction would display itself as a 
   difference in the slopes of the regression lines for each group, so for example perhaps the conifer data set has a 
   significantly steeper line than the broad leaf woodland data set.

In this case, no interaction means that the regression lines will have the same slope. Essentially the analysis is 
identical to two-way ANOVA.

We will plot the data and visually inspect it.
1. We will test for an interaction and if it doesn’t exist then:
2. We can test to see if either predictor variable has an effect (i.e. do the regression lines have different 
   intercepts? and is the common gradient significantly different from zero?)
   a. We will first consider how to visualise the data before then carrying out an appropriate statistical test.

"""

# Load the data
treelight_py = pd.read_csv(f"{work_dir}data/CS4-treelight.csv")

# Have a look at the data
write_to_output("Head of Tree Data", outfile, treelight_py.head().to_string())

# Plot the data
scatt_one_treelight = (ggplot(treelight_py, aes(x="depth", y="light", colour="species"))
                       + geom_point()
                       + geom_smooth(method="lm", se=False)  # Add regression lines
                       + scale_color_brewer(type="qual", palette="Dark2")
                       + labs(x="Depth (m)", y="Light intensity (lux)"))

save_plot(f'{plot_dir}day3-scatt_one_treelight.png', scatt_one_treelight)

"""
Looking at this plot, there doesn’t appear to be any significant interaction between the woodland type (Broadleaf and 
Conifer) and the depth at which light measurements were taken (depth) on the amount of light intensity getting through 
the canopy as the gradients of the two lines appear to be very similar. There does appear to be a noticeable slope to 
both lines and both lines look as though they have very different intercepts. All of this suggests that there isn’t any 
interaction but that both depth and species have a significant effect on light independently.

In this case we’re going to implement the test before checking the assumptions. You’ll find out why soon…
"""

# Create a linear model
model = smf.ols(formula="light ~ depth * C(species)",
                data=treelight_py)

# Get the fitted parameters of the model
lm_treelight_py = model.fit()

# Obtain the relevant summary values
write_to_output('Linear Regression Results', outfile, str(lm_treelight_py.summary()))

"""
As with two-way ANOVA we have a row in the table for each of the different effects. At this point we are particularly 
interested in the p-values. We need to look at the interaction first.

The interaction term between depth and species has a p-value of 0.393 (which is bigger than 0.05) and so we can 
conclude that the interaction between depth and species isn’t significant. As such we can now consider whether each of 
the predictor variables independently has an effect.

Both depth and species have very small p-values (2.86x10-9 and 4.13x10 -11) and so we can conclude that they do have a 
significant effect on light.

This means that the two regression lines should have the same non-zero slope, but different intercepts. We would now 
like to know what those values are.

Finding the intercept values is not entirely straightforward and there is some deciphering required to get this right.

For a simple straight line such as the linear regression for the conifer data by itself, the output is relatively 
straightforward:

Python
We have two options to obtain the intercept for conifers only. We could subset our data, keeping only the conifer 
values. We could then create a linear model of those data, and obtain the relevant intercept.

However, since we already created a model for the entire data set (including the interaction term) and printed the 
summary of that, we can actually derive the intercept value with the information that we’ve got.

In the coef table of the summary there are several values:

Intercept                      7798.5655
C(species)[T.Conifer]         -2784.5833
depth                         -221.1256
depth:C(species)[T.Conifer]   -71.0357

This tells us that the overall intercept value for the model with the interaction term is 7798.5655. 
The C(species)[T.Conifer] term means that, to go from this overall intercept value to the intercept for conifer, we 
need to add -2784.5833.

Doing the maths gives us an intercept of 7798.5655 + (-2784.5833) = 5014 if we round this.

Equally, if we want to get the coefficient for depth, then we take the reference value of -221.1256 and add the value 
next to depth:C(species)[T.Conifer] to it. This gives us -221.1256 + (-71.0357) = -292.2 if we round it.

We can interpret this as meaning that the intercept of the regression line is 5014 and the coefficient of the depth variable (the number in front of it in the equation) is -292.2.

So, the equation of the regression line for the conifer data is given by:

light = 5014 + -292.2 * depth

This means that for every extra 1 m of depth of forest canopy we lose 292.2 lux of light.

When we looked at the full data set, we found that interaction wasn’t important. This means that we will have a model 
with two distinct intercepts but only a single slope (that’s what you get for a linear regression without any 
interaction), so we need to calculate that specific combination.
"""

# Create a linear model
model = smf.ols(formula="light ~ depth + C(species)",
                data=treelight_py)

# Get the fitted parameters of the model
lm_treelight_add_py = model.fit()

"""
Notice the + symbol in the argument, as opposed to the * symbol used earlier. This means that we are explicitly not 
including an interaction term in this fit, and consequently we are forcing Python to calculate the equation of lines 
which have the same gradient.
"""

# Write the output
write_to_output('Linear Model w/ no interaction', outfile, str(lm_treelight_add_py.summary()))

"""
Again, I need to work out which group has been used as the baseline.

It will be the group that comes first alphabetically, so it should be Broadleaf
The other way to check would be to look and see which group is not mentioned in the above table. Conifer is mentioned (in the C(species)[T.Conifer] heading) and so again the baseline group is Broadleaf.
This means that the intercept value and depth coefficient correspond to the Broadleaf group and as a result I know what the equation of one of my lines is:

Broadleaf:

        light = 7962 + -262.2 * depth
        
n this example we know that the gradient is the same for both lines (because we explicitly asked to exclude an 
interaction), so all I need to do is find the intercept value for the Conifer group. Unfortunately, the final value 
given in C(species)[T.Conifer] does not give me the intercept for Conifer, instead it tells me the difference between 
the Conifer group intercept and the baseline intercept i.e. the equation for the regression line for conifer woodland 
is given by:

        light = (7962 + -3113) + -262.2 * depth
        light = 4829 + -262.2 * depth

"""

# Assumptions

"""
In this case we first wanted to check if the interaction was significant, prior to checking the assumptions. If we 
would have checked the assumptions first, then we would have done that one the full model (with the interaction), then 
done the ANOVA if everything was OK. We would have then found out that the interaction was not significant, meaning 
we’d have to re-check the assumptions with the new model. In what order you do it is a bit less important here. The 
main thing is that you check the assumptions and report on it!

Anyway, hopefully you’ve got the gist of checking assumptions for linear models by now: diagnostic plots!
"""

# Plot diagnostic plots
dgplots(plot_dir, 'day3-dg_plots_two', lm_treelight_add_py)

"""
- The Residuals plot looks OK, no systematic pattern.
- The Q-Q plot isn’t perfect, but I’m happy with the normality assumption.
- The Location-Scale plot is OK, some very slight suggestion of heterogeneity of variance, but nothing to be too worried 
  about.
- The Influential points plot shows that all of the points are OK
"""

# Multiple Predictors #

"""
Revisiting the linear model framework and expanding to systems with three predictor variables.

Data:

    The data set we’ll be using is located in data/CS5-pm2_5.csv. It contains data on air pollution levels measured in 
    London, in 2019. It also contains several meteorological measurements. Each variable was recorded on a daily basis.

Note: some of the variables are based on simulations.
"""

# Load the data
pm2_5_py = pd.read_csv(f"{work_dir}data/CS5-pm2_5.csv")
# View the data
write_to_output('Head air pollution data', outfile, pm2_5_py.head().to_string())

# Boxplot inner vs outer london
bp_four_pollution = (ggplot(pm2_5_py, aes(x="location", y="pm2_5"))
                     + geom_boxplot()
                     + geom_jitter(width=0.1, alpha=0.7))
save_plot(f'{plot_dir}day3-bp_four_pollution.png', bp_four_pollution)


"""
I’ve added the (jittered) data to the plot, with some transparency (alpha = 0.7). It’s always good to look at the 
actual data and not just summary statistics (which is what the box plot is).

There seems to be quite a difference between the PM2.5 levels in the two London areas, with the levels in inner London 
being markedly higher. I’m not surprised by this! So when we do our statistical testing, I would expect to find a 
clear difference between the locations.

Apart from the location, there are quite a few numerical descriptor variables. At this point I should probably bite 
the bullet and install seaborn, so I can use the pairplot() function.

But I’m not going to ;-)

I’ll just tell you that there is not much of a correlation between pm2_5 and avg_temp or rain_mm, whereas there might be something going on in relation to wind_m_s. So I plot that instead and colour it by location:
"""

# Plot wind vs pm2.5 coloured by loction
scatt_two_pollut = (ggplot(pm2_5_py, aes(x="wind_m_s", y="pm2_5", colour="location"))
                    + geom_point())
save_plot(f'{plot_dir}day3-scatt_two_pollut.png', scatt_two_pollut)

"""
This seems to show that there might be some linear relationship between PM2.5 levels and wind speed.

If I would plot all the other variables against each other, then I would spot that rainfall seems 
completely independent of wind speed (rain fall seems pretty constant). Nor does the average temperature seem in any 
way related to wind speed (it looks like a random collection of data points!). You can check this yourself!

Another way of looking at this would be to create a correlation matrix, like we did before in the correlations chapter:
"""

# Output correlations between variables
write_to_output('Correlations Pollution Variables', outfile, str(pm2_5_py.corr()))





