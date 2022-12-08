from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from .models import Message
from .serializers import MessageSerializers
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action


"""
1: username - benny, password - 1234
2: username - abra, passsword - abra1234
"""


class MessagesAll(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    def create(self, request):
        data = JSONParser().parse(request)
        try:
            receiver = User.objects.get(id=data['receiver'])
            message = Message(sender=request.user,receiver=receiver
                ,subject=data['subject'],message=data['message'])
            message.save()
            return Response('The message has been sent', status=status.HTTP_201_CREATED)
        except ObjectDoesNotExist:
            return Response('You cannot send him a message because the user does not exist, Please enter existing user id', status=status.HTTP_404_NOT_FOUND)


    def list(self, request):
        data = Message.objects.filter(~Q(deleted_by=request.user.id),receiver=request.user)
        if not data:
            return Response('There is no messages for you', status=status.HTTP_404_NOT_FOUND)
        else:
            serializer = MessageSerializers(data, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)


    @action(detail=True, methods=['get'])
    def unreadMessages(self, request):
        data = Message.objects.filter(~Q(deleted_by=request.user.id),receiver=request.user,read=False)
        if not data:
            return Response('There is not unread messages for you', status=status.HTTP_404_NOT_FOUND)
        else:
            serializer = MessageSerializers(data, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)


    def update(self, request, pk):
        try:
            data = Message.objects.get(pk=pk,receiver=request.user)
            data.read = True
            data.save()
            serializer = MessageSerializers(data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response('You must be as receiver and have a message with the message ID', status=status.HTTP_404_NOT_FOUND)

    
    def destroy(self, request, pk):
        try:
            data = Message.objects.get(pk=pk)
            if data.sender == request.user or data.receiver == request.user:
                data.deleted_by = request.user.id
                data.save()
                return Response('Message deleted', status=status.HTTP_200_OK)
            else:
                return Response('You need to be the sender or the receiver to delete the message', status=status.HTTP_404_NOT_FOUND)
        except ObjectDoesNotExist:
            return Response('This ID does not have any message', status=status.HTTP_404_NOT_FOUND)




