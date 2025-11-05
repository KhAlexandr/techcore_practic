```
Aleksandr@Alexandr ~ % minikube addons list | grep ingress
│ ingress                     │ minikube │ enabled ✅ │ Kubernetes                             │
│ ingress-dns                 │ minikube │ disabled   │ minikube                               │
Aleksandr@Alexandr ~ % kubectl get pods -n ingress-nginx  
NAME                                       READY   STATUS      RESTARTS   AGE
ingress-nginx-admission-create-g6n2r       0/1     Completed   0          4m50s
ingress-nginx-admission-patch-cbk27        0/1     Completed   2          4m50s
ingress-nginx-controller-9cc49f96f-4jg4j   1/1     Running     0          4m50s
```
