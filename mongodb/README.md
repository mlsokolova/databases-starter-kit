run mongodb:  
```
./kubectl apply -f mongodb/namespace.yaml;  
./kubectl apply -f mongodb/service.yaml  
./kubectl apply -f mongodb/deployment.yaml  
```
expose Mongo Express to localhost:  
```
./kubectl port-forward svc/mongo-express 8081:8081 -n mongodb &
```
, so Mongo Express url: http://localhost:8081/, login credentials: default (admin:pass)  
Then create database and collection using MongoExpress.  
Get exact pod name of Mongodb:  
```
mongodb_pod=`./kubectl get pods -n mongodb --selector app=mongodb --output jsonpath={.items[0].metadata.name};`
```  
Load some semi-structured json data to Mongo:  
```
lshw -json|jq .children  | ./kubectl  -n mongodb -it exec $mongodb_pod -- mongoimport -d mydatabase -c mycollection --jsonArray  
```

Playing with Mongo data:
```
echo 'show dbs'|./kubectl  -n mongodb -it exec $mongodb_pod -- mongosh  

echo $'use mydatabase\nshow collections'|./kubectl  -n mongodb -it exec $mongodb_pod -- mongosh  

echo $'use mydatabase\ndb.mycollection.find()'|./kubectl  -n mongodb -it exec $mongodb_pod -- mongosh  
```

Doc URLs:  
https://kubernetes.io/docs/tasks/inject-data-application/environment-variable-expose-pod-information/  
https://kubernetes.io/docs/concepts/workloads/pods/downward-api/#available-fields  


