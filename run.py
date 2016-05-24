#!/usr/bin/env python

from flask import Flask
from flask import render_template

import subprocess

app = Flask(__name__)

def run(cmd):
	p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)
	html = ''
	while True:
	    out = p.stderr.read(1)
	    if out == '' and p.poll() != None:
	        break
	    if out != '':
	        html = html + out + '\n'

	return html

@app.route("/")
def index():
	sites = [
		{'file': 'default'}
	]
	return render_template('index.html', sites=sites)

@app.route("/nginx-config")
def nginx_config():
	return render_template('nginx_config.html')

@app.route("/create-site")
def create_site():
	return render_template('create_site.html')

@app.route("/save-site")
def save_site():
	return 'Saved'

@app.route("/start-nginx")
def start_nginx():
	output = subprocess.check_output("service nginx start", shell=True)
	return output.replace('\n', '<br>')

@app.route("/stop-nginx")
def stop_nginx():
	output = subprocess.check_output("service nginx stop", shell=True)
	return output.replace('\n', '<br>')

@app.route("/reload-nginx")
def reload_nginx():
	output = subprocess.check_output("service nginx reload", shell=True)
	return output.replace('\n', '<br>')

@app.route("/test-nginx")
def test_nginx():
	output = subprocess.check_output("service nginx configtest", shell=True)
	return output.replace('\n', '<br>')

if __name__ == "__main__":
	app.run(debug=True)