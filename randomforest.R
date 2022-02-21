library("randomForest")
library(RSQLite)


conn <- dbConnect(RSQLite::SQLite(), "games.db")
data <- dbGetQuery(conn, "SELECT * FROM games")
data <- subset(data, select = -c(id, moves, elo_tier, file_id, evaluation, event, accuracy_ratio, inaccuracies_ratio, mistakes_ratio, blunders_ratio, greats_ratio, bests_ratio, tablebase_blunders_ratio, tablebase_greats_ratio))
data <- data[complete.cases(data),]

summary(data)

rf <- randomForest::randomForest(
  elo ~ ., 
  data = data, 
  ntree = 600,
  mtry = 3, 
  importance = T)

data

### Predicts

predict_data <- data.frame(
  tier=5,
  total_moves=68,
  accurate_moves=38,
  time_control='rapid',
  evaluation_std_dev=8.88253137657059,
  evaluation_average=7.416578947368421,
  evaluation_median=2.65,
  inaccuracies=3,
  mistakes=3,
  blunders=5,
  greats=4,
  bests=9,
  tablebase_blunders=0,
  tablebase_greats=0,
  opening="french_defence"
)



predict_data

predict(object = rf,
        predict_data,
        interval = "confidence", level = 0.9)
