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

		firstRequest='https://www.amazon.de/ap/signin?_encoding=UTF8&openid.assoc_handle=deflex&openid.claimed_id=http://specs.openid.net/auth/2.0/identifier_select&openid.identity=http://specs.openid.net/auth/2.0/identifier_select&openid.mode=checkid_setup&openid.ns=http://specs.openid.net/auth/2.0&openid.ns.pape=http://specs.openid.net/extensions/pape/1.0&openid.pape.max_auth_age=0&openid.return_to=https://www.amazon.de/gp/yourstore/home?ie=UTF8&action=sign-out&path=%2Fgp%2Fyourstore%2Fhome&ref_=gno_signout&signIn=1&useRedirectOnSuccess=1'
		fourthRequest = amazon_session.get(firstRequest, headers=user_agent)

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
		
		# update email, password, create and metadata1 seperatly. Found way to do it without metadata. Just use the backwards compatible login for people without JavaScript.
		
		post_data.update({'email': user.decode('utf-8')})
		post_data.update({'password':password.decode('utf-8')})
		post_data.update({'create':'0'.decode('utf-8')})

		#AAAAAND FIRE LOGIN REQUEST, BUT UPDATE ALL HEADER FIRST, IS IMPORTANT
		user_agent.update({'Referer': 'https://www.amazon.de/ap/signin?_encoding=UTF8&openid.assoc_handle=deflex&openid.claimed_id=http://specs.openid.net/auth/2.0/identifier_select&openid.identity=http://specs.openid.net/auth/2.0/identifier_select&openid.mode=checkid_setup&openid.ns=http://specs.openid.net/auth/2.0&openid.ns.pape=http://specs.openid.net/extensions/pape/1.0&openid.pape.max_auth_age=0&openid.return_to=https://www.amazon.de/gp/yourstore/home?ie=UTF8&action=sign-out&path=%2Fgp%2Fyourstore%2Fhome&ref_=gno_signout&signIn=1&useRedirectOnSuccess=1'.decode('utf-8')})
		user_agent.update({'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
		'Accept-Language': 'en-US,en;q=0.5',
		'Accept-Encoding': 'gzip, deflate, br',
		'Connection': 'close',
		'Content-Type': 'application/x-www-form-urlencoded',
		})
		time.sleep(randint(0,2))
		for cookie in fourthRequest.cookies:
			if(cookie.name == "session-id"):
				session_id = cookie.value
		if (session_id):
			newURL = 'https://www.amazon.de/ap/signin/' + session_id
			fithRequest = amazon_session.post(newURL, headers=user_agent, data=post_data)

			#print fithRequest.text.encode('utf-8').strip()
			return amazon_session.cookies


def add_to_cart(html_product, cookieJar):

	with requests.Session() as amazon_session:
		amazon_session.cookies = cookieJar
		# all POST params needed
		# please don't ask me what all of this shit is
		post_data_names = ['session-id', 'ASIN', 'offerListingID', 
		'isMerchantExclusive', 'merchantID', 'isAddon', 'nodeID', 
		'sellingCustomerID', 'qid', 'sr', 'storeID', 'tagActionCode', 
		'viewID', 'rsid', 'sourceCustomerOrgListID', 'sourceCustomerOrgListItemID', 
		'wlPopCommand', 'submit.add-to-cart', 'dropdown-selection', 'quantity']

		
		# building POST request
		post_data = dict()
		soup = BeautifulSoup(html_product)
		for input_tag in soup.findAll('input'):
			name =  input_tag.get('name')
			if name is not None:
				if any(name in input_tag.get('name') for name in post_data_names):
					post_data.update({input_tag.get('name'):input_tag.get('value')})
		post_data.update({'submit.add-to-cart': 'In den Einkaufswagen'.decode('utf-8')})
		post_data.update({'quantity': '1'.decode('utf-8')})
		print post_data
		r = amazon_session.post("https://www.amazon.de/gp/product/handle-buy-box/ref=dp_start-bbf_1_glance ", headers=user_agent, data=post_data)
		#print r.text.encode('utf-8').strip()
		return amazon_session.cookies


def search(query_list, cookieJar):

	with requests.Session() as amazon_session:

	    html_dom = ''
	    amazon_session.cookies = cookieJar
	    search_url = "https://www.amazon.de/s/ref=nb_sb_noss?url=search-alias%3Daps&field-keywords="
	    for word in query_list:
	    	search_url += word + '+'
	    r = amazon_session.get(search_url, headers=user_agent)
	    return r.text, amazon_session.cookies


def req_product_page(cookieJar, html_dom, product_identifier):

	with requests.Session() as amazon_session:
		print product_identifier

		amazon_session.cookies = cookieJar
		#get product url
		link_list = []
		soup = BeautifulSoup(html_dom)
		for link in soup.findAll('a'):
			ref = link.get('href')
			if ref is not None:
				if product_identifier in ref:

					#request product page
					#user_agent = {'User-agent': 'Mozilla/5.0'}
					r = amazon_session.get(ref, headers=user_agent)
					return r.text, amazon_session.cookies
		return 

def get_cart_page(cookieJar):
	# Allright, lets just login with our existing session. Dont know yet whether Session() re-uses my existing TCP-Session (i think it shouldn right know, since its a new object), but doesnt seem to be an issue right now (maybe when it comes to all kind of defense mechanisms of amazon, such as captachs and all...)
	with requests.Session() as loggedInSession:
		
		shoppingCard = loggedInSession.get('http://www.amazon.de/gp/cart/view.html/ref=nav_cart', headers=user_agent, cookies=cookieJar)
		
		# Debugging-Output
		#print(shoppingCard.text).encode('utf-8').strip()

		return shoppingCard.text

def delete_from_cart(prudctID, cookieJar):

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


	loggedInSession = login(amazon_user[0], amazon_password[0])
	user_agent.update({'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
	'Accept-Language': 'en-US,en;q=0.5',
	'Accept-Encoding': 'gzip, deflate, br',
	'Connection': 'close',
	'Content-Type': 'application/x-www-form-urlencoded',
	})
	html, loggedInSession = search(query_list, loggedInSession)
	foo, loggedInSession = req_product_page(loggedInSession, html, product_identifier)
	loggedInSession = add_to_cart(foo, loggedInSession)
	get_cart_page(loggedInSession)
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