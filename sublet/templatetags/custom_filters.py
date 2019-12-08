from django import template
import base64

register = template.Library()

@register.filter(name='bytes_to_base64')
def convert_bytes(bytes):
    return bytes.decode("utf-8")