# coding=utf-8
""" JSON

Extra module to help convert to and from JSON with complicated types like
datetime and decimal
"""

__author__		= "Chris Nasr"
__copyright__	= "OuroborosCoding"
__license__		= "Apache"
__version__		= "1.1.0"
__maintainer__	= "Chris Nasr"
__email__		= "ouroboroscode@gmail.com"

# Import python core modules
import json
from datetime import datetime
from decimal import Decimal

# Encode
def encode(o):
	"""Encode

	Handles encoding objects/values into JSON, returns the JSON as a string

	Args:
		o (mixed): The object or value to encode

	Returns:
		str
	"""
	return json.dumps(o, cls=CEncoder)

# EncodeF
def encodef(o, f):
	"""EncodeF

	Handles encoding objects/values into JSON and stores them in the given file

	Args:
		o (mixed): The object or value to encode
		f (fp): An open file pointer which can be written to

	Returns:
		None
	"""
	return json.dump(o, f, cls=CEncoder)

# Decode
def decode(s):
	"""Decode

	Handles decoding JSON, as a string, into objects/values

	Args:
		s (str): The JSON to decode

	Returns:
		mixed
	"""
	return json.loads(s, parse_float=Decimal, encoding='utf-8')

# DecodeF
def decodef(f):
	"""DecodeF

	Handles decoding JSON, from a file, into objects/values

	Args:
		f (fp): An open file pointer that can be read

	Returns:
		mixed
	"""
	return json.load(f, parse_float=Decimal, encoding='utf-8')

# Encoder
class CEncoder(json.JSONEncoder):
	"""Encode

	Handles encoding types the default JSON encoder can't handle

	Extends: json.JSONEncoder
	"""

	# Default
	def default(self, obj):
		"""Default

		Called when the regular Encoder can't figure out what to do with the type

		Args:
			self (CEncoder): A pointer to the current instance
			obj (mixed): An unknown object that needs to be encoded

		Returns:
			str: A valid JSON string representing the object
		"""

		# If we have a datetime object
		if isinstance(obj, datetime):
			return obj.strftime('%Y-%m-%d %H:%M:%S')

		# Else if we have a decimal object
		elif isinstance(obj, Decimal):
			return '{0:f}'.format(obj)

		# Bubble back up to the parent default
		return json.JSONEncoder.default(self, obj)
