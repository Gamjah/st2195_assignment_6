# Assignment 6 for LSE course ST2195

Speeches data obtained from [Speech Link](https://www.ecb.europa.eu/press/key/html/downloads.en.html)


FX data obtained from [FX Link](https://data.ecb.europa.eu/data/datasets/EXR?dataset%5B0%5D=Exchange%20Rates%20%20%28EXR%29&filterSequence=dataset&advFilterDataset%5B0%5D=Exchange%20Rates%20%20%28EXR%29)

Download the ECB speeches dataset and the daily EUR/USD reference exchange rate from the ECB Statistical Data Warehouse. Next, save them as “speeches.csv” and “fx.csv”. For the speeches.csv, please keep only the “date” and “contents” columns.

Create a GitHub repository called “st2195_assignment_6” and include two scripts (one in Python and one in R) to perform the operations described below, and a README.md file.

1. Load and merge the datasets keeping all information available for the dates in which there is a measurement in “fx.csv”. [1 point]

2. Remove entries with obvious outliers or mistakes, if any. [1.5 points]

3. Handle missing observations for the exchange rate, if any. This should be done replacing any missing exchange rate with the latest information available. Whenever this cannot be done, the relevant entry should be removed entirely from the dataset. [1.5 points]

4. Calculate the exchange rate return. Extend the original dataset with the following variables: “good_news” (equal to 1 when the exchange rate return is larger than 0.5 percent, 0 otherwise) and “bad_news” (equal to 1 when the exchange rate return is lower than -0.5 percent, 0 otherwise). [1.5 points]

5. Remove the entries for which contents column has NA values. Generate and store in csv the following tables [1.5 points each]:

    a. “good_indicators” – with the 20 most common words (excluding articles, prepositions and similar connectors) associated with entries wherein “good_news” is equal to 1;

    b. “bad_indicators” – with the 20 most common words (excluding articles, prepositions and similar connectors) associated with entries wherein “bad_news” is equal to 1;

Any observation from the common words found above?

Note that the original data should not be included in the GitHub repository, but only appropriately described and linked in the readme file.