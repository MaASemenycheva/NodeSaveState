from django.db import models
from collections import namedtuple
from django.db import connection

class State(models.Model):
    chat_id = models.TextField()
    node_id = models.TextField()

    class Meta:
        db_table = "state"
        app_label = "state"


def fun_raw_sql_query(**kwargs):
    chat_id = kwargs.get('chat_id')
    if chat_id:
        result = State.objects.raw('SELECT * FROM state WHERE chat_id = %s', [chat_id])
    else:
        result = State.objects.raw('SELECT * FROM state')
    return result

def fun_raw_sql_query_node_id(**kwargs):
    node_id = kwargs.get('node_id')
    if node_id:
        result = State.objects.raw('SELECT * FROM state WHERE node_id = %s', [node_id])
    else:
        result = State.objects.raw('SELECT * FROM state')
    return result


def namedtuplefetchall(cursor):
    # Return all rows from a cursor as a namedtuple
    desc = cursor.description
    nt_result = namedtuple('Result', [col[0] for col in desc])
    return [nt_result(*row) for row in cursor.fetchall()]


def fun_sql_cursor_update(**kwargs):
    chat_id = kwargs.get('chat_id')
    pk = kwargs.get('pk')

    '''
    Note that if you want to include literal percent signs in the query,
    you have to double them in the case you are passing parameters:
    '''
    with connection.cursor() as cursor:
        cursor.execute("UPDATE state SET chat_id = %s WHERE id = %s", [chat_id, pk])
        cursor.execute("SELECT * FROM music WHERE id = %s", [pk])
        # result = cursor.fetchone()
        result = namedtuplefetchall(cursor)
    result = [
        {
            'id': r.id,
            'chat_id': r.chat_id,
            'node_id': r.node_id,

        }
        for r in result
    ]

    return result