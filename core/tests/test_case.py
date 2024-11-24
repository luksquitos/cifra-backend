from rest_framework import test, status
from rest_framework_simplejwt.tokens import AccessToken
from django.http import HttpResponse
from .pagination_mixin import PaginationMixin


class APITestCase(PaginationMixin, test.APITestCase):
    def authenticate(self, user=None):
        if not user:
            self.client.credentials(HTTP_AUTHORIZATION=None)
            return

        access = str(AccessToken.for_user(user))
        self.client.credentials(HTTP_AUTHORIZATION="Bearer %s" % access)

    def assertResponseDetail(self, response: HttpResponse, detail: str):
        expected = {"detail": detail}
        self.assertDictEqual(response.json(), expected)

    def assertResponseNotAuthenticated(self, response: HttpResponse):
        message = "As credenciais de autenticação não foram fornecidas."
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertResponseDetail(response, message)

    def assertResponseNotFound(self, response: HttpResponse):
        message = "Não encontrado."
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertResponseDetail(response, message)

    def assertResponseDeleted(self, response: HttpResponse):
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def assertResponseValidationError(
        self, response: HttpResponse, field: str, message: str
    ):
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertDictEqual(data, {field: [message]})
