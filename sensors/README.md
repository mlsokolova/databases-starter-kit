Gather laptop sensor metrics  
If you want to get some practice in Spark Streamong in addition to the databases features.  
Steps:  
1. Install and setup tools and drivers for the monitoring of sensors
```
sudo dnf install lm_sensors  
sensors-detect
```
2. Download Apache Spark `https://spark.apache.org/downloads.html` and unpack it  
```
mkdir spark
tar  -xzvf spark-3.5.0-bin-hadoop3.tgz --strip-components=1 -C spark
```
3. Copy PostgreSQL JDBC Driver into Spark $CLASSPATH  
`cp ../gui-clients/jdbc/postgresql-42.7.1.jar ./spark/jars/`
4. Run Spark Master and Spark Worker  
```
cd spark/sbin
./start-master.sh
./start-worker.sh spark://rockmashine:7077
```
5. Check Spark Web UI URL  
`http://localhost:8080/`
6. Run minikube cluster with PostgreSQL [see here](https://github.com/mlsokolova/databases-starter-kit/tree/main/postgres#readme)  
7. Run TCP socket  
`nc -lk --broker 9999`
8. Set $POSTGRES_PASSWORD environment variable  
9. Run Spark job  
`./spark/bin/spark-submit --master spark://rockmashine:7077 ./task.py localhost 9999`

10. In order to send data of CPU temperature sensor  to TCP socket, run script gather-chip-sensor-data-to-tcp-socket.sh with the following parameters:  
1 - chip  
2 - port  
3 - host  
4 - interval in seconds  
Example:  
`./gather-chip-sensor-data-to-tcp-socket.sh coretemp-isa-0000 9999 localhost 5`  

  
refs:  
https://spark.apache.org/docs/latest/streaming-programming-guide.html#input-dstreams-and-receivers  
