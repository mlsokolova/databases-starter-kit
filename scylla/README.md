Run on minikube:  
```
mkdir db-runtime/scylla;  
./kubectl apply -f scylla/namespace.yaml;  
./kubectl apply -f scylla/service.yaml;  
./kubectl apply -f scylla/deployment.yaml; 
```
GUI Tool for ScyllaDB:  
- dbeaver ce: https://dbeaver.io/download/ plus Cassandra JDBC Wrapper https://github.com/ing-bank/cassandra-jdbc-wrapper/releases  
  Cassandra driver is added using Driver Manager:  
  - Class name: com.ing.data.cassandra.jdbc.CassandraDriver  
  - URL Template: jdbc:cassandra://{host}:{port}/{keyspace}?localdatacenter={localdatacenter}  
  - URL Example: jdbc:cassandra://192.168.49.2:9042/system?localdatacenter=datacenter1  
  
FAQ:  
- What host should we use for connection to ScyllaDB?  
Answer: `minikube ip`  
- What is "local data center" in ScyllaDB/Cassandra?  
Amswer: A group of nodes related and configured within a cluster for replication purposes. For our minicube installation `localdatacenter=datacenter1`  

Create keyspace  
```
 CREATE KEYSPACE MyKeyspace
WITH REPLICATION = { 
      'class' : 'SimpleStrategy', 'replication_factor' : 1 }
```
Create table  

```
create table mykeyspace.kinneret ( id int,
                                  Survey_Date timestamp,
                                  Kinneret_Level decimal,
                                  primary key(id,Survey_Date)
                                 );
```
Load data  
```
curl "https://data.gov.il/api/3/action/datastore_search?resource_id=2de7b543-e13d-4e7e-b4c8-56071bc4d3c8&limit=10253" | jq -r '.result.records[] | [._id, .Survey_Date, .Kinneret_Level]| @csv'| ./kubectl exec -i -t -n scylla {scylladb pod name} -- cqlsh -e "copy mykeyspace.kinneret(id,Survey_Date,Kinneret_Level)  from stdin with header = false"
```
`{scylladb pod name}` is a pod name, something like scylladb-78546864f4-lq82w.  
How to get pods: `./kubectl get pods -n scylla`  

Retrieve data from table  
```
select * from mykeyspace.kinneret
```
Insert json data (I like this feature)  
```
CREATE TABLE mykeyspace.mytable(pk int PRIMARY KEY,  txt text );

insert into mykeyspace.mytable json '{ "pk" : 0, "txt" : "txt"}';

insert into mykeyspace.mytable json '{ "pk" : 1, "txt" : "txt1"}';

insert into mykeyspace.mytable json '{ "pk" : 2, "txt" : "txt2"}';

select * from mykeyspace.mytable;
```


