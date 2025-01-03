from dataclasses import dataclass, field
from urllib.parse import urljoin, urlencode
from dotenv import load_dotenv
import zeep
from zeep.transports import Transport
import ssl
import requests

load_dotenv()


@dataclass
class MaerskApi():
	base_api_url: str = 'https://pilotws.pilotdelivers.com'
	wsdl_url: str = 'https://pilotws.pilotdelivers.com/copilotforms/wsCoPilotSG.asmx?WSDL'
	session: requests.Session = field(default_factory=requests.Session)

	def get_new_quote(self):
		settings = zeep.Settings(strict=False)

		self.session.headers.update({
			"Content-Type": "application/soap+xml; charset=utf-8"
		})

		# self.session.verify = 'certificates/server.pem'
		self.session.verify = False

		wsdl_url = "https://ws.pilotair.com/tms2.1/tms/PilotServiceRequest.asmx?WSDL"

		transport = Transport(session=self.session)
		zeep_client = zeep.Client(wsdl=wsdl_url, transport=transport, settings=settings)

		try:
			response = zeep_client.service.GetNewQuote()
			return response
		except Exception as e:
			print("Error:", e)
			return None

	def get_new_quote_rest(self):
		endpoint = 'https://ws.pilotair.com/tms2.1/tms/PilotServiceRequest.asmx/GetNewQuote'

		try:
			with requests.Session() as client:
				response = client.get(endpoint, verify=False)
			response.raise_for_status()
			return response
		except Exception as e:
			print(f"Error occurred: {e}")
			return None

	def find_origin_by_zip_rest(self, sZip):
		endpoint = urljoin(self.base_api_url, '/copilotforms/wsCoPilotSG.asmx/FindOriginByZip')

		payload = {'sZip': sZip}
		encoded_payload = urlencode(payload)
		content_length = str(len(encoded_payload))

		headers = {
			'Content-Type': 'application/x-www-form-urlencoded',
			'Content-Length': content_length
		}

		self.client.headers.update(headers)
		try:
			response = self.client.post(endpoint, data=encoded_payload)
			response.raise_for_status()
			return response
		except Exception as e:
			print(f"Error occurred: {e}")
			return None

	def find_origin_by_zip(self, sZip):
		self.session.headers.update({
			"Content-Type": "application/soap+xml; charset=utf-8",
		})

		wsdl_url = "https://pilotws.pilotdelivers.com/copilotforms/wsCoPilotSG.asmx?WSDL"

		transport = Transport(session=self.session)
		zeep_client = zeep.Client(wsdl=wsdl_url, transport=transport)

		try:
			return zeep_client.service.FindOriginByZip(sZip=sZip)
		except Exception as e:
			print("Error:", e)

	def service_info_rest(self, sOriginZip, sDestZip):
		endpoint = urljoin(self.base_api_url, '/copilotforms/wsCoPilotSG.asmx/ServiceInfo')

		payload = {
			'sOriginZip': sOriginZip,
			'sDestZip': sDestZip
		}
		encoded_payload = urlencode(payload)
		content_length = str(len(encoded_payload))

		headers = {
			'Content-Type': 'application/x-www-form-urlencoded',
			'Content-Length': content_length
		}

		self.client.headers.update(headers)
		try:
			response = self.client.post(endpoint, data=encoded_payload)
			response.raise_for_status()
			return response
		except Exception as e:
			print(f"Error occurred: {e}")
			return None

	def service_info(self, sOriginZip, sDestZip):
		self.session.headers.update({
			"Content-Type": "application/soap+xml; charset=utf-8",
		})

		wsdl_url = "https://pilotws.pilotdelivers.com/copilotforms/wsCoPilotSG.asmx?WSDL"

		transport = Transport(session=self.session)
		zeep_client = zeep.Client(wsdl=wsdl_url, transport=transport)

		try:
			return zeep_client.service.ServiceInfo(sOriginZip=sOriginZip, sDestZip=sDestZip)
		except Exception as e:
			print("Error:", e)

	def get_rating_rest(self, ratingRootObject):
		endpoint = 'https://www.pilotssl.com/pilotapi/v1/Ratings'

		payload = ratingRootObject
		# encoded_payload = urlencode(payload)
		# content_length = str(len(encoded_payload))

		headers = {
			'Content-Type': 'application/json',
			'Accept': 'text/plain',
			'api-key': '9AC336ED-722D-440E-9439-43AFEA65D884'
		}

		try:
			with requests.Session() as client:
				client.headers.update(headers)
				response = client.post(endpoint, verify=False, json=payload)
			response.raise_for_status()
			return response.json()
		except Exception as e:
			print(f"Error occurred: {e}")
			return None


if __name__ == '__main__':
	api = MaerskApi()
	# response = api.find_origin_by_zip('30044')
	# response = api.service_info(sOriginZip='90001', sDestZip='30044')
	response = api.get_new_quote_rest()
	quote_object = response.text
	print(quote_object)
