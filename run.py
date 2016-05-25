#!/usr/bin/env python

from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from os import listdir
from os.path import isfile, join

import subprocess

app = Flask(__name__)

config_file = '/etc/nginx/nginx.conf'
sample_site = 'sample.conf'
sites_dir = '/etc/nginx/sites-available'
enabled_sites_dir = sites_dir + '/../sites-enabled'

@app.route('/')
def index():
	files = [f for f in listdir(sites_dir) if isfile(join(sites_dir, f))]
	sites = []

	for file in files:
		sites.append({'file':file})

	return render_template('index.html', sites=sites)

@app.route('/nginx-config')
def nginx_config():
	with open(config_file) as f:
		config = f.read()
	return render_template('nginx_config.html', config=config)

@app.route('/save-nginx-config', methods=['POST'])
def save_nginx_config():
	with open(config_file, "w") as f:
		f.write(request.form['conf'])
	return redirect(url_for('index'))

@app.route('/create-site')
def create_site():
	return render_template('create_site.html')

@app.route('/save-site', methods=['POST'])
def save_site():
	name = request.form['name']

	with open(sample_site, "r") as s:
		sample = s.read()
		new_file = '%s/%s.conf' % (sites_dir, name)
		with open(new_file, "w") as f:
			f.write(sample)

	return redirect(url_for('edit_site', name=name))

@app.route('/edit-site')
def edit_site():
	name = request.args.get('name', '')
	with open('%s/%s.conf' % (sites_dir, name)) as f:
		file = f.read()
	return render_template('edit_site.html', file=file, name=name)

@app.route('/update-site', methods=['POST'])
def update_site():
	name = request.args.get('name', '')
	with open('%s/%s.conf' % (sites_dir, name), "w") as f:
		f.write(request.form['file'])
	return redirect(url_for('index'))

@app.route('/delete-site')
def delete_site():
	name = request.args.get('name', '')
	file = '%s/%s.conf' % (sites_dir, name)
	subprocess.call("rm " + file, shell=True)
	return redirect(url_for('index'))

@app.route('/enable-site')
def enable_site():
	name = request.args.get('name', '')
	file = '%s/%s.conf' % (sites_dir, name)
	link = '%s/%s.conf' % (enabled_sites_dir, name)
	print "ln %s %s" % (file, link)
	subprocess.call("ln %s %s" % (file, link), shell=True)
	return redirect(url_for('index'))

@app.route('/disable-site')
def disable_site():
	name = request.args.get('name', '')
	file = '%s/%s.conf' % (enabled_sites_dir, name)
	subprocess.call("rm " + file, shell=True)
	return redirect(url_for('index'))

@app.route('/start-nginx')
def start_nginx():
	output = subprocess.check_output('service nginx start', shell=True)
	return output.replace('\n', '<br>')

@app.route('/stop-nginx')
def stop_nginx():
	output = subprocess.check_output('service nginx stop', shell=True)
	return output.replace('\n', '<br>')

@app.route('/reload-nginx')
def reload_nginx():
	output = subprocess.check_output('service nginx reload', shell=True)
	return output.replace('\n', '<br>')

@app.route('/test-nginx')
def test_nginx():
	output = subprocess.check_output('service nginx configtest', shell=True)
	return output.replace('\n', '<br>')

if __name__ == '__main__':
	app.run(debug=True)