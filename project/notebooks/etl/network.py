from pyspark.sql import DataFrame, SparkSession, functions as F

class NetworkProcessor:
    def __init__(self, spark: SparkSession, table_raw: str, table_processed: str):
        self.spark = spark
        self.table_raw = table_raw
        self.table_processed = table_processed

    def read_data(self):
        return self.spark.read.table(self.table_raw)

    def process_data(self, df):
        split_df: DataFrame = df.select(F.split(df.value, " ").alias("nodes"))

        network_df: DataFrame = split_df.select(
            F.col("nodes").getItem(0).alias("node_id"), 
            F.explode(F.slice(F.col("nodes"), 2, F.size(F.col("nodes")))).alias("adjacent_node_id")
        )
        return network_df.select(
            F.regexp_replace(F.col("node_id"), "NODE", "").alias("node_id"),
            F.regexp_replace(F.col("adjacent_node_id"), "NODE", "").alias("adjacent_node_id")
        )

    def write_data(self, df):
        df.write.format("delta").option("overwriteSchema", "true").saveAsTable(self.table_processed, mode="overwrite")

    def process(self):
        df: DataFrame = self.read_data()
        processed_df: DataFrame = self.process_data(df)
        self.write_data(processed_df)
