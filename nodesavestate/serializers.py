from rest_framework import serializers
from nodesavestate.models import State

class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = State
        # fields = '__all__'
        fields = ('chat_id', 'node_id')
