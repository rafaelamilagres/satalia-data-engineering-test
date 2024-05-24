# Databricks notebook source
from pyspark.sql import SparkSession, functions as F
from etl.network import NetworkProcessor
from etl.visits import VisitsProcessor

spark = SparkSession.builder.getOrCreate()

# COMMAND ----------

base_path: str = "abfss://stfsmdata@stfsmdata.dfs.core.windows.net/"
landing_path: str = f"{base_path}landing/visits/"
raw_path: str = f"{base_path}raw/visits/"
TABLE_LANDING_VISITS: str = "fsm.landing.visits"
TABLE_RAW_NETWORK: str = "fsm.raw.network"
TABLE_RAW_VISITS: str = "fsm.raw.visits"
TABLE_PROCESSED_NETWORK: str = "fsm.processed.network"
TABLE_PROCESSED_VISITS: str = "fsm.processed.visits"
TABLE_PROCESSED_VISIT_NOTES: str = "fsm.processed.visit_notes"

# COMMAND ----------

network_processor = NetworkProcessor(spark, TABLE_RAW_NETWORK, TABLE_PROCESSED_NETWORK)

network_processor.process()

# COMMAND ----------

visits_processor = VisitsProcessor(spark, landing_path, raw_path, TABLE_RAW_VISITS, TABLE_LANDING_VISITS,
                                   TABLE_PROCESSED_VISITS, TABLE_PROCESSED_VISIT_NOTES)
visits_processor.process()
