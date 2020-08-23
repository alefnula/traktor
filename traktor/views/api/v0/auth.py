from rest_framework.exceptions import ValidationError
from rest_framework_jwt.views import ObtainJSONWebToken, RefreshJSONWebToken


class ObtainToken(ObtainJSONWebToken):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 400:
            raise ValidationError(detail=response.data)
        return response


class RefreshToken(RefreshJSONWebToken):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 400:
            raise ValidationError(detail=response.data)
        return response
