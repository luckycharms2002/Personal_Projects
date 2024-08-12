# Load necessary libraries
library(DBI)
library(RSQLite)
library(ggplot2)
library(ggrepel)  # For better label positioning

# Connect to the SQLite database and load data
conn <- dbConnect(RSQLite::SQLite(), "ufc_stats.db")
fighter_data <- dbReadTable(conn, "fighter_stats")
dbDisconnect(conn)

# Convert all relevant columns to numeric, replacing "X" with 0
numeric_columns <- c('KO_Wins', 'Sub_Wins', 'Dec_Wins', 'Sig_Strikes_Absorbed',
                     'Sig_Strikes_Landed', 'Sig_Strikes_Attempted',
                     'Sig_Strikes_from_Standing', 'Sig_Strikes_from_Clinch',
                     'Sig_Strikes_from_Ground', 'Strike_Defense', 
                     'Takedowns_Landed', 'Takedowns_Attempted', 'Takedown_Defense')

fighter_data[numeric_columns] <- lapply(fighter_data[numeric_columns], function(x) {
  x <- as.numeric(as.character(x))
  x[is.na(x)] <- 0  # Replace NA values (from "X" or other non-numeric) with 0
  return(x)
})

# Handle potential division by zero by adding a small constant to Dec_Wins
fighter_data$Dec_Wins <- fighter_data$Dec_Wins + 1  # Add 1 to avoid division by zero

# Calculate Ground Game Expertise
fighter_data$Ground_Prowess <- 
  (1.8 * fighter_data$Sub_Wins) + 
  (1.3 * fighter_data$Sig_Strikes_from_Ground) + 
  (1.3 * fighter_data$Takedowns_Landed) + 
  (fighter_data$Takedown_Defense / 100 * fighter_data$Takedowns_Attempted) +
  (fighter_data$KO_Wins) - 
  (0.75 * fighter_data$Dec_Wins) - 
  (0.5 * fighter_data$Sig_Strikes_Absorbed)

# Calculate Standup Game Expertise
fighter_data$Standup_Prowess <- 
  (1.8 * fighter_data$KO_Wins) + 
  (1.3 * fighter_data$Sig_Strikes_from_Standing) + 
  (1.3 * fighter_data$Sig_Strikes_from_Clinch) +
  (1.5 * fighter_data$Strike_Defense) - 
  (0.75 * fighter_data$Dec_Wins) - 
  (0.5 * fighter_data$Sig_Strikes_Absorbed)


# Create Scatter Plot with labels
ggplot(fighter_data, aes(x = Ground_Prowess, y = Standup_Prowess, label = fighter_name)) +
  geom_point(size = 4, color = "blue", alpha = 0.7) +
  geom_text_repel(size = 3.5, max.overlaps = Inf) +  # Use ggrepel to avoid overlap
  labs(title = "UFC Fighters: GOAT Debate",
       x = "Ground Game Prowess",
       y = "Standup Game Prowess") +
  theme_minimal()
