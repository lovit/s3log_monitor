import argparse
import os
from config import directory
from flask import Flask
from analyzer import listup

app = Flask('S3 access log monitor')
min_byte = 0

@app.route('/')
def main():
    return listup(min_byte)

@app.route('/test/')
def about():
    return 'Test'

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', type=str, default=None, help='IP address')
    parser.add_argument('--port', type=str, default=None, help='Port')
    parser.add_argument('--min_byte', type=int, default=2048, help='Min Bytes to print')

    args = parser.parse_args()
    host = args.host
    port = args.port
    min_byte = args.min_byte

    app.run(host=host, port=port)
