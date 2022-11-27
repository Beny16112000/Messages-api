from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from .models import Message
from .serializers import MessageSerializers




class MessagesAll(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = JSONParser().parse(request)
        receiver = User.objects.filter(id=data['receiver'])
        if not receiver:
            return Response('You cannot send him a message because the user does not exist, Please enter existing user id', status=status.HTTP_404_NOT_FOUND)
        else:
            receiver = User.objects.get(id=data['receiver'])
            message = Message(sender=request.user,receiver=receiver,subject=data['subject'],message=data['message'])
            message.save()
            return Response('The message has been sent', status=status.HTTP_201_CREATED)


    def get(self, request):
        data = Message.objects.filter(receiver=request.user)
        if not data:
            return Response('There is no messages for you', status=status.HTTP_404_NOT_FOUND)
        else:
            serializer = MessageSerializers(data, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def unread_messages(request):
    if request.method == 'GET':
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
            message = Message.objects.get(id=id,receiver=request.user)
            message.read = True
            message.save()
            serializer = MessageSerializers(message)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self,request,id):
        data = Message.objects.filter(id=id,sender=request.user) or Message.objects.filter(id=id,receiver=request.user)
        if not data:
            return Response('To delete this message, You need to be sender or receiver and have the id of the message', status=status.HTTP_404_NOT_FOUND)
        else:
            message = Message.objects.get(id=id)
            message.delete()
            return Response('Message deleted', status=status.HTTP_204_NO_CONTENT)
