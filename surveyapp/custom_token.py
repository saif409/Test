from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status


class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        active_status = "Active" if user.is_active else "Suspend"
        surveyor_id = user.surveyer.id if user.surveyer else user.id

        return Response({
            'surveyor_id ': surveyor_id,
            'token': token.key,
            'msg': "Login Success",
            'active_status': active_status
        }, status=200)