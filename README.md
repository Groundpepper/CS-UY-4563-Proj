# CS-UY-4563-Proj

## Data Engineering
The dataset for this project was obtained independently from Geoguessr.com; specifically, the google streetview photos (X) and their corresponding, actual latitude & longitude values (Y) were taken from single player Russia country games. Each pair of data was collected through Selenium from `geoguessr_DE.py`: Geoguessr.com has a cooldown for every game played, so the process described there was repeated many times, capturing photos in a folder named `screenshots/` and corresponding coordinate labels in `coordinates.txt`. Around one thousand data points were used for machine learning & analysis, but due to the nature of data collection for this project, results are replicable only to some extent, as photos collected from Geoguessr.com are always randomized for unpredictability. It must also be noted that this data engineering method may be outdated in the future as the usage of Selenium depends on Geoguessr webpage configuration when this project was initially developed.

## Machine Learning
