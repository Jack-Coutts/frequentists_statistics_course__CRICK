
# Function that will save a plot to a png file
def save_plot(filename, plot):

    plot.save(filename=filename,
              height=15,
              width=20,
              units='cm',
              dpi=600)


