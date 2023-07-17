# from django.test import TestCase
# from django.urls import reverse
# from rest_framework import status
# from rest_framework.test import APIClient

# class STKPushAPIViewTestCase(TestCase):
#     def setUp(self):
#         self.client = APIClient()

#     def test_stk_push_success(self):
#         payload = {
#             "phone_number": "1234567890",
#             "amount": 1,
#             "account_reference": "ABC123",
#             "transaction_desc": "Example transaction"
#         }

#         response = self.client.post(reverse("payments:stk-push"), data=payload)

#         self.assertEqual(response.status_code, status.HTTP_200_OK)

#     def test_stk_push_missing_parameters(self):
#         payload = {
#             "phone_number": "1234567890"
#         }

#         response = self.client.post(reverse("payments:stk-push"), data=payload)

#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
