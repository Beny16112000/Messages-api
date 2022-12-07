from rest_framework import serializers
from .models import Message


class MessageSerializers(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = [
            'id',
            'sender',
            'receiver',
            'subject',
            'message',
            'created',
            'read'
        ]

"""
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['sender'], data['receiver'] = instance.sender.username, instance.receiver.username
        return data
"""
        
