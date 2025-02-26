from django.shortcuts import render

from rest_framework.views import APIView

from rest_framework.response import Response

from api.serializers import UserCreationSerializer

# Create your views here.

class SignUpView(APIView):

    def post(self,request,*args,**kwargs):

        serializer_instance=UserCreationSerializer(data=request.data)

        if serializer_instance.is_valid():

            serializer_instance.save()

            return Response(data=serializer_instance.data)
        
        else:

            return Response(data=serializer_instance.errors)
