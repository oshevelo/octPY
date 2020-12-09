from rest_framework.authentication import TokenAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import LimitOffsetPagination

from .DiscountRequestAdapter import *
from .application.DiscountService import DiscountService
from .serializers import DiscountPostSerializer


class Discounts(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication, BasicAuthentication)
    pagination_class = LimitOffsetPagination

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.discount_request_adapter = DiscountRequestAdapter()
        self.discount = DiscountService()

    def post(self, request) -> Response:
        discount_data = DiscountPostSerializer(data=request.data)

        if not discount_data.is_valid():
            return Response({"message": "Not Valid"}, status=status.HTTP_400_BAD_REQUEST)

        code, cart_number, cart_amount = self.discount_request_adapter.adapt_serializer_data(discount_data)

        return self.discount.response_client_service(
            code,
            cart_number,
            cart_amount
        )
