from pyspark.sql import SparkSession, DataFrame, functions as F
import sys
sys.path.append("etl")
from utils.utils import drop_file_from_path
from utils.schemas import Schemas

class VisitsProcessor:
    def __init__(self, spark: SparkSession, path_landing: str, path_raw: str, table_raw: str, table_landing: str, table_processed_visits: str, table_processed_visit_notes: str):
        self.spark = spark
        self.table_landing = table_landing
        self.path_raw = path_raw
        self.path_landing = path_landing
        self.table_raw = table_raw
        self.table_processed_visits = table_processed_visits
        self.table_processed_visit_notes = table_processed_visit_notes

    def load_landing_to_raw(self):
        df: DataFrame = self.spark.read.table(self.table_landing)
        if not df.isEmpty():
            df.write.format("text").save(self.path_raw, mode="overwrite")
            drop_file_from_path(self.path_landing)
            return True
        else:
            return False

    def process_data(self, df):
        df_fixed: DataFrame = df.withColumn("value",F.regexp_replace(F.col("value"), ":\":", "\":"))
        df_exploded: DataFrame = df_fixed.select(F.from_json(F.col("value"), Schemas.get_visits_schema()).alias("data")) \
            .select("data.*")

        df_visit = df_exploded.withColumn("task_id",F.regexp_replace(F.col("task_id"), "TASK", "")) \
            .withColumn("node_id", F.regexp_replace(F.col("node_id"), "NODE", "")) \
            .withColumn("node_type", F.regexp_replace(F.col("node_type"), "TYPE", "")) \
            .withColumn("task_type", F.regexp_replace(F.col("task_type"), "TASK", "")) \
            .withColumn("engineer_skill_level", F.regexp_replace(F.col("engineer_skill_level"), "LEVEL", "")) \
            .withColumn("success", F.when(F.col("outcome") == "SUCCESS", True).otherwise(False)) \
            .withColumn("engineer_note", F.split(F.col("engineer_note"), " ").cast("array<int>")) \
            .drop(*["outcome"])
        
        df_visit_note = df_visit.select("task_id", "visit_id", "node_id", 
                                        F.explode(F.col("engineer_note")).alias("engineer_note_word"))

        return df_visit, df_visit_note

    def write_visit_data(self, df):
        df.write.format("delta").option("mergeSchema", "true") \
            .saveAsTable(self.table_processed_visits, mode="append")

    def write_visit_notes_data(self, df):
        df.write.format("delta").option("mergeSchema", "true") \
            .saveAsTable(self.table_processed_visit_notes, mode="append")

    def process(self):
        result = self.load_landing_to_raw()
        if result:
            df= self.spark.read.table(self.table_raw)
            df_visit, df_visit_notes = self.process_data(df)
            self.write_visit_data(df_visit)
            self.write_visit_notes_data(df_visit_notes)
