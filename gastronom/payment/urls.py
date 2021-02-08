from django.urls import path
from . import views

urlpatterns = [
    path('', views.PaymentsList.as_view(), name = 'payments_list'),
    path('<int:payment_id>/',
        views.PaymentsDetail.as_view(), name = 'payments_detail'
    ),

]