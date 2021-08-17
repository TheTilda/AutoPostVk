# -*- coding: utf-8 -*-
import requests
import random
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

while True:
	# читаем конфиг
	with open("config.json", "r") as read_file:
		config = json.load(read_file)

	vk_key = config['vk_key']
	group_id = config['group_id']  # ID паблика
	get_channel = config['get_channel']
	offset = config['offset']
	lists_time = config['list_time']

	session = vk.Session(access_token=vk_key)
	vk_api = vk.API(session)
	now = datetime.now(pytz.timezone('Europe/Moscow'))

	current_time = now.strftime("%H:%M")

	if current_time in lists_time:

		post = vk_api.wall.get(domain=get_channel, offset=offset, filter='owner', v = '5.131')
		type = post['items'][0]['attachments'][0]['type']
		if type == 'photo':
			#Загрузка поста который был 1000 постов назад
			list_link = post['items'][0]['attachments'][0][type]['sizes'][-1]['url']
			print(list_link)
			
			img = requests.get(list_link)
			img_file = open('image.jpg', 'wb')
			img_file.write(img.content)
			img_file.close()
			message = post['items'][0]['text']
			pics = glob.glob('*.jpg')
			if len(pics) == 0:
				print('Нет изображений для постинга')
				exit()

			pic2post = random.choice(pics)

			url = 'https://api.vk.com/method/photos.getWallUploadServer?group_id=%s&v=5.28&access_token=%s' % (
				str(group_id), vk_key)

			resp = requests.get(url).json()['response']
			upload_url = resp['upload_url']
			files = {'file1': open(pic2post, 'rb')}
			resp = requests.post(upload_url, files=files)
			resp = resp.json()
			server = resp['server']
			photo = resp['photo']
			vkhash = resp['hash']
			sleep(0.4)
			url = 'https://api.vk.com/method/photos.saveWallPhoto?group_id=%s&server=%s&photo=%s&hash=%s&v=5.28&access_token=a03d7ce8e11da4507e1aa3d2dc235dcb782d83749ccb6dc9165dfae66d7ff17cade182eb5c0caa77df99c' % (
				group_id, server, photo, vkhash)
			resp = requests.get(url).json()['response']
			print(resp)
			resp = resp[0]
			photo_id = resp['id']
			owner_id = resp['owner_id']
			atts = 'photo%s_%s' % (owner_id, photo_id)
			sleep(0.4)
			url = f'https://api.vk.com/method/wall.post?owner_id={-group_id}&message={message}&from_group=1&attachments={atts}&v=5.28&access_token=a03d7ce8e11da4507e1aa3d2dc235dcb782d83749ccb6dc9165dfae66d7ff17cade182eb5c0caa77df99c' 
			resp = requests.get(url).json()
			print(resp)
			files = 0

			os.remove(pic2post)
			
		elif type == 'video':

			text = post['items'][0]['text']
			owner_id = post['items'][0]['attachments'][0]['video']['owner_id']
			video_id = post['items'][0]['attachments'][0]['video']['id']
			access_key = post['items'][0]['attachments'][0]['video']['access_key']

			#vk_api.wall.post(owner_id = group_id, from_group='1', message = post['items'][0]['text'], attachments=f'video{owner_id}_{video_id}_{access_key}' , v = '5.131')
			video = vk_api.video.get(owner_id=owner_id, videos=f'{owner_id}_{video_id})_{access_key}', v = '5.131')
			vid = requests.get(video['items'][0]['player'])
			
			ydl_opts = {}
			with youtube_dl.YoutubeDL(ydl_opts) as ydl:
				ydl.download([video['items'][0]['player']])
				
			pics = glob.glob('*.mp4')
			if len(pics) == 0:
				print('Нет видео для постинга')
				exit()
			pic2post = random.choice(pics)
			server = vk_api.video.save(name='Видео от паблика',is_private= 0,group_id = f'{group_id}' ,v = '5.131')
			upload_url = server['upload_url']
			files = {'file1': open(pic2post, 'rb')}
			resp = requests.post(upload_url, files=files)
			access_key = server['access_key']
			vk_api.video.add(target_id= -group_id, video_id=server['video_id'], owner_id=server['owner_id'], v = '5.131')
			vk_api.wall.post(owner_id = -group_id, from_group='1', message = text, attachments=f'video{owner_id}_{video_id}_{access_key}' , v = '5.131')
			time.sleep(5)
			files = 0


			os.remove(pic2post)
		''' 
			urllib.request.urlretrieve(video['items'][0]['player'], 'video_name.mp4')
			print('succesfull')

		'''
		try:
			requests.get('http://127.0.0.1:5000/upload/true')
			print('succesfull')
		except:
			pass
	else:
		try:

			print(current_time)
			requests.get('http://127.0.0.1:5000/upload/false')
		except:
			pass
	time.sleep(60)
