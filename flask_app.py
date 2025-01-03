from maerskapi import MaerskApi
from shopifyapi import ShopifyApi
from processing import *
from flask import Flask, request, jsonify, Response


sapi = ShopifyApi()
mapi = MaerskApi()

app = Flask(__name__)


@app.route('/rates', methods=['POST'])
def calculate_rates():
	# data = request.json
	# dummy input
	shopify_input = {
		"rate": {
			"origin": {
				"country": "CA",
				"postal_code": "K2P1L4",
				"province": "ON",
				"city": "Ottawa",
				"name": None,
				"address1": "150 Elgin St.",
				"address2": "",
				"address3": None,
				"phone": None,
				"fax": None,
				"email": None,
				"address_type": None,
				"company_name": "Jamie D's Emporium"
			},
			"destination": {
				"country": "CA",
				"postal_code": "K1M1M4",
				"province": "ON",
				"city": "Ottawa",
				"name": "Bob Norman",
				"address1": "24 Sussex Dr.",
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
					"name": "Short Sleeve T-Shirt",
					"sku": "",
					"quantity": 1,
					"grams": 1000,
					"price": 1999,
					"vendor": "Jamie D's Emporium",
					"requires_shipping": True,
					"taxable": True,
					"fulfillment_service": "manual",
					"properties": None,
					"product_id": 48447225880,
					"variant_id": 258644705304
				}
			],
			"currency": "USD",
			"locale": "en"
		}
	}

	maersk_new_quote = mapi.get_new_quote_rest()
	ratingRootObject = shopify_maersk_rate_all_services(maersk_new_quote.text, shopify_input)
	result = mapi.get_rating_rest(ratingRootObject)

	return result

# get order
# response = mapi.get_new_quote_rest()
# print(response.text)


if __name__ == '__main__':
	app.run(host="0.0.0.0", port=5000, debug=True)