# Databricks notebook source
from pyspark.sql import functions as F
from utils import utils
import importlib

importlib.reload(utils)

# COMMAND ----------

from utils.schemas import Schemas
from utils.utils import drop_file_from_path

# COMMAND ----------

base_path: str = "abfss://stfsmdata@stfsmdata.dfs.core.windows.net/"
landing_path: str = f"{base_path}landing/"
TABLE_LANDING_VISITS: str = "fsm.landing.visits"
TABLE_RAW_NETWORK: str = "fsm.raw.network"
TABLE_RAW_VISITS: str = "fsm.raw.visits"
TABLE_PROCESSED_NETWORK: str = "fsm.processed.network"
TABLE_PROCESSED_VISITS: str = "fsm.processed.visits"

# COMMAND ----------

# MAGIC %md
# MAGIC #### Network

# COMMAND ----------

df = spark.read.table(TABLE_RAW_NETWORK)

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
drop_file_from_path(f"{landing_path}visits/")

# COMMAND ----------

df = spark.read.table("fsm.raw.visits")
df_fixed = df.withColumn("value",F.regexp_replace(F.col("value"), ":\":", "\":"))
df_exploded = df_fixed.select(F.from_json(F.col("value"), Schemas.get_visits_schema()).alias("data")).select("data.*")

df_exploded = df_exploded.withColumn("task_id",F.regexp_replace(F.col("task_id"), "TASK", "")) \
    .withColumn("node_id", F.regexp_replace(F.col("node_id"), "NODE", "")) \
    .withColumn("node_type", F.regexp_replace(F.col("node_type"), "TYPE", "")) \
    .withColumn("task_type", F.regexp_replace(F.col("task_type"), "TASK", "")) \
    .withColumn("engineer_skill_level", F.regexp_replace(F.col("engineer_skill_level"), "LEVEL", "")) \
    .withColumn("success", F.when(F.col("outcome") == "SUCCESS",True).otherwise(False)) \
    .withColumn("engineer_note", F.split(F.col("engineer_note"), " ").cast("array<int>")) \
    .drop(*["outcome"])

network_df.write.format("delta").saveAsTable("fsm.processed.network", mode="append")
