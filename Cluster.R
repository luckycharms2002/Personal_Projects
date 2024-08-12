# Load necessary libraries
library(DBI)
library(RSQLite)
library(ggplot2)
library(cluster)
library(ggrepel)  # New library for better label positioning

# Connect to the SQLite database and load data
conn <- dbConnect(RSQLite::SQLite(), "ufc_stats.db")
fighter_data <- dbReadTable(conn, "fighter_stats")
dbDisconnect(conn)

# Debugging: Print the initial fighter_data to verify fighter names
cat("Initial fighter_data:\n")
print(fighter_data)

# Store fighter names
fighter_names <- fighter_data$fighter_name

# Remove the fighter_name column for numeric operations
fighter_data <- fighter_data[ , !(names(fighter_data) %in% c("fighter_name"))]

# Convert all columns to numeric, replacing non-numeric values with NA
numeric_columns <- c('KO_Wins', 'Sub_Wins', 'Sig_Strikes_Landed', 'Sig_Strikes_Attempted',
                     'Sig_Strikes_from_Standing', 'Sig_Strikes_from_Clinch',
                     'Sig_Strikes_from_Ground', 'Strike_Defense', 
                     'Takedowns_Landed', 'Takedowns_Attempted', 'Takedown_Defense')

fighter_data[numeric_columns] <- lapply(fighter_data[numeric_columns], function(x) as.numeric(as.character(x)))

# Check for and remove rows with NA values introduced by coercion
fighter_data <- na.omit(fighter_data)

# Ensure fighter_names only contains the rows left after na.omit
fighter_names <- fighter_names[1:nrow(fighter_data)]

# Scale the metrics
normalized_metrics <- scale(fighter_data[numeric_columns])

# Perform PCA
pca_result <- prcomp(normalized_metrics, center = TRUE, scale. = TRUE)

# Get the PCA results for the first two principal components
pca_data <- as.data.frame(pca_result$x[, 1:2])
colnames(pca_data) <- c("PC1", "PC2")

# Add the PCA results back to the fighter data
fighter_data <- cbind(fighter_data, pca_data)

# Add the fighter names back as a column
fighter_data$fighter_name <- fighter_names

# Perform K-means clustering with 2 clusters for Ground vs Standup
set.seed(123)
kmeans_result <- kmeans(pca_data, centers = 2, nstart = 25)

# Add the cluster assignment back to the fighter data
fighter_data$cluster <- as.factor(kmeans_result$cluster)

# Manually label clusters as "Ground" or "Standup" based on domain knowledge or visual inspection
fighter_data$style <- ifelse(fighter_data$cluster == 1, "Ground", "Standup")

# Visualize the PCA results with clustering and label the points with fighter names using ggrepel
ggplot(fighter_data, aes(x = PC1, y = PC2, color = style)) +
  geom_point(size = 4, alpha = 0.7) +
  geom_text_repel(aes(label = fighter_name), size = 2, max.overlaps = Inf) +  # Use ggrepel to avoid overlap
  labs(title = "PCA of UFC Fighters (Ground vs Standup)",
       x = "Principal Component 1",
       y = "Principal Component 2",
       color = "Fighting Style") +
  theme_minimal() +
  scale_color_manual(values = c("Ground" = "blue", "Standup" = "red")) +  # Customize colors if desired
  theme(legend.position = "bottom")

# Output the fighter legend
cat("Fighter Legend:\n")
for (i in 1:nrow(fighter_data)) {
  cat(fighter_data$fighter_name[i], "\n")
}
