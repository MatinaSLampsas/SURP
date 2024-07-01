#Housing prices
setwd("C:/Users/kalis/OneDrive/Documents/Housing_research")
library(readr)
d <- read_csv("redfin_sfh_clean.csv")
dc <- read_csv("combined_final.csv") 
View(dc)
dc$`ZIP OR POSTAL CODE`
hedonic_model <- lm(PRICE ~ BEDS + BATHS + `SQUARE FEET` + `LOT SIZE` + `HOA/MONTH` + `ZIP OR POSTAL CODE`, data = dc)
summary(hedonic_model)
hm2 <- lm(PRICE ~ BEDS, data = dc)
summary(hm2)
#problems: multicollinearity, and missing data-> from a huge dataset down to a few variables
na_count_hoa <- sum(is.na(dc$`HOA/MONTH`)); na_count_hoa
na_count_CITY <- sum(is.na(dc$CITY)); na_count_CITY
na_count_Loc <- sum(is.na(dc$LOCATION)); na_count_Loc
