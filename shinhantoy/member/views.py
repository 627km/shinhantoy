from django.shortcuts import render
from rest_framework import mixins, generics
from .serializers import MemberSerializer
from rest_framework.views import APIView
from .models import Member
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import check_password, make_password
from rest_framework.permissions import IsAuthenticated

# Create your views here.

class MemberRegisterView(
    mixins.CreateModelMixin,
    generics.GenericAPIView
):
    serializer_class = MemberSerializer
    
    def post(self, request, *args, **kwargs):
        return self.create(request, args, kwargs)
    
class MemberChangePasswordView(APIView):
    # 로그인된 사용자만 사용할 수 있도록 
    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        current = request.data.get('current')
        password1 = request.data.get('password1')
        password2 = request.data.get('password2')

        if password1 != password2:
            return Response({
                'detail': 'Wrong new passwords',
            }, status=status.HTTP_400_BAD_REQUEST)
        
        member = request.user
        
        if not check_password(current, member.password):
            return Response({
                'detail': 'Wrong password',
            }, status=status.HTTP_400_BAD_REQUEST)

        member.password = make_password(password1)
        member.save()

        return Response(status=status.HTTP_200_OK)
