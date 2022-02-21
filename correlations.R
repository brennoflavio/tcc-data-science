library(RSQLite)
library("plotly")
library("tidyverse")
library("ggrepel")
library("fastDummies")
library("knitr")
library("kableExtra")
library("splines")
library("reshape2")
library("PerformanceAnalytics")
library("metan")
library("correlation")
library("see")
library("ggraph")
library("nortest")
library("rgl")
library("car")
library("olsrr")
library("jtools")
library("ggstance")
library("magick")
library("cowplot")
library("beepr")
library("Rcpp")

conn <- dbConnect(RSQLite::SQLite(), "games.db")
data <- dbGetQuery(conn, "SELECT * FROM games")
data <- subset(data, select = -c(id, moves, elo_tier, file_id, evaluation, event, accuracy_ratio, inaccuracies_ratio, mistakes_ratio, blunders_ratio, greats_ratio, bests_ratio, tablebase_blunders_ratio, tablebase_greats_ratio))
data <- data[complete.cases(data),]

summary(data)

data_dummies <- dummy_columns(.data = data,
                                    select_columns = "opening",
                                    remove_selected_columns = T,
                                    remove_most_frequent_dummy = T)

data_dummies <- dummy_columns(.data = data_dummies,
                              select_columns = "time_control",
                              remove_selected_columns = T,
                              remove_most_frequent_dummy = T)
                              
summary(data_dummies)

data_dummies %>%
  kable() %>%
  kable_styling(bootstrap_options = "striped", 
                full_width = F, 
                font_size = 19)

model_dummies <- lm(elo ~ ., data_dummies)

summary(model_dummies)

step_model_dummies <- step(model_dummies, k = 3.841459)

summary(step_model_dummies)

sf.test(sample(x=step_model_dummies$residuals, size=1000))

data_dummies %>%
  mutate(residuos = step_model_dummies$residuals) %>%
  ggplot(aes(x = residuos)) +
  geom_histogram(color = "white", 
                 fill = "#55C667FF", 
                 bins = 15,
                 alpha = 0.6) +
  labs(x = "Resíduos",
       y = "Frequências") + 
  theme_bw()


ols_test_breusch_pagan(step_model_dummies)
summary(data)

summary(step_model_dummies)

### Predicts

predict_data <- data.frame(
  total_moves=68,
  accurate_moves=39,
  evaluation_std_dev=9.79658583509532,
  evaluation_median=3.76,
  inaccuracies=2,
  blunders=7,
  greats=4,
  bests=10,
  tablebase_blunders=0,
  tablebase_greats=0,
  opening_benoni_defense=0,
  opening_bishops_opening=0,
  opening_catalan_opening=0,
  opening_english_opening=0,
  opening_grunfeld_indian=0,
  opening_italian_game=0,
  opening_kings_indian=0,
  opening_kings_pawn_openings=0,
  opening_queens_gambit_accepted=0,
  opening_queens_pawn_openings_d7d5=0,
  opening_queens_pawn_openings_g8f6=0,
  opening_reti_opening=0,
  opening_russian_game_petroff=0,
  opening_ruy_lopez_spanish=0,
  opening_scandinavian_defence=0,
  opening_scotch_opening=0,
  opening_sicilian_defence=0,
  opening_vienna_game=0,
  time_control_bullet=0,
  time_control_classical=0,
  time_control_rapid=1
)

predict(object = step_model_dummies,
        predict_data,
        interval = "confidence", level = 0.9)
