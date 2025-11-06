```
Aleksandr@Alexandr ~ % kubectl exec -it $(kubectl get pods -l app=gateway -o name) -- python3 -c "
import httpx
try:
    response = httpx.get('http://bookservice:80', timeout=5) 
    print(f'✅ SUCCESS: Status {response.status_code}')
    print(f'Response: {response.text}')
except Exception as e:
    print(f'❌ ERROR: {e}')
"
✅ SUCCESS: Status 200
Response: {"message":"Hello, World"}
Aleksandr@Alexandr ~ % 
```
