from django.shortcuts import render
from rest_framework import permissions, viewsets
from rest_framework.response import Response
from rest_framework.decorators import detail_route
from coupons.models import Coupon
from coupons.permissions import IsAdminUser
from coupons.serializers import CouponSerializer
from datetime import date


class CouponViewSet(viewsets.ModelViewSet):
	lookup_field = 'code'
	queryset = Coupon.objects.order_by('-created_at')
	serializer_class = CouponSerializer

	def get_permissions(self):
		if self.request.method in permissions.SAFE_METHODS:
			return (permissions.AllowAny(),)
		return (permissions.IsAuthenticated(), IsAdminUser(),)
		
	def perform_create(self, serializer):
		instance = serializer.save()
		return super(CouponViewSet, self).perform_create(serializer)

	
	
	@detail_route(methods=['GET']) 
	def verify(self, request, code=None):
		coupon = Coupon.objects.filter(code=code)
		if coupon.exists() and coupon[0].valid_till > date.today():
			return Response({'valid': True}) 
		else:
			return Response({'valid': False}) 
