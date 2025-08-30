from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/_matrix/client/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def proxy(path):
    url = f"https://matrix-conduit-production.up.railway.app/_matrix/client/{path}"
    resp = requests.request(
        method=request.method,
        url=url,
        headers={k: v for k, v in request.headers if k != 'Host'},
        data=request.get_data(),
        params=request.args
    )
    
    data = resp.json() if resp.headers.get('content-type') == 'application/json' else resp.content
    
    # Fix the field name
    if isinstance(data, dict) and 'home_server' in data:
        data['homeserver'] = data.pop('home_server')
    
    return jsonify(data) if isinstance(data, dict) else data

if __name__ == '__main__':
    app.run(port=8008)
