import pandas as pd
from nltk.corpus import stopwords

''' Question 1 - Load and merge the datasets keeping all information available for the dates in which there is a measurement in “fx.csv”. [1 point]'''

# Load data sets
Speeches_df = pd.read_csv('/Users/tiagooliveira/Dev/LSE/ST2195/st2195_assignment_6/speeches.csv', delimiter='|')
fx_df = pd.read_csv('/Users/tiagooliveira/Dev/LSE/ST2195/st2195_assignment_6/fx.csv', delimiter=',')

# Merge data sets on date
df_1 = Speeches_df.merge(fx_df, on='date')
print(df_1)
'''Question 2 - Remove entries with obvious outliers or mistakes, if any. [1.5 points]'''

# Convert the 'US dollar/Euro (EXR.D.USD.EUR.SP00.A)' column to numeric
df_1['US dollar/Euro (EXR.D.USD.EUR.SP00.A)'] = pd.to_numeric(df_1['US dollar/Euro (EXR.D.USD.EUR.SP00.A)'], errors='coerce')

# Calculate the quartiles and IQR for the 'US dollar/Euro (EXR.D.USD.EUR.SP00.A)' column
Q1 = df_1['US dollar/Euro (EXR.D.USD.EUR.SP00.A)'].quantile(0.25)
Q3 = df_1['US dollar/Euro (EXR.D.USD.EUR.SP00.A)'].quantile(0.75)
IQR = Q3 - Q1

lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

# Identify the outliers in the 'US dollar/Euro (EXR.D.USD.EUR.SP00.A)' column
outliers = (df_1['US dollar/Euro (EXR.D.USD.EUR.SP00.A)'] < lower_bound) | (df_1['US dollar/Euro (EXR.D.USD.EUR.SP00.A)'] > upper_bound)

# Print the number of outliers
print(f'There are {outliers.sum()} outliers in the data set')

# Remove the outliers from the DataFrame
df_1 = df_1[~outliers]
'''
3. Handle missing observations for the exchange rate, if any. 
This should be done replacing any missing exchange rate with the latest information available.
Whenever this cannot be done, the relevant entry should be removed entirely from the dataset. [1.5 points]
'''

# Print missing values from the FX column
# Create a boolean mask for missing values in the 'us dollar/euro' column
mask = df_1['US dollar/Euro (EXR.D.USD.EUR.SP00.A)'].isnull()

# Use the mask to index into the DataFrame and print the missing values
missing_values_us_euro = df_1[mask]['US dollar/Euro (EXR.D.USD.EUR.SP00.A)']
print(f'Number of missing values in this column: {missing_values_us_euro.sum()}')

# Forward fill to replace missing values with the latest available information
df_1['US dollar/Euro (EXR.D.USD.EUR.SP00.A)'].fillna(method='ffill', inplace=True)

# Check if there are still any missing values
missing_values_after_fill = df_1['US dollar/Euro (EXR.D.USD.EUR.SP00.A)'].isnull().sum()
print(f'Number of missing values after forward fill: {missing_values_after_fill}')

# If there are still missing values, remove those entries
if missing_values_after_fill > 0:
    df_1.dropna(subset=['US dollar/Euro (EXR.D.USD.EUR.SP00.A)'], inplace=True)
    
df_1['Exchange Rate Return'] = df_1['US dollar/Euro (EXR.D.USD.EUR.SP00.A)'].pct_change()
print(df_1['Exchange Rate Return'])
print(df_1)
'''4. Calculate the exchange rate return. 
Extend the original dataset with the following variables: “good_news” (equal to 1 when the exchange rate return is larger than 0.5 percent, 0 otherwise) 
“bad_news” (equal to 1 when the exchange rate return is lower than -0.5 percent, 0 otherwise). [1.5 points]'''

# Initialize 'news' column with None
df_1['news'] = None

# Set 'news' to 'good_news' where 'Exchange Rate Return' is greater than 0.005
df_1.loc[df_1['Exchange Rate Return'] > 0.005, 'news'] = 'good_news'

# Set 'news' to 'bad_news' where 'Exchange Rate Return' is less than -0.005
df_1.loc[df_1['Exchange Rate Return'] < -0.005, 'news'] = 'bad_news'

print(df_1[df_1['news'] == 'good_news'])

'''
5. Remove the entries for which contents column has NA values. Generate and store in csv the following tables [1.5 points each]:
 a. “good_indicators” – with the 20 most common words (excluding articles, prepositions and similar connectors) associated with entries wherein “good_news” is equal to 1;
 b. “bad_indicators” – with the 20 most common words (excluding articles, prepositions and similar connectors) associated with entries wherein “bad_news” is equal to 1;
'''

# Remove entries with NA values in the 'contents' column
df_1_no_na_contents = df_1.dropna(subset=['contents'])
print(df_1_no_na_contents.head(30))

# Filter the DataFrame to include only rows where 'news' is 'good_news'
df_1_no_na_contents_good_news = df_1_no_na_contents[df_1_no_na_contents['news'] == 'good_news']
print(df_1_no_na_contents_good_news.head(30))

# Define the words to exclude
stop_words = set(stopwords.words('english'))
stop_words.add("–")
stop_words.add("also")
stop_words.add("de")

# Convert 'contents' to lowercase and split the text into words
words = df_1_no_na_contents_good_news['contents'].str.lower().str.split(expand=True).stack()

# Filter out the stop words
filtered_words = words[~words.isin(stop_words)]

# Count the frequency of the remaining words
word_freq = filtered_words.value_counts()

# Display the 20 most common words
print(word_freq.head(20))
word_freq.head(20).to_csv('good_indicators.csv')

## Now for the bad_news

# Filter the DataFrame to include only rows where 'news' is 'bad_news'
df_1_no_na_contents_bad_news = df_1_no_na_contents[df_1_no_na_contents['news'] == 'bad_news']
print(df_1_no_na_contents_bad_news.head(30))

# Define the words to exclude
stop_words = set(stopwords.words('english'))
stop_words.add("–")
stop_words.add("also")
stop_words.add("de")

# Convert 'contents' to lowercase and split the text into words
words = df_1_no_na_contents_bad_news['contents'].str.lower().str.split(expand=True).stack()

# Filter out the stop words
filtered_words = words[~words.isin(stop_words)]

# Count the frequency of the remaining words
word_freq = filtered_words.value_counts()

# Display the 20 most common words
print(word_freq.head(20))
word_freq.head(20).to_csv('bad_indicators.csv')