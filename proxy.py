from flask import Flask, request, jsonify
import requests
import logging

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

logging.info('Proxy application is starting...')

@app.route('/_matrix/client/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def proxy(path):
    logging.debug(f'Received {request.method} request for path: {path}')
    url = f"https://matrix-conduit-production.up.railway.app/_matrix/client/{path}"
    resp = requests.request(
        method=request.method,
        url=url,
        headers={k: v for k, v in request.headers if k != 'Host'},
        data=request.get_data(),
        params=request.args
    )
    logging.debug(f'Response status: {resp.status_code}')
    
    data = resp.json() if resp.headers.get('content-type') == 'application/json' else resp.content
    
    # Fix the field name
    if isinstance(data, dict) and 'home_server' in data:
        data['homeserver'] = data.pop('home_server')
    
    return jsonify(data) if isinstance(data, dict) else data

if __name__ == '__main__':
    logging.info('Starting proxy server on port 8008')
    app.run(port=8008)
