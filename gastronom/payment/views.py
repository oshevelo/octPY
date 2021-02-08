from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from rest_framework import generics
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from .models import Payments, PaymentSystemLog
from .serializers import PaymentsSerializer
from .filters import PaymentsFilter
from .permissions import PaymentsPermission

class PaymentsList(generics.ListCreateAPIView):
    queryset = Payments.objects.all()
    serializer_class = PaymentsSerializer
    pagination_class = LimitOffsetPagination
    filterset_class = PaymentsFilter
    permission_class = [IsAuthenticated]

class PaymentsDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PaymentsSerializer
    permission_class = [IsAuthenticated, PaymentsPermission]

    def get_object(self):
        obj = get_object_or_404(Payments, pk=self.kwargs.get('payment_id'))
        return obj


class PaymentSystemLogList(generics.ListCreateAPIView):
    queryset = PaymentSystemLog.objects.all()
    pagination_class = LimitOffsetPagination


class PaymentSystemLogDetail(generics.RetrieveUpdateDestroyAPIView):
    def get_object(self):
        obj = get_object_or_404(PaymentSystemLog,
            pk=self.kwargs.get('paymentsystemlog_id')
        )
        return obj