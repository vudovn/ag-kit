from httpx import Client as SyncClient
import inspect

try:
    c = SyncClient(proxy="http://localhost:8080")
    print("Proxy argument supported")
except TypeError as e:
    print(f"Proxy argument error: {e}")

print("SyncClient signature:", inspect.signature(SyncClient.__init__))
