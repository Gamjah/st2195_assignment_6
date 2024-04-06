library(readr)
library(dplyr)
library(tidyr)
library(stringr)
library(tm)

# Load data sets
Speeches_df <- read_delim('/Users/tiagooliveira/Dev/LSE/ST2195/st2195_assignment_6/speeches.csv', delim = '|')
fx_df <- read_delim('/Users/tiagooliveira/Dev/LSE/ST2195/st2195_assignment_6/fx.csv', delim = ',')

# Merge data sets on date
df_1 <- merge(Speeches_df, fx_df, by = 'date')

# Convert the 'US dollar/Euro (EXR.D.USD.EUR.SP00.A)' column to numeric
df_1$`US dollar/Euro (EXR.D.USD.EUR.SP00.A)` <- as.numeric(df_1$`US dollar/Euro (EXR.D.USD.EUR.SP00.A)`)

# Identify the outliers in the 'US dollar/Euro (EXR.D.USD.EUR.SP00.A)' column
outliers <- boxplot.stats(df_1$`US dollar/Euro (EXR.D.USD.EUR.SP00.A)`) $out

# Remove the outliers from the DataFrame
df_1 <- df_1[!df_1$`US dollar/Euro (EXR.D.USD.EUR.SP00.A)` %in% outliers, ]

# Forward fill to replace missing values with the latest available information
df_1 <- fill(df_1, `US dollar/Euro (EXR.D.USD.EUR.SP00.A)`, .direction = "down")

# If there are still missing values, remove those entries
df_1 <- df_1[!is.na(df_1$`US dollar/Euro (EXR.D.USD.EUR.SP00.A)`), ]

df_1$`Exchange Rate Return` <- c(0, diff(log(df_1$`US dollar/Euro (EXR.D.USD.EUR.SP00.A)`)))

# Initialize 'news' column with None
df_1$news <- NA

# Set 'news' to 'good_news' where 'Exchange Rate Return' is greater than 0.005
df_1$news[df_1$`Exchange Rate Return` > 0.005] <- 'good_news'

# Set 'news' to 'bad_news' where 'Exchange Rate Return' is less than -0.005
df_1$news[df_1$`Exchange Rate Return` < -0.005] <- 'bad_news'

# Remove entries with NA values in the 'contents' column
df_1 <- df_1[!is.na(df_1$contents), ]

# Define the words to exclude
stop_words <- stopwords("en")

# Filter the DataFrame to include only rows where 'news' is 'good_news'
df_1_good_news <- df_1[df_1$news == 'good_news', ]

## Convert 'contents' to lowercase and split the text into words
words <- str_split(tolower(df_1_good_news$contents), "\\s+")

# Unlist the words to create a vector
words_vector <- unlist(words)

# Filter out the stop words
filtered_words <- words_vector[!words_vector %in% stop_words]

# Count the frequency of the remaining words
word_freq <- table(filtered_words)

# Convert to data frame for easier manipulation
word_freq_df <- as.data.frame(table(filtered_words), stringsAsFactors = FALSE)
names(word_freq_df) <- c("Word", "Freq")

# Sort by frequency
word_freq_df <- word_freq_df[order(-word_freq_df$Freq),]

# Write the 20 most common words to a CSV file
write.csv(word_freq_df[1:20, ], file = "good_indicators.csv", row.names = FALSE)

# Now for the bad_news

## Filter the DataFrame to include only rows where 'news' is 'bad_news'
df_1_bad_news <- df_1[df_1$news == 'bad_news', ]

# Convert 'contents' to lowercase and split the text into words
words <- str_split(tolower(df_1_bad_news$contents), "\\s+")

# Unlist the words to create a vector
words_vector <- unlist(words)

# Filter out the stop words
filtered_words <- words_vector[!words_vector %in% stop_words]

# Count the frequency of the remaining words
word_freq <- table(filtered_words)

# Convert to data frame for easier manipulation
word_freq_df <- as.data.frame(table(filtered_words), stringsAsFactors = FALSE)
names(word_freq_df) <- c("Word", "Freq")

# Sort by frequency
word_freq_df <- word_freq_df[order(-word_freq_df$Freq),]

# Write the 20 most common words to a CSV file
write.csv(word_freq_df[1:20, ], file = "bad_indicators.csv", row.names = FALSE)
