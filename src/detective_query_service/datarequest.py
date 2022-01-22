import requests
import json

url = "http://alpha:8080/graphql"
query = """
    query {
        querySourceConnection() {
            xid
            host
            user
            password
            database
            db_type
        }
    }
"""

headers = {
    "Content-type": "application/json",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36"
}

r = requests.post(url, data=json.dumps({"query": query}), headers=headers)
print(r.status_code)
print(json.dumps(json.loads(r.text), indent=4))

