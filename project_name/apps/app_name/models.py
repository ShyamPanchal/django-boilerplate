from django.db import models

# Create your models here.
from django.db import models
from ..core.models import TimestampedUserModel


class Task(TimestampedUserModel):
    id = models.AutoField(primary_key=True, db_column="TaskId")
    name = models.CharField(db_column="Name", max_length=128, unique=True)

    class Meta(TimestampedUserModel.Meta):
        db_table = f'"{{ project_name }}"."Task"'

    def __str__(self) -> str:
        return f"{self.name}"

    def __repr__(self) -> str:
        return super().__str__()
