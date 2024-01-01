# databases-starter-kit  
The world of databases very diverse.  
Here a zoopark under herding on minikube.  

Folders:  
- db-runtime: persistent volume for the data of databases  
- scilla:  
  ScillaDB: database with the Cassandra architecture that rewrited from Java to C++  
- mongoDB
  Extremely popular NoSQL database  
- MySQL  
- PostgreSQL  
- sensors: how to load sensor data that is on your laptop into PostgreSQL using the tcp socket and Apache Spark Structured streaming  

Tools:
- kubectl: https://kubernetes.io/docs/tasks/tools/install-kubectl-linux/#install-kubectl-binary-with-curl-on-linux  


Howto run it:  
```
minikube start --extra-config=apiserver.service-node-port-range=3000-61616 --mount --mount-string=$PWD/db-runtime:/db-runtime --alsologtostderr --v=8 --driver=docker ;  
./helm install elasticsearch elastic/elasticsearch --set service.type=NodePort,replicas=1,minimumMasterNodes=1 --namespace elastic --create-namespace -f elastic/elastic-values.yaml
```   

cheatsheet:  

```
#Log into the minikube environment  
minikube ssh  
#Run minikube dashboard
minikube dashboard
#describe pod  
./kubectl describe pods -n scylla  
#restart deployment
./kubectl rollout restart deployment mongo-express -n mongodb  
# Displays the contents of the values.yaml file  
./helm show values elastic/elasticsearch  
#delete helm chart
./helm delete elasticsearch -n elastic
#curl elastic
curl -H "Authorization: Basic 9SvYFxU3WNoWT3si" -XGET "https://localhost:9200/_cluster/health
#get exact container name from deployment description
./kubectl get pods -n mongodb --selector app=mongodb --output jsonpath={.items[0].metadata.name}
```
refs:
https://github.com/elastic/helm-charts/blob/main/elasticsearch/README.md
https://github.com/elastic/helm-charts/blob/main/elasticsearch/values.yaml

