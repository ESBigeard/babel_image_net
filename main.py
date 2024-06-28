#!/usr/bin/python
# -*- coding:utf-8 -*-
""" from an OMW id, gets images from babelnet
"""

import requests
import sys
import json

def imagenet(omw_id,len_return=0):
	""" from an OMW id, gets images from babelnet. returns a list of image urls, ordonned from most to less relevant. argument len_return = how many images to return? leave at zero to return all images found"""

	#use it like this:
	#imagenet("08420278-n")
	#or
	#imagenet("08420278-n",2) to limit to 2 images

	len_return=int(len_return)

	#get a key here https://babelnet.org/register
	with open("key.txt",mode="r",encoding="utf-8") as f:
		key=f.readline().strip()

	base_url="https://babelnet.io/v9/"

	#format wordnet id
	omw_id=omw_id.strip()
	if " " in omw_id: #my usual database sometimes has something like: 09213565-n (25)
		omw_id=omw_id.split(" ")[1]
	offset,pos=omw_id.split("-")
	clean_id="wn:"+offset+pos

	#from wordnet id, gets babelnet id
	p={}
	p["id"]=clean_id #looks like wn:08420278n
	p["key"]=key
	p["source"]="WN"
	p["wnVersion"]="WN_30"
	infos=requests.get(base_url+"getSynsetIdsFromResourceID",params=p)
	json_=infos.json()
	babelid=json_[0]["id"]
	#print("babelid",babelid)

	#from babelnet id, get images url
	p={}
	p["id"]=babelid
	p["key"]=key
	infos=requests.get(base_url+"getSynset",params=p)
	json_=infos.json()
	image_urls=[]
	for i,image_data in enumerate(json_["images"]): #json_["images"] is a list
		url=image_data["url"]
		image_urls.append(url)
		if len_return:
			if i>=len_return-1:
				break
	return(image_urls)


if __name__=="__main__":

	synset=sys.argv[1].strip()
	if len(sys.argv)>2:
		len_=int(sys.argv[2])
	else:
		len_=0
	print(imagenet(synset,len_))

