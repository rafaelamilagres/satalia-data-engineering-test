# Databricks notebook source
# MAGIC %sql
# MAGIC USE CATALOG fsm;

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE TABLE IF NOT EXISTS fsm.landing.visits
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
