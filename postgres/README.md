run PostgreSQL:  
```
mkdir db-runtime/postgres;
./kubectl apply -f postgres/namespace.yaml;  
./kubectl apply -f postgres/service.yaml;  
export POSTGRES_PASSWORD=<some password>  
envsubst < postgres/deployment.yaml | ./kubectl apply -f -  
```

