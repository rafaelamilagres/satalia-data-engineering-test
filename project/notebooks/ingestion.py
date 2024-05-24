# Databricks notebook source
from pyspark.sql import functions as F
from pyspark.sql.types import StructField, StringType, StructType, TimestampType, IntegerType

# COMMAND ----------

# MAGIC %md
# MAGIC #### Setup

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC USE CATALOG fsm;

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE TABLE fsm.landing.visits
# MAGIC USING TEXT
# MAGIC LOCATION 'abfss://stfsmdata@stfsmdata.dfs.core.windows.net/landing/visits/';

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE TABLE IF NOT EXISTS fsm.raw.visits
# MAGIC USING TEXT
# MAGIC LOCATION 'abfss://stfsmdata@stfsmdata.dfs.core.windows.net/raw/visits/';
# MAGIC
# MAGIC CREATE TABLE IF NOT EXISTS fsm.raw.network
# MAGIC USING TEXT
# MAGIC LOCATION 'abfss://stfsmdata@stfsmdata.dfs.core.windows.net/raw/network/';

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE TABLE IF NOT EXISTS fsm.processed.network
# MAGIC USING DELTA
# MAGIC LOCATION 'abfss://stfsmdata@stfsmdata.dfs.core.windows.net/processed/network/';
# MAGIC
# MAGIC
# MAGIC CREATE TABLE IF NOT EXISTS fsm.processed.visits
# MAGIC USING DELTA
# MAGIC LOCATION 'abfss://stfsmdata@stfsmdata.dfs.core.windows.net/processed/visits/';

# COMMAND ----------

# MAGIC %md
# MAGIC #### Network

# COMMAND ----------

df = spark.read.table("fsm.raw.network")

split_df = df.select(F.split(df.value, " ").alias("nodes"))

network_df = split_df.select(
    F.col("nodes").getItem(0).alias("node_id"), 
    F.explode(F.slice(F.col("nodes"), 2, F.size(F.col("nodes")))).alias("adjacent_node_id")
)
network_df = network_df.select(
    F.regexp_replace(F.col("node_id"), "NODE", "").alias("node_id"),
    F.regexp_replace(F.col("adjacent_node_id"), "NODE", "").alias("adjacent_node_id")
)

network_df.write.format("delta").option("overwriteSchema", "true").saveAsTable("fsm.processed.network", mode="overwrite")

# COMMAND ----------

# MAGIC %md
# MAGIC #### Visit

# COMMAND ----------

df = spark.read.table("fsm.landing.visits")
df.write.format("text").option("overwriteSchema", "true").saveAsTable("fsm.raw.visits", mode="append")
spark.sql("DROP TABLE fsm.landing.visits")

# COMMAND ----------

df = spark.read.table("fsm.raw.visits")
schema = StructType([
    StructField("task_id", StringType()),
    StructField("node_id", StringType()),
    StructField("visit_id", IntegerType()),
    StructField("visit_date", TimestampType()),
    StructField("original_reported_date", TimestampType()),
    StructField("node_age", IntegerType()),
    StructField("node_type", StringType()),
    StructField("task_type", StringType()),
    StructField("engineer_skill_level", StringType()),
    StructField("engineer_note", StringType()),
    StructField("outcome", StringType())
])
df_fixed = df.withColumn("value",F.regexp_replace(F.col("value"), ":\":", "\":"))
df_exploded = df_fixed.select(F.from_json(F.col("value"), schema).alias("data")).select("data.*")

df_exploded = df_exploded.withColumn("task_id",F.regexp_replace(F.col("task_id"), "TASK", "")) \
    .withColumn("node_id", F.regexp_replace(F.col("node_id"), "NODE", "")) \
    .withColumn("node_type", F.regexp_replace(F.col("node_type"), "TYPE", "")) \
    .withColumn("task_type", F.regexp_replace(F.col("task_type"), "TASK", "")) \
    .withColumn("engineer_skill_level", F.regexp_replace(F.col("engineer_skill_level"), "LEVEL", "")) \
    .withColumn("success", F.when(F.col("outcome") == "SUCCESS",True).otherwise(False)) \
    .withColumn("engineer_note", F.split(F.col("engineer_note"), " ").cast("array<int>")) \
    .drop(*["outcome"])

network_df.write.format("delta").option("overwriteSchema", "true").saveAsTable("fsm.processed.network", mode="append")
