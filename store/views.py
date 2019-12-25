import json
from collections import OrderedDict
from key_value_store.settings import redis_client as redis

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class KeyValueApiView(APIView):

	def get(self, request, *args, **kwargs):
		key_value = {}
		for key in redis.scan_iter():
			k = str(key.decode('utf-8'))
			key_value[k] = redis.get(key)

		return Response(key_value, status=status.HTTP_200_OK)

	def post(self, request, *args, **kwargs):
		d = {'name': 'raisul', 'age': 26}
		o = OrderedDict(d)
		for key, value in o.items():
			print(key, value)
			redis.set(key, value)
			redis.expire(key, 300)
		return Response({'success': 'ok'}, status=status.HTTP_201_CREATED)

	def patch(self, request, *args, **kwargs):
		print('##########', request.data)
		return Response({'success': 'ok'}, status=status.HTTP_200_OK)


