from lxml import etree
import xml.etree.ElementTree as ET
import os
from dotenv import load_dotenv

load_dotenv()


def quote_to_json(source_xml):
	root = ET.fromstring(source_xml)
	ns = {
		'diffgr': 'urn:schemas-microsoft-com:xml-diffgram-v1',
		'temp': 'http://tempuri.org/dsTQSQuote.xsd'
	}

	tqs_quote = root.find('.//temp:TQSQuote', ns)
	shipper = tqs_quote.find('.//temp:Shipper', ns)
	consignee = tqs_quote.find('.//temp:Consignee', ns)

	result = {'Rating': dict()}
	result['Rating']['TQSQuoteID'] = tqs_quote.find('temp:TQSQuoteID', ns).text
	result['Rating']['QuoteID'] = tqs_quote.find('temp:QuoteID', ns).text
	result['Rating']['TariffID'] = tqs_quote.find('temp:TariffID', ns).text
	result['Rating']['Scale'] = tqs_quote.find('temp:Scale', ns).text
	result['Rating']['LocationID'] = tqs_quote.find('temp:LocationID', ns).text
	result['Rating']['TransportByAir'] = tqs_quote.find('temp:TransportByAir', ns).text
	result['Rating']['CalculateBillCode'] = tqs_quote.find('temp:CalculateBillCode', ns).text
	result['Rating']['IsSaveQuote'] = tqs_quote.find('temp:IsSaveQuote', ns).text
	result['Rating']['IATA_Classifications'] = tqs_quote.find('temp:IATA_Classifications', ns).text
	result['Rating']['PackingContainers'] = tqs_quote.find('temp:PackingContainers', ns).text
	result['Rating']['DeclaredValue'] = tqs_quote.find('temp:DeclaredValue', ns).text
	result['Rating']['InsuranceValue'] = tqs_quote.find('temp:InsuranceValue', ns).text
	result['Rating']['COD'] = tqs_quote.find('temp:COD', ns).text
	result['Rating']['TariffName'] = tqs_quote.find('temp:TariffName', ns).text
	result['Rating']['Notes'] = tqs_quote.find('temp:Notes', ns).text
	result['Rating']['Service'] = tqs_quote.find('temp:Service', ns).text
	result['Rating']['QuoteDate'] = tqs_quote.find('temp:QuoteDate', ns).text
	result['Rating']['ChargeWeight'] = tqs_quote.find('temp:ChargeWeight', ns).text
	result['Rating']['TotalPieces'] = tqs_quote.find('temp:TotalPieces', ns).text

	for field in [
		'Name', 'PDArea', 'Address1', 'Address2', 'City', 'State', 'Zipcode',
		'Airport', 'Attempted', 'PrivateRes', 'Hotel', 'Inside', 'Liftgate',
		'TwoManHours', 'WaitTimeHours', 'Special', 'DedicatedVehicle', 'Miles',
		'Canadian', 'ServiceCode', 'Convention', 'Country', 'IsBeyond',
		'BeyondServiceArea', 'Station', 'AirtrakNo'
	]:
		value = shipper.find(f'temp:{field}', ns)
		result['Rating']['Shipper'][field] = value.text

	for field in [
		'Name', 'PDArea', 'Address1', 'Address2', 'City', 'State', 'Zipcode',
		'Airport', 'Attempted', 'PrivateRes', 'Hotel', 'Inside', 'Liftgate',
		'TwoManHours', 'WaitTimeHours', 'Special', 'DedicatedVehicle', 'Miles',
		'Canadian', 'ServiceCode', 'Convention', 'Country', 'IsBeyond',
		'BeyondServiceArea', 'Station', 'AirtrakNo'
	]:
	value = consignee.find(f'temp:{field}', ns)
	result['Rating']['Consignee'][field] = value.text

	# line_items = ET.SubElement(rating, 'LineItems')
	# for field in ['LineRow', 'Pieces', 'Weight', 'Description', 'Length', 'Width', 'Height']:
	# add_element(line_items, field, 'string')

	# Add Quote information
	# quote = ET.SubElement(rating, 'Quote')
	# add_element(quote, 'Service', 'string')
	# add_element(quote, 'DimWeight', 'string')
	# add_element(quote, 'TotalQuote', 'string')

	# Add Breakdown information
	# breakdown = ET.SubElement(quote, 'Breakdown')
	# for field in ['ChargeCode', 'Charge', 'BillCodeName', 'Steps']:
	# add_element(breakdown, field, 'string')

	# Add remaining Quote fields
	# for field in [
	# 'Oversized', 'OversizedServiceArea', 'AbleToCalculate', 'ChargeWeight',
	# 'Beyond', 'DisplayService', 'TopLine', 'UpgradeRequiredForServiceArea',
	# 'LinkForShipping', 'ExtendedTopLine'
	# ]:
	# add_element(quote, field, 'string')

	# Add delivery date
	# delivery_date = ET.SubElement(quote, 'DeliveryDate')
	# delivery_date.text = '1970-01-01T00:00:00.001Z'

	# Add remaining Rating fields
	# ship_date = ET.SubElement(rating, 'ShipDate')
	# ship_date.text = '1970-01-01T00:00:00.001Z'

	result['Rating']['TariffHeaderID'] = tqs_quote.find('temp:TariffHeaderID', ns).text
	result['Rating']['UserID', 'string')
	result['Rating']['QuoteConfirmationEmail'] = tqs_quote.find('temp:QuoteConfirmationEmail', ns).text
	result['Rating']['DebrisRemoval'] = tqs_quote.find('temp:DebrisRemoval', ns).text
	result['Rating']['Gateway'] = tqs_quote.find('temp:Gateway', ns).text
	result['Rating']['IsInternational'] = tqs_quote.find('temp:IsInternational', ns).text

	return result


