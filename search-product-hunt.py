#!/usr/bin/env python3

# We wrote this file. As long as you retain this notice you can do whatever you
# want with this stuff. If we meet some day, and you think this stuff is worth
# it, you can buy us a bottle of cider in return.
#       Ekaterina Klink <ekaterina.klink@gmail.com>
# 	Constantin S. Pan <kvapen@gmail.com>

# This program performs a bulk search of product hunt posts by name.
# It reads the inputs from 'queries.csv' and saves the resulting query-url
# pairs into 'urls.csv'.

import requests
import json
import csv

def call_algolia(query):
	api_key = '9670d2d619b9d07859448d7628eea5f3'
	app_id = '0H4SMABBSG'
	index_url = 'https://0h4smabbsg-dsn.algolia.net/1/indexes/Post_production'

	headers = {
		'x-algolia-api-key': api_key,
		'x-algolia-application-id': app_id,
	}

	params = {
		'query': query,
	}

	r = requests.get(index_url, headers=headers, params=params)
	return r.text

def get_post_url(j):
	if len(j['hits']) > 0:
		return j['hits'][0]['url']
	else:
		return None

with open('queries.csv') as src, open('urls.csv', 'w') as dst:
	reader = csv.reader(src)
	writer = csv.writer(dst)
	for row in reader:
		q = row[0].strip()
		raw = call_algolia(q)
		j = json.loads(raw)
		u = get_post_url(j)
		if u:
			u = "https://producthunt.com" + u
		writer.writerow((q, u))
		print("%s -> %s" % (q, u))
