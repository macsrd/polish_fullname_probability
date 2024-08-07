import pandas as pd
import numpy as np

# Function to load data from Excel and calculate probabilities
def load_data(firstname_file, lastname_file):
    try:
        firstnames_df = pd.read_excel(firstname_file)
        lastnames_df = pd.read_excel(lastname_file)
    except Exception as e:
        print(f"Error reading files: {e}")
        return None, None

    try:
        total_firstnames = firstnames_df.iloc[:,2].sum()
        total_lastnames = lastnames_df.iloc[:,1].sum()

        firstnames_df['probability'] = firstnames_df.iloc[:,2] / total_firstnames
        lastnames_df['probability'] = lastnames_df.iloc[:,1] / total_lastnames

# Convert names to lowercase for case-insensitive comparison
        firstnames_df.iloc[:,0] = firstnames_df.iloc[:,0].str.lower()
        lastnames_df.iloc[:,0] = lastnames_df.iloc[:,0].str.lower()

    except KeyError as e:
        print(f"Error in data format: Missing expected column {e}")
        return None, None

    return firstnames_df, lastnames_df

# Function to calculate the probability of a given first name and last name
def calculate_name_probability(firstname, lastname, firstnames_df, lastnames_df):

    firstname = firstname.lower()
    lastname = lastname.lower()

    firstname_prob = firstnames_df[firstnames_df.iloc[:,0] == firstname]['probability']
    lastname_prob = lastnames_df[lastnames_df.iloc[:,0] == lastname]['probability']
    
    if not firstname_prob.empty and not lastname_prob.empty:
        combined_prob = firstname_prob.values[0] * lastname_prob.values[0]
        return combined_prob
    else:
        return None

# Load data for male and female names
female_firstnames_df, female_lastnames_df = load_data('firstname_female.xlsx', 'lastname_female.xlsx')
male_firstnames_df, male_lastnames_df = load_data('firstname_male.xlsx', 'lastname_male.xlsx')

# Check if data is loaded correctly
if female_firstnames_df is None or female_lastnames_df is None:
    print("Failed to load female names data.")
if male_firstnames_df is None or male_lastnames_df is None:
    print("Failed to load male names data.")

# Function to get user input and calculate probability
def get_user_input_and_calculate_probability():
    firstname = input("Enter the first name: ").strip()
    lastname = input("Enter the last name: ").strip()
    gender = input("Enter the gender (male/female): ").strip().lower()

    if gender == 'female':
        firstnames_df = female_firstnames_df
        lastnames_df = female_lastnames_df
    elif gender == 'male':
        firstnames_df = male_firstnames_df
        lastnames_df = male_lastnames_df
    else:
        print("Invalid gender entered. Please enter 'male' or 'female'.")
        return

    probability = calculate_name_probability(firstname, lastname, firstnames_df, lastnames_df)
    if probability is not None:
        print(f"The probability of the name '{firstname} {lastname}' is: {probability * 100:.6f}%")
    else:
        print(f"The name '{firstname} {lastname}' was not found in the dataset.")

# Example usage
if female_firstnames_df is not None and female_lastnames_df is not None and male_firstnames_df is not None and male_lastnames_df is not None:
    get_user_input_and_calculate_probability()
