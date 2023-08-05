from typing import Dict, Any

from pyspark.sql import SparkSession, DataFrame


class SparkDataFrameHelpers:
    @staticmethod
    def create_view_from_dictionary(view: str,
                                    data: [Dict[str, Any]],
                                    spark_session: SparkSession,
                                    schema=None
                                    ) -> DataFrame:
        df = spark_session.createDataFrame(data=data, schema=schema)
        df.createOrReplaceTempView(name=view)
        return df
