import copy

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from core.forms.mixins import SyncedDataMixin
from core.models import *
from netbox.forms import NetBoxModelForm
from netbox.registry import registry
from pathlib import Path
from utilities.forms import get_field_value
from utilities.forms.fields import CommentField
from utilities.forms.widgets import HTMXSelect

__all__ = (
    'DataSourceForm',
    'ManagedFileForm',
)


class DataSourceForm(NetBoxModelForm):
    comments = CommentField()

    class Meta:
        model = DataSource
        fields = [
            'name', 'type', 'source_url', 'enabled', 'description', 'comments', 'ignore_rules', 'tags',
        ]
        widgets = {
            'type': HTMXSelect(),
            'ignore_rules': forms.Textarea(
                attrs={
                    'rows': 5,
                    'class': 'font-monospace',
                    'placeholder': '.cache\n*.txt'
                }
            ),
        }

    @property
    def fieldsets(self):
        fieldsets = [
            (_('Source'), ('name', 'type', 'source_url', 'enabled', 'description', 'tags', 'ignore_rules')),
        ]
        if self.backend_fields:
            fieldsets.append(
                (_('Backend Parameters'), self.backend_fields)
            )

        return fieldsets

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Determine the selected backend type
        backend_type = get_field_value(self, 'type')
        backend = registry['data_backends'].get(backend_type)

        # Add backend-specific form fields
        self.backend_fields = []
        for name, form_field in backend.parameters.items():
            field_name = f'backend_{name}'
            self.backend_fields.append(field_name)
            self.fields[field_name] = copy.copy(form_field)
            if self.instance and self.instance.parameters:
                self.fields[field_name].initial = self.instance.parameters.get(name)

    def save(self, *args, **kwargs):

        parameters = {}
        for name in self.fields:
            if name.startswith('backend_'):
                parameters[name[8:]] = self.cleaned_data[name]
        self.instance.parameters = parameters

        return super().save(*args, **kwargs)


class ManagedFileForm(SyncedDataMixin, NetBoxModelForm):
    upload_file = forms.FileField(
        required=False
    )

    fieldsets = (
        (_('File Upload'), ('upload_file',)),
        (_('Data Source'), ('data_source', 'data_file', 'auto_sync_enabled')),
    )

    class Meta:
        model = ManagedFile
        fields = ('data_source', 'data_file', 'auto_sync_enabled')

    def _validate_file_extension(self, file):
        if file:
            extension = Path(file.name).suffix[1:].lower()

            if extension != "py":
                raise ValidationError(
                    "File extension “%(extension)s” is not allowed .py extension is required",
                    code="invalid_extension",
                    params={
                        "extension": extension,
                    },
                )

    def clean(self):
        super().clean()

        upload_file = self.cleaned_data['upload_file']
        data_file = self.cleaned_data['data_file']

        if upload_file and data_file:
            extension = Path(upload_file.name).suffix[1:].lower()
            raise forms.ValidationError("Cannot upload a file and sync from an existing file")
        if not upload_file and not data_file:
            raise forms.ValidationError("Must upload a file or select a data file to sync")

        self._validate_file_extension(upload_file)
        self._validate_file_extension(data_file)

        return self.cleaned_data

    def save(self, *args, **kwargs):
        # If a file was uploaded, save it to disk
        if self.cleaned_data['upload_file']:
            self.instance.file_path = self.cleaned_data['upload_file'].name
            with open(self.instance.full_path, 'wb+') as new_file:
                new_file.write(self.cleaned_data['upload_file'].read())

        return super().save(*args, **kwargs)
