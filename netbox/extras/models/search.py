import uuid

from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import gettext_lazy as _

from netbox.registry import registry
from utilities.fields import RestrictedGenericForeignKey
from utilities.utils import content_type_identifier
from ..fields import CachedValueField

__all__ = (
    'CachedValue',
)


class CachedValue(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    timestamp = models.DateTimeField(
        verbose_name=_('timestamp'),
        auto_now_add=True,
        editable=False
    )
    object_type = models.ForeignKey(
        to=ContentType,
        on_delete=models.CASCADE,
        related_name='+'
    )
    object_id = models.PositiveBigIntegerField()
    object = RestrictedGenericForeignKey(
        ct_field='object_type',
        fk_field='object_id'
    )
    field = models.CharField(
        verbose_name=_('field'),
        max_length=200
    )
    type = models.CharField(
        verbose_name=_('type'),
        max_length=30
    )
    value = CachedValueField(
        verbose_name=_('value'),
    )
    weight = models.PositiveSmallIntegerField(
        verbose_name=_('weight'),
        default=1000
    )

    class Meta:
        ordering = ('weight', 'object_type', 'object_id')
        verbose_name = _('cached value')
        verbose_name_plural = _('cached values')

    def __str__(self):
        return f'{self.object_type} {self.object_id}: {self.field}={self.value}'

    @property
    def display_attrs(self):
        indexer = registry['search'].get(content_type_identifier(self.object_type))
        attrs = {}
        for attr in getattr(indexer, 'display_attrs', []):
            name = self.object._meta.get_field(attr).verbose_name
            if value := getattr(self.object, attr):
                if display_func := getattr(self.object, f'get_{attr}_display', None):
                    attrs[name] = display_func()
                else:
                    attrs[name] = value
        return attrs
