from maerskapi import MaerskApi
from shopifyapi import ShopifyApi
from processing import *
from flask import Flask, request, jsonify, Response

sapi = ShopifyApi()
mapi = MaerskApi()

app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
	data = request.data
	hmac_header = request.headers.get('X-Shopify-Hmac-Sha256')

	if not verify_webhook(data, hmac_header):

		return "Webhook verification failed", 401

	payload = request.json
	print("Webhook received:", payload)

	return "Webhook received", 200


@app.route('/rates', methods=['POST'])
def calculate_rates():
	# data = request.json
	# dummy input
	# shopify_input = {
	# 	"rate": {
	# 		"origin": {
	# 			"country": "CA",
	# 			"postal_code": "K2P1L4",
	# 			"province": "ON",
	# 			"city": "Ottawa",
	# 			"name": None,
	# 			"address1": "150 Elgin St.",
	# 			"address2": "",
	# 			"address3": None,
	# 			"phone": None,
	# 			"fax": None,
	# 			"email": None,
	# 			"address_type": None,
	# 			"company_name": "Jamie D's Emporium"
	# 		},
	# 		"destination": {
	# 			"country": "CA",
	# 			"postal_code": "K1M1M4",
	# 			"province": "ON",
	# 			"city": "Ottawa",
	# 			"name": "Bob Norman",
	# 			"address1": "24 Sussex Dr.",
	# 			"address2": "",
	# 			"address3": None,
	# 			"phone": None,
	# 			"fax": None,
	# 			"email": None,
	# 			"address_type": None,
	# 			"company_name": None
	# 		},
	# 		"items": [
	# 			{
	# 				"name": "Short Sleeve T-Shirt",
	# 				"sku": "",
	# 				"quantity": 1,
	# 				"grams": 1000,
	# 				"price": 1999,
	# 				"vendor": "Jamie D's Emporium",
	# 				"requires_shipping": True,
	# 				"taxable": True,
	# 				"fulfillment_service": "manual",
	# 				"properties": None,
	# 				"product_id": 48447225880,
	# 				"variant_id": 258644705304
	# 			}
	# 		],
	# 		"currency": "USD",
	# 		"locale": "en"
	# 	}
	# }

	# shopify_input = {
	# 	"rate": {
	# 		"origin": {
	# 			"country": "US",
	# 			"postal_code": "10001",
	# 			"province": "NY",
	# 			"city": "New York",
	# 			"name": None,
	# 			"address1": "350 5th Avenue",  # Empire State Building
	# 			"address2": "Suite 300",
	# 			"address3": None,
	# 			"phone": None,
	# 			"fax": None,
	# 			"email": None,
	# 			"address_type": None,
	# 			"company_name": "Manhattan Apparel Co."
	# 		},
	# 		"destination": {
	# 			"country": "US",
	# 			"postal_code": "90210",
	# 			"province": "CA",
	# 			"city": "Beverly Hills",
	# 			"name": "Sarah Johnson",
	# 			"address1": "9641 Sunset Boulevard",  # Beverly Hills Hotel address
	# 			"address2": "",
	# 			"address3": None,
	# 			"phone": None,
	# 			"fax": None,
	# 			"email": None,
	# 			"address_type": None,
	# 			"company_name": None
	# 		},
	# 		"items": [
	# 			{
	# 				"name": "Premium Cotton Hoodie",
	# 				"sku": "",
	# 				"quantity": 1,
	# 				"grams": 1000,
	# 				"price": 4999,
	# 				"vendor": "Manhattan Apparel Co.",
	# 				"requires_shipping": True,
	# 				"taxable": True,
	# 				"fulfillment_service": "manual",
	# 				"properties": None,
	# 				"product_id": 48447225881,
	# 				"variant_id": 258644705305
	# 			}
	# 		],
	# 		"currency": "USD",
	# 		"locale": "en"
	# 	}
	# }

	shopify_input = {
		"rate": {
			"origin": {
				"country": "CA",
				"postal_code": "M5V 2T6",
				"province": "ON",
				"city": "Toronto",
				"name": None,
				"address1": "301 Front St W",
				"address2": "",
				"address3": None,
				"phone": None,
				"fax": None,
				"email": None,
				"address_type": None,
				"company_name": "CN Tower Gift Shop"
			},
			"destination": {
				"country": "CA",
				"postal_code": "H2Y 1C6",
				"province": "QC",
				"city": "Montreal",
				"name": "Marie Tremblay",
				"address1": "985 Rue Saint-Paul O",
				"address2": "",
				"address3": None,
				"phone": None,
				"fax": None,
				"email": None,
				"address_type": None,
				"company_name": None
			},
			"items": [
				{
					"name": "Canadian Maple Syrup",
					"sku": "",
					"quantity": 1,
					"grams": 1000,
					"price": 2499,
					"vendor": "CN Tower Gift Shop",
					"requires_shipping": True,
					"taxable": True,
					"fulfillment_service": "manual",
					"properties": None,
					"product_id": 48447225881,
					"variant_id": 258644705305
				}
			],
			"currency": "CAD",
			"locale": "en"
		}
	}

	maersk_new_quote = mapi.get_new_quote_rest()
	ratingRootObject = shopify_maersk_rate_all_services(maersk_new_quote.text, shopify_input)
	result = mapi.get_rating_rest(ratingRootObject)
	# result = ratingRootObject
	return result
	# return Response(result, mimetype='text/xml')

# get order
# response = mapi.get_new_quote_rest()
# print(response.text)


if __name__ == '__main__':
	app.run(host="0.0.0.0", port=5000, debug=True)