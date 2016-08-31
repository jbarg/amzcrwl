#!/usr/bin/python2
import requests
import argparse
import time
from random import randint
from BeautifulSoup import BeautifulSoup


query_list = ['rotes', 'gummiboot']
product_identifier = 'Kinderboot-Speedway-Friends'

user_agent = {'User-agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:47.0) Gecko/20100101 Firefox/47.0'}



def login(user, password):

	# OK, SHITTY LONG ASS AMAZON LOGIN FLOW STARTS RIGHT HERE AT AMAZON MAIN PAGE
	with requests.Session() as amazon_session:


		initialRequest = amazon_session.get('https://www.amazon.de/', headers=user_agent)
		# GREAT! WE NOW HAVE THE INITIAL COOKIES. TIME FOR THE NEXT REQUEST FOR SOME REASON NECESSARY

		# RANDOM SLEEPS MIGHT HELP AGAINST ANNOYING CAPTCHAS???
		time.sleep(randint(0,3))
		secondRequest = amazon_session.get('https://www.amazon.de/gp/prime/digital-adoption/navigation-bar/255-9312508-3957466?type=load&isPrime=false&referrer=&height=841&width=1377&_=1472583390045', headers=user_agent)
		# SUCCESS! WE NOW EVEN HAVE MORE IMPORTANT COOKIES!
		time.sleep(randint(0,5))
		thirdRequest = amazon_session.post('https://www.amazon.de/gp/gw/ajax/desktop/herotator/record-impressions.html/255-9312508-3957466?ie=UTF8&aPTID=36701&cmpnId=567f980d-1159-3da4-9269-6d3bf0327230&cnttId=11d776ee-b65a-4ab6-8b75-98c3f2335eb3&h=BFBF15464D85B3FD5E278D40D4A5EB122CD3BE8A1&mId=A3JWKAKR8XB7XF&mkId=A1PA6795UKMFR9&pId=cdbc2dbd-7025-4c40-8619-6f6e7515a47a&pIdent=desktop&rId=TKWSCVWBCYDX81G1VWDX8&sid=14&slotName=desktop-hero-piv', headers=user_agent)
		# AND IT GOES ON!
		time.sleep(randint(0,1))
		fourhtURL='https://www.amazon.de/ap/signin?_encoding=UTF8&openid.assoc_handle=deflex&openid.claimed_id=http://specs.openid.net/auth/2.0/identifier_select&openid.identity=http://specs.openid.net/auth/2.0/identifier_select&openid.mode=checkid_setup&openid.ns=http://specs.openid.net/auth/2.0&openid.ns.pape=http://specs.openid.net/extensions/pape/1.0&openid.pape.max_auth_age=0&openid.return_to=https://www.amazon.de/?ref_=nav_signin'
		fourthRequest = amazon_session.get(fourhtURL, headers=user_agent)

		# NOW COMES THE ACTUAL LOGIN. WE HAVE TO READ OUT SOME OPENID-STUFF FROM THE PREVIOUS RESPONSE BECAUSE YES
		# LOT OF SEEMINGLY STATIC STUFF IN THIS POST, THE NECESSARY DATA IS BEING UPDATED. USING JONS GREAT UPDATESHIT

		postdata_elements=['appActionToken', 'appAction', 'openid.pape.max_auth_age', 'openid.return_to', 'prevRID', 'openid.identity', 'openid.assoc_handle', 'openid.mode', 'openid.ns.pape', 'openid.claimed_id', 'pageId', 'openid.ns', 'email', 'create', 'password', 'metadata1']
		
		post_data = dict()
		
		soup = BeautifulSoup(fourthRequest.text)
		for input_tag in soup.findAll('input'):
			name =  input_tag.get('name')
			if name is not None:
				if any(name in input_tag.get('name') for name in postdata_elements):
					post_data.update({input_tag.get('name'):input_tag.get('value')})
		
		# update email, password, create and metadata1 seperatly. Sorry, no fast way in creating this metadata out of request, pls ignore the bloat in the code
		
		post_data.update({'email': user.decode('utf-8')})
		post_data.update({'password':password.decode('utf-8')})
		post_data.update({'create':'0'.decode('utf-8')})
		post_data.update({'metadata1':'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'.decode('utf-8')})

		#AAAAAND FIRE LOGIN REQUEST
		user_agent.update({'Referer': fourhtURL.decode('utf-8')})
		time.sleep(randint(0,10))
		fithRequest = amazon_session.post('https://www.amazon.de/ap/signin', headers=user_agent, data=post_data)

		print post_data			
		print initialRequest.cookies
		print secondRequest.cookies
		print thirdRequest.cookies
		print fourthRequest.cookies
		print fithRequest.text
		print fithRequest.status_code
		return amazon_session.cookies


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
	login(amazon_user[0], amazon_password[0])
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