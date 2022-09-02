import uuid

from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

NULL_AND_BLANK = {"null": True, "blank": True}


class Location(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name="ID",
        help_text=_(
            """The unique identifier of the instance this object belongs to. 
            Mandatory, unless a new instance to create is given."""
        )
    )
    ip = models.GenericIPAddressField(
            editable=False,
            **NULL_AND_BLANK,
            verbose_name=_("IP Address"),
            help_text=_("The IP Address of the user at the time of creating record.")
        )

    type = models.CharField(
        **NULL_AND_BLANK,
        max_length=50
    )

    continent_code = models.CharField(
        **NULL_AND_BLANK,
        max_length=50
    )

    continent_name = models.CharField(
        **NULL_AND_BLANK,
        max_length=50
    )

    country_code = models.CharField(
        **NULL_AND_BLANK,
        max_length=50
    )

    country_name = models.CharField(
        **NULL_AND_BLANK,
        max_length=50
    )

    region_code = models.CharField(
        **NULL_AND_BLANK,
        max_length=50
    )

    region_name = models.CharField(
        **NULL_AND_BLANK,
        max_length=50
    )

    city = models.CharField(
        **NULL_AND_BLANK,
        max_length=50
    )

    zip = models.CharField(
        **NULL_AND_BLANK,
        max_length=50
    )

    latitude = models.CharField(
        **NULL_AND_BLANK,
        max_length=50
    )

    longitude = models.CharField(
        **NULL_AND_BLANK,
        max_length=50
    )
    
    location = models.JSONField(
        default=None,
        null=True,
    )

    time_zone = models.JSONField(
        default=None,
        null=True,
    )

    currency = models.JSONField(
        default=None,
        null=True,
    )

    connection = models.JSONField(
        default=None,
        null=True,
    )


    security = models.JSONField(
        default=None,
        null=True,
    )


    created_at = models.DateTimeField(
        default=timezone.now,
        editable=False,
        verbose_name=_('Created'),
        help_text=_(
            """Timestamp when the record was created. The date and time 
            are displayed in the Timezone from where request is made. 
            e.g. 2019-14-29T00:15:09Z for April 29, 2019 0:15:09 UTC"""
        )
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        editable=False,
        verbose_name=_('Updated'),
        **NULL_AND_BLANK,
        help_text=_(
            """Timestamp when the record was modified. The date and 
            time are displayed in the Timezone from where request 
            is made. e.g. 2019-14-29T00:15:09Z for April 29, 2019 0:15:09 UTC
            """)
    )
    #Metadata
    class Meta :
        ordering = ['-created_at']

    #Methods

    def __str__(self):
        return self.ip
