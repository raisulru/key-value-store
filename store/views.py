import json
from collections import OrderedDict
from key_value_store.settings import redis_client as redis
from key_value_store.settings import TTL_VALUE

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class KeyValueApiView(APIView):

	def get(self, request, *args, **kwargs):
		keys = self.request.query_params.get('keys', None)
		key_value = {}

		if keys:
			keys = keys.split(',')

			for key in keys:
				value = redis.get(key)
				if value:
					key_value[key] = value
					redis.expire(key, TTL_VALUE)
		else:
			for key in redis.scan_iter():
				k = str(key.decode('utf-8'))
				key_value[k] = redis.get(key)

		return Response(key_value, status=status.HTTP_200_OK)

	def post(self, request, *args, **kwargs):
		ordered_dict = OrderedDict(request.data)
		for key, value in ordered_dict.items():
			redis.set(key, value)
			redis.expire(key, TTL_VALUE)
		return Response({'success': 'Successfully created this store'}, status=status.HTTP_201_CREATED)

	def patch(self, request, *args, **kwargs):
		ordered_dict = OrderedDict(request.data)

		for key, value in ordered_dict.items():
			if redis.get(key):
				redis.set(key, value)
				redis.expire(key, TTL_VALUE)
			else:
				return Response({'error': 'Key not found in store'}, status=status.HTTP_404_NOT_FOUND)
		return Response({'success': 'successfully updated'}, status=status.HTTP_200_OK)




