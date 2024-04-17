
# Function to add lines of text to a txt file
def write_to_output(title, filename, text):
    with open(filename, 'a') as file:
        file.write(title + '\n')
        file.write(text + '\n')  # Write the ANOVA results
        file.write('----------\n' * 2)  # Write two lines of dashes

