from nodesavestate.models import State
from nodesavestate.serializers import StateSerializer

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated



class StateViewSet(viewsets.ModelViewSet):
    queryset = State.objects.all()
    serializer_class = StateSerializer
    permission_classes = (IsAuthenticated,)