def shopify_maersk_rate_all_services(maersk_new_qoute, shopify_input):
	maersk_new_quote_bytes = maersk_new_qoute.encode('utf-8')
	parser = etree.XMLParser(remove_blank_text=True)
	root = etree.fromstring(maersk_new_quote_bytes, parser)

	namespaces = {
		'default': 'http://tempuri.org/dsTQSQuote.xsd',
		'diffgr': 'urn:schemas-microsoft-com:xml-diffgram-v1',
		'msdata': 'urn:schemas-microsoft-com:xml-msdata',
	}

	# quote_id = root.find('.//default:QuoteID', namespaces)
	# if quote_id is not None:
	# 	quote_id.text = '12345'

	# tariff_id = root.find('.//default:TariffID', namespaces)
	# if tariff_id is not None:
	# 	tariff_id.text = os.getenv('TARIFFHEADERID')

	location_id = root.find('.//default:LocationID', namespaces)
	if location_id is not None:
		location_id.text = os.getenv('LOCATIONID')

	charge_weight = root.find('.//default:ChargeWeight', namespaces)
	if charge_weight is not None:
		total_grams = sum(item['grams'] for item in shopify_input['rate']['items'])
		charge_weight.text = str(total_grams)

	total_pieces = root.find('.//default:TotalPieces', namespaces)
	if total_pieces is not None:
		quantities = sum(item['quantity'] for item in shopify_input['rate']['items'])
		total_pieces.text = str(quantities)

	tariff_header_id = root.find('.//default:TariffHeaderID', namespaces)
	if tariff_header_id is not None:
		tariff_header_id.text = os.getenv('TARIFFHEADERID')

	# Shipper
	shipper_name = root.find('.//default:Shipper/default:Name', namespaces)
	if shipper_name is not None:
		if shopify_input['rate']['origin']['name']:
			shipper_name.text = shopify_input['rate']['origin']['name']
		else:
			shipper_name.text = shopify_input['rate']['origin']['company_name']

	shipper_address1 = root.find('.//default:Shipper/default:Address1', namespaces)
	if shipper_address1 is not None:
		shipper_address1.text = shopify_input['rate']['origin']['address1']

	shipper_address2 = root.find('.//default:Shipper/default:Address2', namespaces)
	if shipper_address2 is not None:
		shipper_address2.text = shopify_input['rate']['origin']['address2']

	shipper_city = root.find('.//default:Shipper/default:City', namespaces)
	if shipper_city is not None:
		shipper_city.text = shopify_input['rate']['origin']['city']

	shipper_state = root.find('.//default:Shipper/default:State', namespaces)
	if shipper_state is not None:
		shipper_state.text = shopify_input['rate']['origin']['province']

	shipper_zipcode = root.find('.//default:Shipper/default:Zipcode', namespaces)
	if shipper_zipcode is not None:
		shipper_zipcode.text = shopify_input['rate']['origin']['postal_code']

	shipper_country = root.find('.//default:Shipper/default:Country', namespaces)
	if shipper_country is not None:
		shipper_country.text = shopify_input['rate']['origin']['country']

	# Consignee
	consignee_name = root.find('.//default:Consignee/default:Name', namespaces)
	if consignee_name is not None:
		if shopify_input['rate']['destination']['name']:
			consignee_name.text = shopify_input['rate']['destination']['name']
		else:
			consignee_name.text = shopify_input['rate']['destination']['company_name']

	consignee_address1 = root.find('.//default:Consignee/default:Address1', namespaces)
	if consignee_address1 is not None:
		consignee_address1.text = shopify_input['rate']['destination']['address1']

	consignee_address2 = root.find('.//default:Consignee/default:Address2', namespaces)
	if consignee_address2 is not None:
		consignee_address2.text = shopify_input['rate']['destination']['address2']

	consignee_city = root.find('.//default:Consignee/default:City', namespaces)
	if consignee_city is not None:
		consignee_city.text = shopify_input['rate']['destination']['city']

	consignee_state = root.find('.//default:Consignee/default:State', namespaces)
	if consignee_state is not None:
		consignee_state.text = shopify_input['rate']['destination']['province']

	consignee_zipcode = root.find('.//default:Consignee/default:Zipcode', namespaces)
	if consignee_zipcode is not None:
		consignee_zipcode.text = shopify_input['rate']['destination']['postal_code']

	consignee_country = root.find('.//default:Consignee/default:Country', namespaces)
	if consignee_country is not None:
		consignee_country.text = shopify_input['rate']['destination']['country']

	modified_xml = etree.tostring(root, pretty_print=True, xml_declaration=True, encoding='utf-8')
	modified_xml = convert_xml(modified_xml)

	return modified_xml
