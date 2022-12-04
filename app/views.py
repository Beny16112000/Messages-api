from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from .models import Message
from .serializers import MessageSerializers
from django.db.models import Q


"""
1: 
username - benny
password - 1234
2:
username - abra
passsword - abra1234
"""


class MessagesAll(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = JSONParser().parse(request)
        receiver = User.objects.filter(id=data['receiver'])
        if not receiver:
            return Response('You cannot send him a message because the user does not exist, Please enter existing user id', status=status.HTTP_404_NOT_FOUND)
        else:
            message = Message(sender=request.user,receiver=receiver[0],subject=data['subject'],message=data['message'])
            message.save()
            return Response('The message has been sent', status=status.HTTP_201_CREATED)


    def get(self, request):
        data = Message.objects.filter(receiver=request.user)
        if not data:
            return Response('There is no messages for you', status=status.HTTP_404_NOT_FOUND)
        else:
            serializer = MessageSerializers(data, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        

class MessagesUnread(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        data = Message.objects.filter(receiver=request.user,read=False)
        if not data:
            return Response('It appears that you do not have any unread messages', status=status.HTTP_404_NOT_FOUND)
        else:
            serializer = MessageSerializers(data, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)



class Messages(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request,id):
        data = Message.objects.filter(id=id,receiver=request.user)
        if not data:
            return Response('You must be as receiver and have a message with the message ID', status=status.HTTP_404_NOT_FOUND)
        else:
            data[0].read = True
            data[0].save()
            serializer = MessageSerializers(data[0])
            return Response(serializer.data, status=status.HTTP_200_OK)


    def delete(self,request,id):
        data = Message.objects.filter(id=id)
        if not data:
            return Response('This ID does not have any message', status=status.HTTP_404_NOT_FOUND)
        else:
            if data[0].sender == request.user or data[0].receiver == request.user:
                data[0].delete()
                return Response('Message deleted', status=status.HTTP_200_OK)
            else:
                return Response('You need to be the sender or the receiver to delete the message', status=status.HTTP_404_NOT_FOUND)
