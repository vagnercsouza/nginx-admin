#!/usr/bin/env python

from flask import Flask
from flask import render_template

app = Flask(__name__)

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

@app.route("/start-nginx")
def start_nginx():
	return render_template('start_nginx.html')

@app.route("/stop-nginx")
def stop_nginx():
	return render_template('stop_nginx.html')

@app.route("/reload-nginx")
def reload_nginx():
	return render_template('reload_nginx.html')

@app.route("/test-nginx")
def test_nginx():
	return render_template('test_nginx.html')

if __name__ == "__main__":
	app.run(debug=True)