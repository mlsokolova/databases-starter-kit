# databases-starter-kit  
The world of databases very diverse.  
Here a zoopark under herding on minikube.  

Folders:  
- scilla: ScillaDB  
  It's  database with the Cassandra architecture that rewrited from Java to C++  
- mongoDB
  Extremely popular NoSQL database  

Tools:
- kubectl: https://kubernetes.io/docs/tasks/tools/install-kubectl-linux/#install-kubectl-binary-with-curl-on-linux  


Howto run it:  
```
mkdir db-runtime/scylla;  
mkdir db-runtime/mongodb;  
minikube start --extra-config=apiserver.service-node-port-range=3000-61616 --mount --mount-string=$PWD/db-runtime:/db-runtime --alsologtostderr --v=8 --driver=docker ;  
./kubectl apply -f scylla/namespace.yaml;  
./kubectl get scylla/namespaces;  
./kubectl apply -f scylla/service.yaml;  
./kubectl apply -f scylla/deployment.yaml;  
./kubectl apply -f mongodb/namespace.yaml;
./kubectl apply -f mongodb/service.yaml
./kubectl apply -f mongodb/deployment.yaml
```  

minikube` and kubectl cheatsheet:  

```
#Log into the minikube environment  
minikube ssh  
#describe pod  
./kubectl describe pods -n scylla  
#restart deployment
./kubectl rollout restart deployment mongo-express -n mongodb
```

