from django.shortcuts import render,HttpResponse
from .models import *
from.serializers import *
from rest_framework.views import APIView
from .permissions import *
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class UserRegisterView(APIView):
   def post(self,request,format=None):
    serializer = SignupSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data,status=status.HTTP_201_CREATED)
   

   

class UserLoginView(APIView):
    def post(self, request, format=None):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data.get('email')
        password = serializer.data.get('password')
        user = authenticate(email=email, password=password)
        if user is not None:
            token = get_tokens_for_user(user)
            return Response({'token':token,'msg':'Login Success'}, status=status.HTTP_200_OK)
        else:
            return Response({'errors':{'non_field_errors':['Email or Password is not Valid']}}, status=status.HTTP_404_NOT_FOUND)


class UserLogoutView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, format=None):
        try:
            refresh_token = request.META.get('HTTP_REFRESH')
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({'msg':'Logout Success'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'msg':'Invalid Token'}, status=status.HTTP_401_UNAUTHORIZED)


class BlogCreateview(APIView):
    permission_classes = [IsAdmin]
    def post(self, request):
        serializer = BlogSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class BlogGetview(APIView):
    permission_classes = [IsAdmin | IsManager | IsSupport | IsGuest]
    def get(self,request):
        blogs = Blog.objects.all()
        serializer = BlogSerializer(blogs, many=True)
        return Response(serializer.data)


class BlogUpdateView(APIView):
    permission_classes = [IsAdmin | IsManager]

    def get_object(self, pk):
        try:
            return Blog.objects.get(pk=pk)
        except Blog.DoesNotExist:
            return HttpResponse(status=404)

    def put(self, request, pk, format=None):
        blog = self.get_object(pk)
        serializer = BlogSerializer(blog, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class BlogDelete(APIView):
    permission_classes = [IsAdmin]
    def get_object(self, pk):
        try:
            return Blog.objects.get(pk=pk)
        except Blog.DoesNotExist:
            return HttpResponse(status=404)
    def delete(self, request, pk, format=None):
        blog = self.get_object(pk)
        blog.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        

    
        



        
