# Databricks notebook source
# MAGIC %sql
# MAGIC USE CATALOG fsm;

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE TABLE IF NOT EXISTS fsm.landing.visits
# MAGIC USING TEXT
# MAGIC LOCATION 'abfss://stfsmdata@stfsmdata.dfs.core.windows.net/landing/visits/';
# MAGIC
# MAGIC REFRESH TABLE fsm.landing.visits;

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE TABLE IF NOT EXISTS fsm.raw.visits
# MAGIC USING TEXT
# MAGIC LOCATION 'abfss://stfsmdata@stfsmdata.dfs.core.windows.net/raw/visits/';
# MAGIC
# MAGIC CREATE TABLE IF NOT EXISTS fsm.raw.network
# MAGIC USING TEXT
# MAGIC LOCATION 'abfss://stfsmdata@stfsmdata.dfs.core.windows.net/raw/network/';
# MAGIC
# MAGIC REFRESH TABLE fsm.raw.network;
# MAGIC REFRESH TABLE fsm.raw.visits;

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE TABLE IF NOT EXISTS fsm.processed.network
# MAGIC USING DELTA
# MAGIC LOCATION 'abfss://stfsmdata@stfsmdata.dfs.core.windows.net/processed/network/';
# MAGIC
# MAGIC CREATE TABLE IF NOT EXISTS fsm.processed.visits
# MAGIC USING DELTA
# MAGIC LOCATION 'abfss://stfsmdata@stfsmdata.dfs.core.windows.net/processed/visits/';
# MAGIC
# MAGIC CREATE TABLE IF NOT EXISTS fsm.processed.visit_notes
# MAGIC USING DELTA
# MAGIC LOCATION 'abfss://stfsmdata@stfsmdata.dfs.core.windows.net/processed/visit_notes/';
# MAGIC
# MAGIC REFRESH TABLE fsm.processed.network;
# MAGIC REFRESH TABLE fsm.processed.visits;
# MAGIC REFRESH TABLE fsm.processed.visit_notes;
