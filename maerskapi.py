from httpx import Client
from dataclasses import dataclass, field
from urllib.parse import urljoin, urlencode
from dotenv import load_dotenv

load_dotenv()


@dataclass
class MaerskApi():
	base_api_url: str = 'https://pilotws.pilotdelivers.com'
	client: Client = field(default_factory=Client)

	def find_origin_by_zip(self, sZip):
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

	def service_info(self, sOriginZip, sDestZip):
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


if __name__ == '__main__':
	api = MaerskApi()
	# response = api.find_origin_by_zip('30044')
	response = api.service_info(sOriginZip='90001', sDestZip='30044')
	if response:
		print(response.status_code, response.text)