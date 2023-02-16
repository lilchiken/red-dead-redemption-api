import subprocess
import requests
import time

flask = subprocess.Popen('python3 -m tests.api_tests.flask', shell=True)
time.sleep(2)
fastapi = subprocess.Popen(
    'python3 -m uvicorn tests.api_tests.fastapi:app',
    shell=True
)
time.sleep(2)
requests.get('http://127.0.0.1:1234/test')
requests.get('http://127.0.0.1:8000/docs')
subprocess.run(
    'curl -H http://127.0.0.1:8000/docs',
    shell=True
)
flask.kill()
fastapi.kill()
