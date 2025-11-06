```
Aleksandr@Alexandr ~ % kubectl port-forward -n monitoring svc/loki 3100:3100 &
[1] 56934
Aleksandr@Alexandr ~ % Forwarding from 127.0.0.1:3100 -> 3100
Forwarding from [::1]:3100 -> 3100
Aleksandr@Alexandr ~ % curl http://localhost:3100/ready
Handling connection for 3100
ready
Aleksandr@Alexandr ~ % curl -s http://localhost:3100/loki/api/v1/labels | jq .
Handling connection for 3100
{
  "status": "success",
  "data": [
    "app",
    "component",
    "container",
    "filename",
    "instance",
    "job",
    "namespace",
    "node_name",
    "pod"
  ]
}
```
