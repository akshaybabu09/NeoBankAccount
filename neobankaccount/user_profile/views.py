# django imports
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import *
from rest_framework.views import APIView

# project level imports
from user_profile.constants import *
from user_profile.serializers import UserRegistrationSerializer
from user_profile.services import arrange_data, check_for_duplicate, \
    fetch_user_details_from_mobile


class OpenAccountView(APIView):
    get_serializer = UserRegistrationSerializer

    def post(self, request):
        try:
            dup, msg = check_for_duplicate(request.data)
            if dup:
                return Response(msg, status=HTTP_409_CONFLICT)

            serialize_data = arrange_data(request.data)

            serializer = self.get_serializer(data=serialize_data)

            if serializer.is_valid():
                user = serializer.save()

                if user:
                    token, created = Token.objects.get_or_create(user=user)
                    json = {
                        'token': token.key,
                        'msg': ACCOUNT_CREATED_MSG
                    }
                    return Response(json, status=HTTP_201_CREATED)
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

        except:
            return Response(ERROR_MSG, status=HTTP_500_INTERNAL_SERVER_ERROR)


class DisplayUserDetailsAPI(APIView):
    # authentication_classes = (TokenAuthentication,)
    # permission_classes = (IsAuthenticated,)

    def get(self, request, mobile):
        try:
            print(request)
            user_details, msg = fetch_user_details_from_mobile(mobile)
            if not user_details:
                return Response(msg, status=HTTP_404_NOT_FOUND)
            return Response(user_details, status=HTTP_200_OK)
        except:
            return Response(ERROR_MSG, status=HTTP_400_BAD_REQUEST)
