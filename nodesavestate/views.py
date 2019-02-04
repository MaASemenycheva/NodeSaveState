from nodesavestate.models import State
from nodesavestate.serializers import StateSerializer

from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import JSONParser
from django.shortcuts import get_object_or_404
#from nodesavestate.models import State
#from nodesavestate.models import fun_raw_sql_query, fun_sql_cursor_update
#from nodesavestate.serializers import StateSerializer, StateSerializerV1
from nodesavestate.serializers import StateSerializer

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import detail_route, list_route


class StateViewSet(viewsets.ModelViewSet):
    queryset = State.objects.all()
    serializer_class = StateSerializer
    permission_classes = (IsAuthenticated,)
    parser_classes = (JSONParser,)

    # /api/state/{pk}/detail/
    @detail_route(methods=['get'])
    def detail(self, request, pk=None):
        state = get_object_or_404(State, pk=pk)
        result = {
            'chat_id': state.chat_id,
            'node_id': state.node_id
        }

        return Response(result, status=status.HTTP_200_OK)

    # /api/music/all_singer/
    @list_route(methods=['get'])
    def all_chat_id(self, request):
        music = State.objects.values_list('chat_id', flat=True).distinct()
        return Response(state, status=status.HTTP_200_OK)

    # /api/music/raw_sql_query/
    @list_route(methods=['get'])
    def raw_sql_query(self, request):
        song = request.query_params.get('song', None)
        music = fun_raw_sql_query(song=song)
        serializer = StateSerializer(music, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # /api/music/{pk}/sql_cursor_update/
    @detail_route(methods=['put'])
    def sql_cursor_update(self, request, pk=None):
        song = request.data.get('song', None)
        if song:
            music = fun_sql_cursor_update(song=song, pk=pk)
            return Response(music, status=status.HTTP_200_OK)

    # /api/music/version_api/
    @list_route(methods=['get'])
    def version_api(self, request):
        music = State.objects.all()
        if self.request.version == '1.0':
            serializer = StateSerializerV1(music, many=True)
        else:
            serializer = StateSerializer(music, many=True)


            return Response(serializer.data, status=status.HTTP_200_OK)