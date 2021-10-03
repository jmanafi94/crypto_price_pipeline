README

This is a serverless ETL pipeline that collects hourly crypto prices using AWS Lambda for the top 100 cryptocurrencies. The data is collected thorugh the coincap API and transformed into a csv with a format that will be more suitable to time series forecasting. It uses the requests library so will need to be zipped with the requests package for deployment.

CSV FORMAT: \
  TIME, coin1, coin2, coin3,... coin100 \
  TIMESTAMP, price1, price2, price3,... price100 


The data is then uploaded into a s3 bucket with the following directory schema: \
  BUCKETNAME/raw/{year}/{month}/{day}/{timestamp} 

The intent of this data is to use the hourly prices to predict short term trends in crypto prices for a future project.
