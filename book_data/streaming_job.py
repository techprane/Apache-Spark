from pyspark.sql import SparkSession
from pyspark.sql.functions import window, col
# Import required types
from pyspark.sql.types import StructType, StructField, StringType, DoubleType

spark = (SparkSession.builder
         .appName("IoTStreamingDemo")
         .getOrCreate())

# Define the schema using StructType
schema = StructType([
    StructField("device", StringType(), True),
    StructField("timestamp", StringType(), True),
    StructField("temperature", DoubleType(), True),
    StructField("humidity", DoubleType(), True)
])

# 1. Read JSON files as streaming source with the correct schema
df = (spark.readStream
      .schema(schema)  # Use the StructType schema
      .option("maxFilesPerTrigger", 1)
      .json("/opt/spark/data/iot_stream"))

# 2. Parse timestamp and apply watermark
df2 = (df.withColumn("event_time", col("timestamp").cast("timestamp"))
         .withWatermark("event_time", "1 minute"))

# 3. Tumbling window aggregation without orderBy
agg = (df2.groupBy(
    window(col("event_time"), "10 seconds"),
    col("device"))
    .agg(
        {"temperature": "avg", "humidity": "avg"}
)
    .select("window.start", "window.end", "device",
            col("avg(temperature)").alias("avg_temp"),
            col("avg(humidity)").alias("avg_hum"))
    # Removed orderBy to avoid streaming sorting issues
)

# 4. Output to console
query = (agg.writeStream
         .outputMode("update")
         .format("console")
         .option("truncate", False)
         .start())

try:
    # Wait for 60 seconds or manual termination
    query.awaitTermination()
except KeyboardInterrupt:
    print("Stopping query gracefully...")
finally:
    # Explicitly stop the query and Spark session
    query.stop()
    spark.stop()
