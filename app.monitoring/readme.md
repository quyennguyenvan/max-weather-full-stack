**Installation the Prometheus and Grafana**

**1. Install the Prometheus**

add the helm repo

```
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
```

create the namespace with name ```monitoring``` or ```other one you like it```
``` 
kubectl create namespace monitoring
export ns=monitoring
```

install the stack of prometheus
```
helm install prometheus prometheus-community/kube-prometheus-stack  --namespace $ns
```


verify the prometheus services
```kubectl get all -n $ns```


**2. Install the grafana**

add the helm repo
```
helm repo add grafana https://grafana.github.io/helm-charts
helm repo update
```

create the namespace grafana or reused the namespace monitoring
```
kubectl create namespace grafana
```

install the grafana

```
helm install grafana grafana/grafana --namespace grafana --set adminPassword='Y$ytdsy2dsfs@#D$'
```

verify the result ```kubectl get all -n grafana```


**3. Access the services**
3.1 for grafana:  
```
kubectl port-forward svc/grafana 3000:80 -n grafana
```
3.2 for prometheus
``` 
kubectl svc -n grafana
```

get the ip of service name: service/prometheus-kube-prometheus-prometheus
expose the cluster_IP:9090 

**Install the fluent bit to monitoring the kubernetes container apps**
```
helm repo add fluent https://fluent.github.io/helm-charts
helm repo update
```
install fluent bit
```
helm install fluent-bit fluent/fluent-bit \
  --namespace fluent-bit \
  --create-namespace \
  --set backend.type=lokiprovider \
  --set backend.host={{replace the svc of loki}}:3100
```

```
helm install fluent-bit fluent/fluent-bit \
  --namespace fluent-bit \
  --create-namespace \
  -f fluentbitvalue.yaml
```

install loki
=> create the value file for loki first: valueloki.yaml
contains:
```
loki:
  auth_enabled: false  # Ensure authentication is disabled
  config:
    auth_enabled: false
  image:
    tag: 2.9.3
```
install command ```helm install loki grafana/loki-stack --namespace=logging --create-namespace --values=valueloki.yaml``` to setup the loki