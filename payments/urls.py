
from django.urls import path

from payments import views

app_name = "payments"

urlpatterns = [
    path("stk_push/", views.STKPushAPIView.as_view(), name="stk-push"),
    path("mpesa_callback/", views.MPESACallBackAPIView.as_view(), name="mpesa-callback"),
]