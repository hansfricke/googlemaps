"""
This is the googlemaps module. It provides classes to access the googlemaps APIs.
Currently, the GeoCoding, Distancematrix, and Nearby search APIs are implemented.
"""
__author__ = 'Hans Fricke'
__version__ = '0.1'
__date__ = '04-16-2018'

import simplejson 
import urllib.request
import random


# ----------------------------------------------------------------
# Functions
#-----------------------------------------------------------------

class Query():
	"""Parent class with basic API call functionality"""
	def __init__(self, key):
		self.url = "https://maps.googleapis.com/maps/api/"
		self.key = key

	def submit(self):
		"""Submits API call."""	
		query_url = self.url
		return simplejson.load(urllib.request.urlopen(query_url))
				

class NearBySearch(Query):
	"""Class to submit and process NearBySearch request"""
	def __init__(self, key, lat, lng, keyword, 
					radius=500, 
					random_noise=True):
		super().__init__(key=key)
		self.lat = lat
		self.lng = lng
		self.keyword = keyword
		self.radius = radius
		self.random_noise = random_noise
		if random_noise:
			self.lat, self.lng = add_noise(lat=lat, lng=lng)

		self.url = self.url \
						+ "place/nearbysearch/json?location={0},{1}&radius={2}&keyword={3}&key={4}" \
						.format(self.lat, self.lng , self.radius, self.keyword, self.key)	

	def submit(self):
		"""Uses the submit function from parent class Query."""
		self.result = super().submit()	

	def get_info(self):
		"""Retrieves the information for each search result from
		   from Nearby API call."""
		information = []
		for item in self.result['results']:
			info = {'id': get_id(item),
					'name': get_name(item),
					'lat': get_lat(item),
					'lng': get_lng(item),
					'address': get_vicinity(item),
					'place_id': get_place_id(item),
					'types': get_types(item),
					'keyword': self.keyword
					}
			information.append(info)		 
		return information										


class GeoCode(Query):
	"""Class to submit and process Geocode request."""
	def __init__(self, address, key):
		super().__init__(key=key)
		self.address = address
		self.url =self.url \
						+ "geocode/json?address={0}&key={1}".format(self.address, self.key)	

	def submit(self):
		"""Uses the submit function from parent class Query."""		
		self.result = super().submit()	

	def get_info(self):
		"""Retrieves the latitude and longitude od address
		   from GeoCode API call."""
		item = self.result['results'][0]
		return {'latitude': get_lat(item), 
				'longitude': get_lng(item)}	


class Distance(Query):
	""" Class to submit and process Distancematrixs request."""
	def __init__(self, orig, dest, key, 
					mode='driving', 
					use_address_orig=False, 
					use_address_dest=False):
		super().__init__(key=key)
		if use_address_orig:
			self.orig = orig
		else:	
			self.lat_orig = orig[0]
			self.lng_orig = orig[1]
			self.orig = str(self.lat_orig) + "," + str(self.lng_orig)

		if use_address_dest:
			self.dest = dest
		else:	
			self.lat_dest = dest[0]
			self.lng_dest = dest[1]
			self.dest = str(self.lat_dest) + "," + str(self.lng_dest)

		self.mode = mode
		self.url =self.url \
						+ "distancematrix/json?origins={0}&destinations={1}&mode={2}&key={3}" \
						.format(self.orig, self.dest, self.mode, self.key)	

	def submit(self):
		"""Uses the submit function from parent class Query."""
		self.result = super().submit()	

	def get_info(self):
		"""Retrieves the distance and duration between two locations
		   from Distancematrix API call."""
		return {'distance': get_distance(self.result),
				'duration':	get_duration(self.result)}	

# ----------------------------------------------------------------
# Functions
#-----------------------------------------------------------------
def add_noise(**kwargs):
	""" Meant to add random noise to geo coordinates"""
	return [value + random.randrange(-100,100,1)/10000 + random.choice([0.001,-0.001])
				for key, value in kwargs.items()]

def get_id(dict):
	"""Retrieves the ID from a googlemap api request response."""
	return dict['id']	

def get_name(dict):
	"""Retrieves the name from a googlemap api request response."""
	return dict['name']			

def get_lat(dict):
	"""Retrieves the latitude from a googlemap api request response."""
	return dict['geometry']['location']['lat']	

def get_lng(dict):
	"""Retrieves the longitude from a googlemap api request response."""
	return dict['geometry']['location']['lng']	

def get_vicinity(dict):
	"""Retrieves the vicinity/address from a googlemap api request response."""
	return dict['vicinity']	

def get_place_id(dict):
	"""Retrieves the place ID from a googlemap api request response."""
	return dict['place_id']		

def get_types(dict):
	"""Retrieves the types from a googlemap api request response."""
	return dict['types']

def get_distance(dict):
	"""Retrieves the distance from a googlemap api request response."""
	return dict['rows'][0]['elements'][0]['distance']['value']

def get_duration(dict):
	"""Retrieves the duration from a googlemap api request response."""
	return dict['rows'][0]['elements'][0]['duration']['value']

					
