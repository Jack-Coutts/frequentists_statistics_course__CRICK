import pandas as pd
import pingouin as pg
from plotnine import *

# Working Directory
work_dir = '/Users/couttsj/Desktop/Statistics_Course/'

# Load the Data
fishlength_py = pd.read_csv(f'{work_dir}data/CS1-onesample.csv')

# Inspect the data
print(fishlength_py.head())
print('----')
print(fishlength_py.describe())

# Plot a boxplot of the data
bp_one = (ggplot(fishlength_py, aes('river', 'length')) + geom_boxplot())
bp_one.show()  # Show the plot in current window

# Plot a histogram of the data to check the distribution
hist_one = (ggplot(fishlength_py, aes("length")) + geom_histogram(bins=15))
hist_one.show()

# The data could be normal so look a Q-Q plot
# Quantile-Quantile plot is a diagnostic plot that compares two distributions
qq_one = (ggplot(fishlength_py, aes(sample=fishlength_py.length)) + stat_qq() + stat_qq_line(colour="blue"))
qq_one.show()  # Points should lie on the line if distributions the same

# Points from either end of the sample distribution diverge from where they
# should be if the distribution was normal. Sample distribution is more spread out.
# Implement Shapiro-Wilk test to statistically test to assess whether sample comes from
# distribution.
print('----')
print(pg.normality(fishlength_py.length))
# As the p-value is bigger than 0.05 (say) then we can say that
# there is insufficient evidence to reject the null hypothesis
# that the sample came from a normal distribution.
# This means we can use a parametric test.

# Implement the one-sample, two-tailed t-test
print('----')
print(pg.ttest(x=fishlength_py.length, y=20, alternative="two-sided").round(3))


# Dealing with non-normal data #

# Summarize and visualise - done above for this data

# One-sample Wilcoxon signed rank test assumed symmetry around the median
# Check this visually
median_fishlength = fishlength_py.length.median()

# Histogram
hist_two = (ggplot(fishlength_py, aes("length")) +
            geom_histogram(bins=15) +
            geom_vline(xintercept=median_fishlength, colour="red"))
hist_two.show()

# Box plot
bp_two = (ggplot(fishlength_py, aes(1, "length")) + geom_boxplot())
bp_two.show()
# The distribution looks symmetric enough

# Implement the one-sample, two-tailed Wilcoxon signed rank test
print('----')
print(pg.wilcoxon(fishlength_py.length - 20, alternative="two-sided"))


# 5.9 Exercises

# Gastric Juices
gastric_juices = pd.read_csv(f'{work_dir}data/CS1-gastric_juices.csv')
print('----')
print(gastric_juices.head())

mean_diss_time = gastric_juices.dissolving_time.mean()
print('----')
print(mean_diss_time)

# H0 - The mean dissolving time is 45 seconds
# H1 - The mean dissolving time is not equal to 45 seconds

# Plot a histogram of the data
hist_three = (ggplot(gastric_juices, aes("dissolving_time")) + geom_histogram(bins=5))
hist_three.show()

# Plot q-q plot
qq_three = (ggplot(gastric_juices, aes(sample=gastric_juices.dissolving_time)) + stat_qq() + stat_qq_line(colour="blue"))
qq_three.show() # Looks like it follows normal distribution

# Normal data so a one-sample t-test is appropriate
print('----')
print(pg.ttest(x=gastric_juices.dissolving_time, y=45, alternative="two-sided").round(3))


# A one-sample t-test indicated that the mean dissolving time (45.21) for the drug
# does not differ significantly from 45s.

# 5.10: Gastric juices revisited #

# What if we were unsure if we could assume normality here?
# In that case we’d have to perform a Wilcoxon signed rank test.

# Find the median
median_diss_time = gastric_juices.dissolving_time.median()
print('----')
print(median_diss_time)

# Box plot
bp_three = (ggplot(gastric_juices, aes(1, "dissolving_time")) + geom_boxplot())
bp_three.show()  # Looks symmetric

# Implement the one-sample, two-tailed Wilcoxon signed rank test
print('----')
print(pg.wilcoxon(gastric_juices.dissolving_time - 45, alternative="two-sided"))

# A one-sample Wilcoxon signed rank test indicated that the mean dissolving time (45.21) for the drug
# does not differ significantly from 45s.

