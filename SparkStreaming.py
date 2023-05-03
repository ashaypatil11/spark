# -*- coding: utf-8 -*-
"""
Created on Sat Apr 15 15:07:32 2023

@author: Aashay Patil
"""
from pyspark.sql import SparkSession
from pyspark.sql.functions import *

# Create the SparkSession
spark = SparkSession.\
builder.\
appName("sparkstream").\
getOrCreate()

# Define input sources
lines = (spark\
.readStream.format("socket")\
.option("host", "localhost")\
.option("port", 9999)\
.load())

# Transform data
words = lines.select(split(col("value"), "\\s").alias("word"))

# Get the count of published words
counts = words.groupBy("word").count()

# Define the checkpoint directory
checkpointDir = "C:/checkpoint/"

# Start streaming defining the necessary configurations
streamingQuery = (counts
.writeStream
.format("console")
.outputMode("complete")
.trigger(processingTime="1 second")
.option("checkpointLocation", checkpointDir)
.start())
streamingQuery.awaitTermination()