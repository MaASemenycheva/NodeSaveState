from django.db import models

# Create your models here.
class State(models.Model):
    chat_id = models.TextField()
    node_id = models.TextField()

    class Meta:
        db_table = 'state'