from maerskapi import MaerskApi
from shopifyapi import ShopifyApi
from flask import Flask, request, jsonify


sapi = ShopifyApi()
mapi = MaerskApi()

app = Flask(__name__)


@app.route('/rates', methods=['POST'])
def calculate_rates():
	data = request.json

	return jsonify(data)

# get order
# response = mapi.get_new_quote_rest()
# print(response.text)


if __name__ == '__main__':
	app.run(host="0.0.0.0", port=5000, debug=True)