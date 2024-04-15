# sqlalchemy-challenge

The purpose of the included notebook was to use SQLAlchemy to retrieve filtered data from the provided
weather data.  Pandas was used to organize and summarize the queried data while Matplotlib was used to
generate visualizations.

The resulting summaries and figures provide broad analyses of the weather patterns in Hawaii.  Additional
specific queries can be made in the future to predict weather trends and pinpoint ideal dates to visit
the islands.

## Climate App

In this section of the exercise, the provided data was used to design a Flask API which would return
weather data through static and dynamic routes.  The static routes can be used to return precipitation
data, the dates that precipitation data was collected on, the stations where data was collected, and
temperature data collected in the last year of this study.  The dynamic routes were designed to receive
dates via user input and provide temperature data based on those dates.