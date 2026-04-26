from django.db import models as dj_models 
import uuid



class PrimaryKeyMixin(dj_models.Model):
    id = dj_models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class DateHistoryMixin(dj_models.Model):
    created_at = dj_models.DateTimeField(auto_now_add=True)
    updated_at = dj_models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
