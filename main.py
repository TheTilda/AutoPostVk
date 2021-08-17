from flask import *
import configparser
import subprocess
import sys
import os
import glob
from time import sleep
import vk
import urllib.request
import pafy
import youtube_dl
import time
from datetime import datetime
import pytz
import json
import threading
from threading import Thread
from flask_basicauth import BasicAuth



'''
#Загрузка поста который был 1000 постов назад
post = vk_api.wall.get(domain=get_channel, offset=offset, filter='owner', v = '5.131')
list_link = post['items']#[0]['attachments'][0][post['items'][0]['attachments'][0]['type']]['image'][-1]['url']
img = requests.get(list_link)
img_file = open('image.jpg', 'wb')
img_file.write(img.content)
img_file.close()
message = post['items'][0]['text']
'''
def start():
	subprocess.Popen(f"python script.py")



app = Flask(__name__, static_folder='static')
app.config['BASIC_AUTH_USERNAME'] = 'test'
app.config['BASIC_AUTH_PASSWORD'] = 'test'

basic_auth = BasicAuth(app)

@app.route('/')
@basic_auth.required
def main():
	return render_template('main.html')
@app.route('/upload/<bool>')
def log(bool):
	return 'test'
@app.route('/start')
@basic_auth.required
def start_script():
	start()
	return 'Succes <a href="/">Назад</a>'
@app.route('/edit', methods=['GET', 'POST'])
@basic_auth.required
def edit():
	with open("config.json", "r") as read_file:
		config = json.load(read_file)

	if request.method == 'GET':
		return render_template('index.html',  config=config, lists_time=str(config['list_time']).replace(',', '').replace('[', '').replace(']', '').replace("'", ""))

	else:
		config['vk_key'] = request.form.get('vk_key')
		config['group_id'] = int(request.form.get('group_id'))
		config['get_channel'] = request.form.get('get_channel')
		config['offset'] = request.form.get('offset')
		config['list_time'] = request.form.get('list_time').replace('[', '').replace(']', '').replace("'", "").split()
		with open("config.json", "w") as write_file:
			json.dump(config, write_file)
		return render_template('index.html',  config=config, lists_time=str(config['list_time']).replace(',', '').replace('[', '').replace(']', '').replace("'", ""))

if __name__ == "__main__":
    #db.create_all()
    
    app.run(host='0.0.0.0',debug=True)