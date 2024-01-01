#!/usr/bin/env python3

from pyspark.conf import SparkConf
from pyspark.sql import SparkSession
from pyspark.streaming import StreamingContext
from pyspark.sql import functions as F
from pyspark.sql.types import *
from pyspark.sql.functions import from_json
import json
import os

jar_path = "/home/masha/projects/databases-collection/databases-starter-kit/gui-clients/jdbc/"
postgres_jdbc_lib = "postgresql-42.7.1.jar"
spark_master_url = "spark://rockmashine:7077"

def extract_sensors(str):
    print(str)
    data_json = json.loads(str)
    sys_keys = ["ts","hostname"]
    res = []
    sys_dict={}
    for sysinfo in sys_keys:
          sys_dict[sysinfo] = data_json[sysinfo]
    print(sys_dict)
    for chip in data_json.keys():
         if chip not in sys_keys:
            sys_dict["chip"] = chip
            for sensor in data_json[chip].keys():
                if type(data_json[chip][sensor]) == dict:
                    metrics_dict = sys_dict.copy()
                    metrics_dict["sensor"] = sensor
                    for  metric in data_json[chip][sensor].keys():
                         if metric.endswith("input"):
                            metrics_dict["input_value"] = data_json[chip][sensor][metric]
                            res.append(metrics_dict)
    print(sys_dict)
    return(res)

extractSensorsUDF = F.udf(lambda x: extract_sensors(x),ArrayType(MapType(StringType(),StringType())))

#schema = ArrayType(StructType(
#   fields = [
#      StructField("hostname", StringType(), True),
#]))

#spark = SparkSession.builder.appName("sensors-data").getOrCreate()
spark_conf = SparkConf().setAppName("tst")\
                      .setMaster(spark_master_url)\
                      .set("spark.sql.repl.eagerEval.enabled", True)\
                      .set("spark.jars", jar_path + postgres_jdbc_lib)
spark = SparkSession.builder.config(conf=spark_conf).getOrCreate()
spark.sparkContext.setLogLevel('WARN')


## Считываем и распаковываем json-сообщения
input_stream = spark \
  .readStream \
  .format("socket") \
  .option("host", "localhost") \
  .option("port", "9999") \
  .load()\
  .selectExpr("CAST(value as string)")\
  .select(extractSensorsUDF(F.col("value")).alias("value"))\
  .withColumn("value",F.explode('value'))\
  .select(F.col("value.hostname")\
         ,F.from_unixtime(F.col("value.ts")).cast("timestamp").alias("ts")\
         ,"value.chip"\
         ,"value.sensor"\
         ,F.col("value.input_value").cast("float").alias("input_value")\
         )


def foreach_batch_function(df, epoch_id):
    jdbc_options = {
                 "url":"jdbc:postgresql://192.168.49.2:5432/mydb",
                 "driver": "org.postgresql.Driver",
                 "user": "postgres",
                 "password": os.environ["POSTGRES_PASSWORD"],
                 "dbtable": "sensors"
               }
    df.write.mode("append").format("jdbc").options(**jdbc_options).save()               
    

#output_stream = input_stream\
#               .writeStream \
#               .format("console")\
#               .outputMode("append")\
#               .start()

output_stream = input_stream\
               .writeStream \
               .foreachBatch(foreach_batch_function)\
               .start()

output_stream.awaitTermination()
