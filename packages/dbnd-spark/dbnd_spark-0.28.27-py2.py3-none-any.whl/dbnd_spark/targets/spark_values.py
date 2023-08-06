from __future__ import absolute_import

import logging
import typing

import pyspark.sql as spark

from targets.value_meta import ValueMeta, ValueMetaConf
from targets.values.builtins_values import DataValueType
from targets.values.pandas_values import DataFrameValueType


if typing.TYPE_CHECKING:
    from typing import Tuple, Optional, Dict, Any


logger = logging.getLogger(__name__)


class SparkDataFrameValueType(DataValueType):
    type = spark.DataFrame
    type_str = "Spark.DataFrame"
    support_merge = False

    config_name = "spark_dataframe"

    def to_signature(self, x):
        id = "rdd-%s-at-%s" % (x.rdd.id(), x.rdd.context.applicationId)
        return id

    def to_preview(self, df, preview_size):  # type: (spark.DataFrame, int) -> str
        return (
            df.limit(1000)
            .toPandas()
            .to_string(index=False, max_rows=20, max_cols=1000)[:preview_size]
        )

    def get_value_meta(self, value, meta_conf):
        # type: (spark.DataFrame, ValueMetaConf) -> ValueMeta

        if meta_conf.log_schema:
            data_schema = {
                "type": self.type_str,
                "columns": list(value.schema.names),
                "dtypes": {f.name: str(f.dataType) for f in value.schema.fields},
            }
        else:
            data_schema = None

        if meta_conf.log_preview:
            data_preview = self.to_preview(value, meta_conf.get_preview_size())
        else:
            data_preview = None

        if meta_conf.log_stats:
            data_schema["stats"] = self.to_preview(
                value.summary(), meta_conf.get_preview_size()
            )

        if meta_conf.log_size:
            data_schema = data_schema or {}
            rows = value.count()
            data_dimensions = (rows, len(value.columns))
            data_schema.update(
                {
                    "size": int(rows * len(value.columns)),
                    "shape": (rows, len(value.columns)),
                }
            )
        else:
            data_dimensions = None

        df_stats, histograms = None, None
        if meta_conf.log_df_hist:
            df_stats, histograms = self.get_histograms(value)

        return ValueMeta(
            value_preview=data_preview,
            data_dimensions=data_dimensions,
            data_schema=data_schema,
            data_hash=self.to_signature(value),
            descriptive_stats=df_stats,
            histograms=histograms,
        )

    def get_histograms(self, df):
        # type: (spark.DataFrame) -> Tuple[Optional[Dict[Dict[str, Any]]], Optional[Dict[str, Tuple]]]
        try:
            return DataFrameValueType.get_histograms(df.toPandas())
        except Exception:
            logger.exception("Error occured during histograms calculation")

    def support_fast_count(self, target):
        from targets import FileTarget

        if not isinstance(target, FileTarget):
            return False
        from targets.target_config import FileFormat

        return target.config.format == FileFormat.parquet
