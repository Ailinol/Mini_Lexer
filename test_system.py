#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from http.server import HTTPServer
from server import BackendHandler
import threading
import time
import requests
import json

def test_server():
    # Start server in background
    server = HTTPServer(('127.0.0.1', 8000), BackendHandler)
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()

    time.sleep(1)  # Wait for server to start

    try:
        # Test API
        response = requests.post(
            'http://127.0.0.1:8000/api/tokenize',
            json={'source': 'program test;'},
            timeout=5
        )

        if response.status_code == 200:
            data = response.json()
            print(f"✓ API funcionando: {len(data.get('tokens', []))} tokens, {len(data.get('errors', []))} erros")
            return True
        else:
            print(f"✗ API erro: {response.status_code}")
            return False

    except Exception as e:
        print(f"✗ Erro na API: {e}")
        return False
    finally:
        server.shutdown()

if __name__ == '__main__':
    success = test_server()
    sys.exit(0 if success else 1)