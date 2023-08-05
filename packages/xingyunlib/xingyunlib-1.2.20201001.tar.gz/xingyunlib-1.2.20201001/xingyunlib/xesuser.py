# from calendar import c

import requests
import json
def _nice(emoji_str):
	import struct
	return ''.join(
		c if c <= '\uffff' else ''.join(chr(x) for x in struct.unpack('>2H', c.encode('utf-16be'))) for c in emoji_str)
def get_fans_info(id, lengh=None):
	id = str(id)
	# page = 1
	if lengh == None:
		lengh = (int(get_info(id)["fans"])//150)+1
	c=[]
	for x in range(lengh):
		headers = {'Content-Type': 'application/json'}
		total = json.loads(_nice(requests.get(
			f"http://code.xueersi.com/api/space/fans?user_id={id}&page={str(x+1)}&per_page=150",headers=headers).text))
		c+=total["data"]["data"]

	return c
def get_follows_info(id, lengh=None):
	id = str(id)
	page = 1
	if lengh == None:
		lengh = get_info(id)["follows"]
	headers = {'Content-Type': 'application/json'}
	total = json.loads(_nice(requests.get(
		"http://code.xueersi.com/api/space/follows?user_id=" + id + "&page=" + str(page) + "&per_page=" + str(lengh),
		headers=headers).text))
	return total["data"]["data"]
def get_info(id):
	headers = {'Content-Type': 'application/json'}
	total = json.loads(
		_nice(requests.get("http://code.xueersi.com/api/space/profile?user_id=" + str(id), headers=headers).text))[
		"data"]
	return {
		# "user_id": total["user_id"],
		"name": total["realname"],
		"slogan": total["signature"],
		"fans": total["fans"],
		"follows": total["follows"],
		"icon": total["avatar_path"]
	}
def get_user_id(id):
	id = id.split("&pid=")[1].split("&")[0]
	url = "http://code.xueersi.com/api/compilers/" + id + "?id=" + id
	headers = {'Content-Type': 'application/json'}
	a = requests.get(url=url, headers=headers)
	a = json.loads(_nice(a.text))
	# self._nice()
	return a["data"]["user_id"]
class user:
	def __init__(self, id):
		id = str(id)
		url = "http://code.xueersi.com/api/space/index?user_id=" + id
		headers = {'Content-Type': 'application/json'}
		a = requests.get(url=url, headers=headers)
		a = json.loads(_nice(a.text))
		a = a["data"]
		self.data = a
		self.works = a["works"]["total"]
		headers = {'Content-Type': 'application/json'}
		total = json.loads(_nice(requests.get(
			"http://code.xueersi.com/api/space/works?user_id=" + id + "&page=1&per_page=" + str(self.works),
			headers=headers).text))
		self.work_info = total["data"]
		self.fans = a["fans"]["total"]
		self.fans_info = get_fans_info(id, self.fans)
		self.follows = a["follows"]["total"]
		self.follows_info = get_follows_info(id, self.follows)
		self.overview = a["overview"]
		self.like_num = self.overview["likes"]
		self.view_num = self.overview["views"]
		self.work_num = self.overview["works"]
		self.favorites = self.overview["favorites"]
#nice
#
# # a = user(get_user_id(
# # 	"http://code.xueersi.com/home/project/detail?lang=code&pid=6076813&version=offline&form=python&langType=python"))
# # print(a.work_info)