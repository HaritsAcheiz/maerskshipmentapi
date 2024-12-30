import requests
from dataclasses import dataclass
from dotenv import load_dotenv
import os
from urllib.parse import urljoin
import logging
from requests.exceptions import RequestException, Timeout

load_dotenv()
logging.basicConfig(level=logging.INFO)


@dataclass
class ShopifyApi():
	store_name: str = None
	access_token: str = None
	version: str = None
	api_url: str = None
	session: requests.Session = None
	retries: int = 3
	timeout: float = 10.0

	# Support
	def send_request(self, query, variables=None):
		"""
		Sends an HTTP POST request to the Shopify API.

		Args:
		query (str): The GraphQL query string.
		variables (dict, optional): Variables for the GraphQL query.

		Returns:
		dict: The parsed JSON response from Shopify.

		Raises:
		ValueError: If the response contains an error.
		"""
		for attempt in range(1, self.retries + 1):
			try:
				response = self.session.post(
					self.api_url,
					json={"query": query, "variables": variables},
					timeout=self.timeout
				)

				# Raise an HTTP error for non-success status codes
				response.raise_for_status()

				# Parse the JSON response
				json_response = response.json()

				# Check for API-specific errors
				if 'errors' in json_response:
					raise ValueError(f"Shopify API Error: {json_response['errors']}")

				return json_response

			except Timeout:
				logging.warning(f"Timeout on attempt {attempt}/{self.retries}")
			except RequestException as e:
				logging.error(f"Request failed on attempt {attempt}/{self.retries}: {e}")
			except ValueError as ve:
				logging.error(f"Shopify API returned an error: {ve}")
				raise ve  # Reraise if it's an API error

		# If all retries fail, raise an exception
		raise RuntimeError("Failed to send request after multiple attempts.")

	# Create
	def create_session(self):
		headers = {
			'X-Shopify-Access-Token': self.access_token,
			'Content-Type': 'application/json'
		}
		self.session = requests.Session()
		self.session.headers.update(headers)
		self.api_url = f'https://{self.store_name}.myshopify.com/admin/api/{self.version}/graphql.json'

	def create_carrier_service(self, name, callbackUrl, discovery, active):
		print("Creating carrier service...")
		query = '''
			mutation CarrierServiceCreate($input: DeliveryCarrierServiceCreateInput!) {
				carrierServiceCreate(input: $input){
					carrierService {
						id
						name
						callbackUrl
						active
						supportsServiceDiscovery
					}
					userErrors {
						field
						message
					}
				}
			}
		'''

		variables = {
			"input": {
				"name": name,
				"callbackUrl": callbackUrl,
				"supportsServiceDiscovery": discovery,
				"active": active
			}
		}

		response = self.send_request(query, variables=variables)

		return response

	# Read
	def products(self):
		print("Fetching Products...")
		query = '''
			{
				products(first:10){
					edges{
						node{
							handle
						}
					}
					pageInfo{
						endCursor
						hasNextPage
					}
				}
			}
		'''

		response = self.send_request(query)

		return response

	# Update

	# Delete


if __name__ == '__main__':
	api = ShopifyApi(store_name=os.getenv('STORE_NAME'), access_token=os.getenv('ACCESS_TOKEN'), version='2024-10')
	api.create_session()
	# response = api.products()
	response = api.create_carrier_service(
		name='Maersk',
		callbackUrl='https://gasscooters.pythonanywhere.com/rates',
		discovery=True,
		active=True
	)
	print(response)
