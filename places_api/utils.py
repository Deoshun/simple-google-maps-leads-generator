import json
import urllib.request
import urllib.error

def http_post(url, body, headers):
    params = json.dumps(body).encode('utf8')
    req = urllib.request.Request(url, data=params, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            response_data = response.read().decode('utf8')
            return json.loads(response_data)
    except urllib.error.HTTPError as e:
        print(f"HTTP Error {e.code}: {e.read().decode('utf8')}")
        return None
    except urllib.error.URLError as e:
        print(f"Network Error {e.reason}")
        return None
    except Exception as e:
        print(f"Unexpected Error: {e}")
        return None
