from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from .models import Message
from .serializers import MessageSerializers
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist



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
        try:
            receiver = User.objects.get(id=data['receiver'])
            message = Message(sender=request.user,receiver=receiver
                ,subject=data['subject'],message=data['message'])
            message.save()
            return Response('The message has been sent', status=status.HTTP_201_CREATED)
        except ObjectDoesNotExist:
            return Response('You cannot send him a message because the user does not exist, Please enter existing user id', status=status.HTTP_404_NOT_FOUND)


    def get(self, request):
        """
        from myapp.models import Entry
        from django.db.models import Q
        Entry.objects.filter(~Q(id=3))
        """
        data = Message.objects.filter(~Q(deleted_by=request.user.id),receiver=request.user)
        if not data:
            return Response('There is no messages for you', status=status.HTTP_404_NOT_FOUND)
        else:
            serializer = MessageSerializers(data, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)



class MessagesUnread(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        data = Message.objects.filter(~Q(deleted_by=request.user.id),receiver=request.user,read=False)
        if not data:
            return Response('There is not unread messages for you', status=status.HTTP_404_NOT_FOUND)
        else:
            serializer = MessageSerializers(data, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)



class Messages(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request,id):
        try:
            data = Message.objects.get(id=id,receiver=request.user)
            data.read = True
            data.save()
            serializer = MessageSerializers(data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response('You must be as receiver and have a message with the message ID', status=status.HTTP_404_NOT_FOUND)


    def delete(self,request,id):
        try:
            data = Message.objects.get(id=id)
            if data.sender == request.user or data.receiver == request.user:
                data.deleted_by = request.user.id # Delete only to the user that want to delete.
                data.save() 
                return Response('Message deleted', status=status.HTTP_200_OK)
            else:
                return Response('You need to be the sender or the receiver to delete the message', status=status.HTTP_404_NOT_FOUND)
        except ObjectDoesNotExist:
            return Response('This ID does not have any message', status=status.HTTP_404_NOT_FOUND)

