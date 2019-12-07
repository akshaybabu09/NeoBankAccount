# django imports
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import *
from rest_framework.views import APIView

# project level imports
from user_profile.constants import *
from user_profile.serializers import UserRegistrationSerializer, UserLoginSerializer
from user_profile.services import arrange_data, check_for_duplicate, \
    fetch_user_details_from_mobile, fetch_user_details, update_user_details, fetch_token_for_user


class UserRegistrationAPI(APIView):
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
                    json = fetch_token_for_user(user, register=True)
                    return Response(json, status=HTTP_201_CREATED)
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

        except:
            return Response(ERROR_MSG, status=HTTP_500_INTERNAL_SERVER_ERROR)


class DisplayUserDetailsAPI(APIView):

    def get(self, request, mobile):
        try:
            user_details, msg = fetch_user_details_from_mobile(mobile)
            if not user_details:
                return Response(msg, status=HTTP_404_NOT_FOUND)
            return Response(user_details, status=HTTP_200_OK)
        except:
            return Response(ERROR_MSG, status=HTTP_500_INTERNAL_SERVER_ERROR)


class UserHomePageAPI(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        try:
            print(request)
            user = request.user
            print(user)
            user_details, msg = fetch_user_details(user)
            if not user_details:
                return Response(msg, status=HTTP_404_NOT_FOUND)
            return Response(user_details, status=HTTP_200_OK)
        except:
            return Response(ERROR_MSG, status=HTTP_500_INTERNAL_SERVER_ERROR)


class UpdateUserDetailsAPI(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            user = request.user
            user_data = request.data
            user_update = update_user_details(user, user_data)
            if user_update:
                return Response(USER_UPDATE_SUCCESS, status=HTTP_200_OK)
            return Response(USER_UPDATE_FAILED, status=HTTP_304_NOT_MODIFIED)
        except:
            return Response(ERROR_MSG, status=HTTP_500_INTERNAL_SERVER_ERROR)


class UserLoginAPI(APIView):
    get_serializer = UserLoginSerializer

    def post(self, request):
        try:
            serializer = self.get_serializer(data=request.data)

            if serializer.is_valid():
                user = serializer.validated_data

                json = fetch_token_for_user(user)

                return Response(json, status=HTTP_200_OK)
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
        except:
            return Response(ERROR_MSG, status=HTTP_500_INTERNAL_SERVER_ERROR)


class UserLogoutAPI(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        try:
            request.user.auth_token.delete()
            return Response(LOGOUT_MSG, status=HTTP_200_OK)
        except:
            return Response(ERROR_MSG, status=HTTP_500_INTERNAL_SERVER_ERROR)
