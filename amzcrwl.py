#!/usr/bin/python2
import requests
import argparse
from BeautifulSoup import BeautifulSoup


query_list = ['rotes', 'gummiboot']
product_identifier = 'Kinderboot-Speedway-Friends'

user_agent = {'User-agent': 'Mozilla/5.0'}



def login(user, password):

    sessionID = ''
    return sessionID


def add_to_cart(html_product, sessionID):

	# all POST params needed
	# please don't ask me what all of this shit is
	post_data_names = ['session-id', 'ASIN', 'offerListingID', 
	'isMerchantExclusive', 'merchantID', 'isAddon', 'nodeID', 
	'sellingCustomerID', 'qid', 'sr', 'storeID', 'tagActionCode', 
	'viewID', 'rsid', 'sourceCustomerOrgListID', 'sourceCustomerOrgListItemID', 
	'wlPopCommand', 'submit.add-to-cart', 'dropdown-selection']


	# building POST request
	post_data = dict()
	soup = BeautifulSoup(html_product)
	for input_tag in soup.findAll('input'):
		name =  input_tag.get('name')
		if name is not None:
			if any(name in input_tag.get('name') for name in post_data_names):
				post_data.update({input_tag.get('name'):input_tag.get('value')})
	
	r = requests.post("https://amazon.de//gp/product/handle-buy-box/ref=dp_start-bbf_1_glance", data=post_data)

	return 


def search(query_list, sessionID):

    html_dom = ''

    search_url = "https://www.amazon.de/s/ref=nb_sb_noss?url=search-alias%3Daps&field-keywords="
    for word in query_list:
    	search_url += word + '+'
    r = requests.get(search_url, headers=user_agent)

    return r.text


def req_product_page(sessionID, html_dom, product_identifier):

	print product_identifier

	#get product url
	link_list = []
	soup = BeautifulSoup(html_dom)
	for link in soup.findAll('a'):
		ref = link.get('href')
		if ref is not None:
			if product_identifier in ref:

				#request product page
				#user_agent = {'User-agent': 'Mozilla/5.0'}
				r = requests.get(ref, headers=user_agent)
				return r.text

	return 

def get_cart_page(sessionID):

	html_dom = ''
	return html_dom

def delete_from_cart(prudctID, sessionID):

	foo = ''
	return foo


def main():

	parser = argparse.ArgumentParser(
		description='Amazon Crawler')

	parser.add_argument("-u", nargs=1, dest="username", type=str, action='store',
						help='Amazon Username')
	parser.add_argument("-p", nargs=1, dest="password", type=str, action='store',
						help='Amazon Password')
	args = parser.parse_args()


    # fuer den Login
	amazon_user = args.username
	amazon_password = args.password

	html = search(query_list, 0)
	foo = req_product_page(0, html, product_identifier)
	add_to_cart(foo, 0)

	# Buy Phase
	# 	-> Login
	# 	-> suche
	#	-> produkt aufrufen
	#	-> warenkorb


	# Kick aus warenkorb
	#	-> Login
	#	-> warenkorb aufrufen
	#	-> ware entfernen


if __name__ == "__main__":
	main()