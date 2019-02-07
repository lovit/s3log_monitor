import argparse
import os
from config import directory
from flask import Flask
from analyzer import listup

app = Flask('S3 access log monitor')

@app.route('/')
def main():
    logs = listup()
    if not logs:
        return 'Empty'
    html = '<br>'.join(logs)
    return html

@app.route('/test/')
def about():
    return 'Test'

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', type=str, default=None, help='IP address')
    parser.add_argument('--port', type=str, default=None, help='Port')

    args = parser.parse_args()
    host = args.host
    port = args.port

    app.run(host=host, port=port)
