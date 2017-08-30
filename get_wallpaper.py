#D:\Python\Python35\python
# -*- coding:utf-8 -*-

import re,sys,os,time,logging

import urllib.request

"""
by ds17
Github: https://github.com/ds17/
E-mail: ingsed@outlook.com
"""
log_dir='D:\\WallPaper\\BingWallpaper\\3.5bing.log'
logging.basicConfig(filename=log_dir,level=logging.INFO)

file_dir='D:\\WallPaper\\BingWallpaper'
now_time=time.strftime('%Y%m%d%H%M%S')

# 通过os.walk遍历壁纸文件夹下所有文件的文件名并放到list中
e_name_t=[]
for root,dirs,files in os.walk(file_dir):
	if not(len(files)==0):
		for pic_name in files:
			if '_1920x1080.jpg' in pic_name:
				name_right=pic_name.find('_')
				e_name=pic_name.replace(pic_name[:name_right+1],'')
				e_name_t.append(e_name)

#通过logging永久保存爬取的文件名，在每次运行的时候读取文件名并放入list中。
log=open(log_dir,'r')
print('Reading Log...')
# time.sleep(2)
names=log.read()
e_name_l=re.findall(r'INFO:root:.*：(.*.jpg)',names)		#INFO:root:已存在：KazakhstanNasa_ZH-CN9791985430_1920x1080.jpg
e_name_l=set(e_name_l)		#将e_name_l从list转换为set，删除log中重复的条目，提高性能
# print('e_name_l SET:',e_name_l)

def get_bing_backpic():
	i=8
	url= 'http://cn.bing.com/HPImageArchive.aspx?format=js&idx=0&n='+ str(i)
	html=urllib.request.urlopen(url).read()
	if html=='null':
		print('获取页面错误')
		sys.exit(-1)
	html=html.decode('utf-8')
	reg=re.compile('"url":"(.*?)","urlbase"',re.S)
	text = re.findall(reg,html)
	# logging.warning([pic_url for pic_url in text])
	text_no=0
	
	for imgurl in text :
		imgurl='http://cn.bing.com'+imgurl
		right = imgurl.rindex('/')
		name = imgurl.replace(imgurl[:right+1],'')
		if name in e_name_t:
			logging.info('已存在：' + name)
			print ('已存在：' + name)
		elif name in e_name_l:
			logging.info('已爬过，被删除：'+name)
			print('已爬过，被删除：'+name)
		else:
			save_name=now_time+'_'+name
			savepath = file_dir+'\\' + save_name
			urllib.request.urlretrieve(imgurl, savepath)
			logging.info('保存成功：' + name)
			print ('保存成功：'+ save_name)
		text_no=text_no+1

		if text_no==len(text):
			sleep_time=6
			print('\n'+now_time+':爬取结束。\n'+'壁纸保存路径：'+file_dir+'\n'+str(sleep_time)+'秒后跳出')
			logging.info('爬取时间：'+now_time+'\n\n')
			time.sleep(sleep_time)

get_bing_backpic()


