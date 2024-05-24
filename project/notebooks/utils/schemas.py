from pyspark.sql.types import StructField, StringType, StructType, TimestampType, IntegerType

class Schemas:
    @staticmethod
    def get_visits_schema():
        return StructType([
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
    
    @staticmethod
    def get_network_schema():
        return None