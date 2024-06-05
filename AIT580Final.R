# VISHAL ORSU // AIT580 Final Project // Harry.J.Foxwell //
# Load & Read csv
# Load the dataset
library(ggplot2)
data <- read.csv("D:\\RWorkshop\\Cleaned_Real_Estate_Sales_2001-2020_GL.csv")
head(data)
data.info()
#=======================Univariate Analysis of NOIR Type========================
# Specify data types
data$Town <- as.factor(data$Town) # Nominal
data$Sale.Rankings <- as.factor(data$Sale.Rankings) # Ordinal
data$Longitude <- as.numeric(data$Longitude) # Interval
data$Latitude <- as.numeric(data$Latitude) # Interval
data$Sales.Ratio <- as.numeric(data$Sales.Ratio) # Ratio

#1 Univariate analysis of Sale Rankings (Ordinal):
# Bar plot of Sale Rankings
ggplot(data, aes(x = Sale.Rankings, fill = Sale.Rankings)) +
  geom_bar() +
  ggtitle("Bar Plot of Sale Rankings") +
  xlab("Sale Rankings") +
  ylab("Frequency") +
  scale_fill_brewer(palette = "Set2")


#2 Univariate analysis of Longitude and Latitude (Interval):
# Histogram of Longitude
ggplot(data, aes(x = Longitude, fill = "khaki")) +
  geom_histogram(bins = 50) +
  ggtitle("Histogram of Longitude") +
  xlab("Longitude") +
  ylab("Frequency")+
  scale_fill_identity()


# Histogram of Latitude
ggplot(data, aes(x = Latitude, fill = "Khaki")) +
  geom_histogram() +
  ggtitle("Histogram of Latitude") +
  xlab("Latitude") +
  ylab("Frequency") +
  scale_fill_identity()

#3 Univariate analysis of Sales Ratio (Ratio):
# Summary statistics of Sales Ratio
summary(data$Sales.Ratio)

# Box Plot
ggplot(data, aes(x = "", y = Sales.Ratio)) +
  geom_boxplot() +
  ggtitle("Boxplot of Sales Ratio") +
  ylab("Sales Ratio")

#4 Univariate analysis of Top 20 Town(Nominal)
# Create a table of frequency counts for Town
town_counts <- table(data$Town)

# Sort the table in descending order and extract the top 20 rows
top_towns <- head(sort(town_counts, decreasing = TRUE), 20)

# Create a bar chart of the top 20 towns
ggplot(data.frame(Town = names(top_towns), Freq = as.numeric(top_towns)), aes(x = Town, y = Freq)) +
  geom_bar(stat = "identity", fill = "steelblue") +
  ggtitle("Top 20 Towns") +
  xlab("Town") +
  ylab("Frequency") +
  theme(axis.text.x = element_text(angle = 90, hjust = 1, size = 8, color = "darkblue"), 
        axis.text.y = element_text(size = 8)) +
  geom_text(aes(label = Freq), vjust = -0.5, size = 3)+
  ylim(0,36000)




#=============================Clustering========================================



library(clustMixType)

# Select relevant columns for clustering
df_cluster <- data[, c("Assessed.Value", "Sale.Amount", "Sales.Ratio", "Town")]

# Convert categorical variable to factor
df_cluster$Town <- as.factor(df_cluster$Town)

# Define distance/similarity measure for numerical and categorical variables
num_dist <- "euclidean"
cat_dist <- "jaccard"

# Perform K-prototypes clustering
set.seed(123)
kp <- kproto(df_cluster, k = 3, num.rounds = 10, lambda = 0.5, 
             diss = list(numerical = num_dist, categorical = cat_dist))

# View clustering results
kp$clustering



#------------plot Clustering kmeans

# Load required packages
library(dplyr)
library(ggplot2)
library(cluster)

# Perform k-means clustering with k=3
set.seed(123)
k <- kmeans(data[,c("Assessed.Value", "Sale.Amount", "Sales.Ratio")], centers = 3)

# Add cluster assignment to data frame
data$cluster <- k$cluster

# Remove outliers
data_filtered <- data %>% 
  filter(!is.na(Sales.Ratio)) %>% # Remove rows with missing values
  filter(Sales.Ratio <= quantile(Sales.Ratio, 0.99)) # Remove top 1% of Sales Ratio values

# Plot k-means clusters
ggplot(data_filtered, aes(x = Assessed.Value, y = Sale.Amount, color = as.factor(cluster))) +
  geom_point() +
  ggtitle("K-Means Clustering (k=3)") +
  xlab("Assessed Value") +
  ylab("Sale Amount") +
  theme_bw()


#===============================Geodistribution===============================
# Geographic Distribution of Real Estate Sales

# Create a subset of the data for the desired columns
data_subset <- data[, c("List Year", "Sale Amount", "Assessed Value")]

# Group the data by year and calculate the sum of sales amounts for each year
sales_volume <- aggregate(data_subset$`Sale Amount`, by = list(data_subset$`List Year`), sum)

# Group the data by year and calculate the mean of assessed values for each year
sales_prices <- aggregate(data_subset$`Assessed Value`, by = list(data_subset$`List Year`), mean)

# Merge the sales volume and prices data frames by year
sales_data <- merge(sales_volume, sales_prices, by = "Group.1")

# Create a time series plot of sales volumes and prices over time
ggplot(sales_data, aes(x = Group.1)) +
  geom_line(aes(y = `x`, colour = "Sales Volume")) +
  geom_line(aes(y = `y`, colour = "Sales Price")) +
  scale_y_continuous(name = "Millions of Dollars") +
  labs(title = "Real Estate Sales Volumes and Prices Over Time",
       x = "Year",
       y = "Sales Volume and Price (Millions of Dollars)",
       colour = "Legend:") +
  theme_bw()

