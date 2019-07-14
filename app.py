import os
import subprocess

from flask import Flask
import logging
from start import BocCrawler

app = Flask(__name__)

@app.route('/')
def start():
    subprocess.run(['python', './start.py'], check=True)
    return 'OK'

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))

