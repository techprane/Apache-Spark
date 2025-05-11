from pyspark.sql import SparkSession
from pyspark.sql.functions import window, col

spark = (SparkSession.builder
         .appName("IoTStreamingDemo")
         .getOrCreate())

# 1. Read JSON files as streaming source
df = (spark.readStream
      .schema("device STRING, timestamp STRING, temperature DOUBLE, humidity DOUBLE")
      .option("maxFilesPerTrigger", 1)         # simulate throttling
      .json("/opt/spark/data/iot_stream"))

# 2. Parse timestamp and watermarks
df2 = (df.withColumn("event_time", col("timestamp").cast("timestamp"))
         .withWatermark("event_time", "1 minute"))

# 3. Run a tumbling window aggregation: avg temp & humidity per device per 10s
agg = (df2.groupBy(
    window(col("event_time"), "10 seconds"),
    col("device"))
    .agg(
    {"temperature": "avg", "humidity": "avg"}
)
    .select("window.start", "window.end", "device",
            col("avg(temperature)").alias("avg_temp"),
            col("avg(humidity)").alias("avg_hum"))
    .orderBy("window.start"))

# 4. Output to console for demo
query = (agg.writeStream
         .outputMode("update")
         .format("console")
         .option("truncate", False)
         .start())

query.awaitTermination(60)  # run for 60 seconds