#===========================R1
library(ggplot2)

# Create a scatter plot of assessed values vs. sale amounts
ggplot(data, aes(x = `Assessed Value`, y = `Sale Amount`)) +
  geom_point(alpha = 0.5) +
  scale_x_continuous(name = "Assessed Value",
                     labels = scales::comma) +
  scale_y_continuous(name = "Sale Amount",
                     labels = scales::comma) +
  labs(title = "Assessed Values vs. Sale Amounts",
       colour = "Year") +
  theme_bw()







#================================Map============================================
# Load necessary packages
library(ggplot2)
library(maps)
library(dplyr)
library(ggtext)


# Filter out rows with missing longitude or latitude data
data <- data %>%
  filter(!is.na(Longitude) & !is.na(Latitude))

# Create a map of Connecticut with major cities marked and labeled
ct_map <- map_data("county", "connecticut")

# Filter out data for Connecticut only
ct_data <- data %>%
  filter(Longitude > -74.3 & Longitude < -71.8 & Latitude > 40.9 & Latitude < 42.1)

# Define a vector of major cities in Connecticut
cities <- c("Hartford", "New Haven", "Bridgeport", "Stamford", "Waterbury", "Norwalk", "Danbury", "New Britain", "West Hartford", "Bristol")

# Plot the map with markers for property locations and major cities labeled
ggplot() +
  geom_polygon(data = ct_map, aes(x = long, y = lat, group = group),
               fill = "white", color = "black") +
  geom_point(data = ct_data, aes(x = Longitude, y = Latitude),
             color = "red", size = 0.5, shape = 21, fill = "white", stroke = 0.2) +
  geom_text(data = data.frame(city = cities, lon = c(-72.68, -72.929, -73.204, -73.537, -73.048, -73.406, -73.452, -72.801, -72.754, -72.945), lat = c(41.76, 41.308, 41.166, 41.053, 41.558, 41.117, 41.392, 41.671, 41.762, 41.673)),
            aes(x = lon, y = lat, label = city), color = "black", size = 4, hjust = 0.5, check_overlap = TRUE,
            family = "Arial", fontface = "bold", color = "black", halo_size = 1, halo_color = "white") +
  coord_fixed() +
  labs(title = "Real Estate Properties in Connecticut",
       x = "Longitude", y = "Latitude") +
  theme(plot.title = element_text(family = "Arial", face = "bold", size = 20, hjust = 0.5),
        plot.subtitle = element_text(family = "Arial", face = "bold", size = 14, hjust = 0.5),
        axis.title = element_text(family = "Arial", face = "bold", size = 16),
        axis.text = element_text(family = "Arial", face = "bold", size = 12),
        legend.text = element_text(family = "Arial", face = "bold", size = 12),
        legend.title = element_text(family = "Arial", face = "bold", size = 14))

#==================================Multivariate:Correlation Plot=============================================
library(corrplot)
sapply(data, class)

library(corrplot)

# select numeric columns
numeric_cols <- c("Assessed.Value", "Sale.Amount", "Gain.loss", "Sales.Ratio", "Longitude", "Latitude", "List.Year")
numeric_data <- data[, numeric_cols]

# convert to numeric data
numeric_data <- apply(numeric_data, 2, as.numeric)

# compute correlation matrix
corr <- cor(numeric_data)


# create correlation plot with title
corrplot(corr, method="color", type="full", order="hclust", 
         addCoef.col="black", tl.col="black", tl.srt=45)


#===============================Multivariate:Regrression Analyses=====================================
library(dplyr)

data_filtered <- data %>%
  filter(`Sale.Amount` < 1000000)

# Fit a linear regression model with filtered data
model <- lm(`Sale.Amount` ~ `Assessed.Value` + `Sales.Ratio`, data = data_filtered)

# View the model summary
summary(model)

ggplot(data_filtered, aes(x = Assessed.Value, y = Sale.Amount)) +
  geom_point() +
  ggtitle("Sale Amount vs. Assessed Value") +
  xlab("Assessed Value") +
  ylab("Sale Amount") +
  geom_smooth(method = "lm", se = FALSE, color = "red")
#==========================Multivarite:Scatter plot=========================================
library(dplyr)
library(ggplot2)

# Remove outliers from data
data_filtered <- data %>%
  filter(`Sale.Amount` < 1000000)

# Create scatterplot with filtered data
ggplot(data_filtered, aes(x = `Assessed.Value`, y = `Sale.Amount`)) +
  geom_point() +
  ggtitle("Sale Amount vs. Assessed Value") +
  xlab("Assessed Value") +
  ylab("Sale Amount")

#====================================Top towns with high average sale===========

# Filter for only residential properties
residential_data <- data[data$Property.Type == "Residential", ]

# Group by town and calculate mean sale amount
town_sales <- aggregate(Sale.Amount ~ Town, data = residential_data, mean)

# Sort by descending order and take top 10
top10_towns <- head(town_sales[order(-town_sales$Sale.Amount), ], 10)

# Create bar plot
ggplot(data = top10_towns, aes(x = Town, y = Sale.Amount)) +
  geom_bar(stat = "identity", fill = "steelblue") +
  coord_flip() +
  labs(title = "Average Sale Amount of Top 10 Residential Towns in Connecticut",
       x = "Town",
       y = "Sale Amount (in millions)") +
  scale_y_continuous(labels = scales::dollar_format(scale = 1e-6))





