import pandas as pd

# Import data sets
Speeches_df = pd.read_csv('/Users/tiagooliveira/Dev/LSE/ST2195/st2195_assignment_6/speeches.csv', delimiter='|')
fx_df = pd.read_csv('/Users/tiagooliveira/Dev/LSE/ST2195/st2195_assignment_6/fx.csv', delimiter=',')

# Merge data sets on date
df_1 = Speeches_df.merge(fx_df, on='date')

# Check for missing values
missing_values = df_1.isnull().sum()
print(missing_values)

# Print missing values from the FX column
# Create a boolean mask for missing values in the 'us dollar/euro' column
mask = df_1['US dollar/Euro (EXR.D.USD.EUR.SP00.A)'].isnull()

# Use the mask to index into the DataFrame and print the missing values
missing_values_us_euro = df_1[mask]['US dollar/Euro (EXR.D.USD.EUR.SP00.A)']
print(missing_values_us_euro)

# Remove NA values
df_1_nona = df_1.dropna()
pd.set_option('display.max_rows', 1000)
print(df_1_nona.head(20))

# Convert all columns to numeric, errors='coerce' will set non-numeric values to NaN
df_1_nona = df_1_nona.apply(pd.to_numeric, errors='coerce')

# Then you can calculate the quartiles as before
Q1 = df_1_nona.quantile(0.25)
Q3 = df_1_nona.quantile(0.75)
IQR = Q3 - Q1

lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

# Check for outliers
outliers = ((df_1_nona < lower_bound) | (df_1_nona > upper_bound)).sum()
print(outliers)

if outliers.sum() == 0:
    print('There are no outliers in the data set')
else:
    print(f'There are {outliers.sum()} outliers in the data set')
