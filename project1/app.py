from flask import Flask, render_template, request, redirect, url_for
from scanner.crawler import Crawler
from scanner.vulnerability_scanner import VulnerabilityScanner

app = Flask(__name__)

@app.route('/')
def index():
    # just renderr the main page here
    return render_template('index.html')

@app.route('/scan', methods=['POST'])
def scan():
    # this gets the url from the form and starts the whole thingg
    target_url = request.form.get('url')
    if not target_url:
        return redirect(url_for('index'))
    
    # Initialize components
    crawler = Crawler(target_url)
    scanner = VulnerabilityScanner(target_url)
    
    # 1. Extract forms from the main page
    # In a real scanner, we would crawl recursively, but for this MVP 
    # we'll scan the target URL and any forms found there.
    forms = crawler.extract_forms(target_url)
    
    # 2. Scan found forms
    results = scanner.scan(forms, target_url)
    
    return render_template('results.html', url=target_url, results=results)

import socket

def find_free_port(start_port=5001):
    # triess to find a port if 5001 is busy so we dont crashh
    port = start_port
    while port < 6000:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(('127.0.0.1', port))
                return port
            except socket.error:
                port += 1
    return start_port

if __name__ == '__main__':
    free_port = find_free_port()
    print(f"Starting server on port {free_port}...")
    app.run(debug=True, port=free_port)
