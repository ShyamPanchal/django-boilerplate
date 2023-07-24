from django.db import models
from django.conf import settings


class TimestampedUserModel(models.Model):
    # A timestamp representing when this object was created.
    created_at = models.DateTimeField(
        auto_now_add=True, db_column="CreatedAt", editable=False
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, db_column="CreatedBy"
    )

    class Meta:
        abstract = True

        # By default, any model that inherits from `TimestampedModel` should
        # be ordered in reverse-chronological order. We can override this on a
        # per-model basis as needed, but reverse-chronological is a good
        # default ordering for most models.
        ordering = ["-created_at"]
        # add, change, delete, and view
        default_permissions = ()
