# oil-well-production-analysis
## Objective
Explore and understand the oil well production dataset in order to identify patterns,
data quality issues, and potential variables useful for predictive modeling.

## Dataset
Source: [Kaggle Oil Well Production Dataset](https://www.kaggle.com/datasets/ruslanzalevskikh/oil-well)

## Data Understanding

The dataset contains operational parameters from an oil well between 2013 and 2021, including oil production, liquid production, gas production, water cut, reservoir pressure, and other operational measurements.

Initial exploration was conducted to understand the structure of the dataset, the available variables, and potential data quality issues.

## Data Preprocessing

Raw operational data from the oil well was cleaned and standardized before analysis. Column names were normalized, dates were converted to datetime format, and the cleaned dataset was stored in the data/processed directory.

## Data Cleaning
### Handling missing dates
The time series contained one missing daily observation (2015-05-31).
To ensure a consistent daily frequency, the dataset was reindexed using
a daily frequency and the missing observation was filled using linear interpolation.
This approach preserves the temporal continuity of the dataset while
introducing minimal distortion due to the very small number of missing values.




