from django import template
import base64
from decimal import Decimal

register = template.Library()

@register.filter(name='bytes_to_string')
def convert_bytes(byte_data):
	return byte_data.decode("utf-8")

@register.filter(name='convert_values')
def convert_data(listings):
	for i in range(len(listings)):
		listings[i].rent = Decimal(listings[i].rent)
		listings[i].distance = Decimal(listings[i].distance)
		listings[i].bedrooms = int(listings[i].bedrooms)
		listings[i].bathrooms = int(listings[i].bathrooms)
	return listings