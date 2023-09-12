from django import forms
from django.utils.translation import gettext_lazy as _

from circuits.models import Circuit, CircuitTermination
from dcim.models import *
from utilities.choices import ChoiceSet
from utilities.forms.fields import DynamicModelChoiceField, DynamicModelMultipleChoiceField
from utilities.forms.widgets import HTMXSelect
from .model_forms import CableForm


class CableTerminationChoices(ChoiceSet):
    CIRCUIT_TERMINATION = 'circuittermination'
    CONSOLE_PORT = 'consoleport'
    CONSOLE_SERVER_PORT = 'consoleserverport'
    FRONT_PORT = 'frontport'
    INTERFACE = 'interface'
    POWER_FEED = 'powerfeed'
    POWER_OUTLET = 'poweroutlet'
    POWER_PORT = 'powerport'
    REAR_PORT = 'rearport'

    CHOICES = [
        (CIRCUIT_TERMINATION, _('Circuit Termination'), 'ircuittermination'),
        (CONSOLE_PORT, _('Console Port'), 'consoleport'),
        (CONSOLE_SERVER_PORT, _('Console Server Port'), 'consoleserverport'),
        (FRONT_PORT, _('Front Port'), 'frontport'),
        (INTERFACE, _('Interface'), 'interface'),
        (POWER_FEED, _('Power Feed'), 'powerfeed'),
        (POWER_OUTLET, _('Power Outlet'), 'poweroutlet'),
        (POWER_PORT, _('Power Port'), 'powerport'),
        (REAR_PORT, _('Rear Port'), 'rearport'),
    ]


class CableCircuitTerminationChoices(ChoiceSet):
    INTERFACE = 'interface'
    FRONT_PORT = 'frontport'
    REAR_PORT = 'rearport'
    CIRCUIT_TERMINATION = 'circuittermination'

    CHOICES = [
        (INTERFACE, _('Interface'), 'interface'),
        (FRONT_PORT, _('Front Port'), 'frontport'),
        (REAR_PORT, _('Rear Port'), 'rearport'),
        (CIRCUIT_TERMINATION, _('Circuit Termination'), 'circuittermination'),
    ]


class CableConsolePortTerminationChoices(ChoiceSet):
    CONSOLE_SERVER_PORT = 'consoleserverport'
    FRONT_PORT = 'frontport'
    REAR_PORT = 'rearport'

    CHOICES = [
        (CONSOLE_SERVER_PORT, _('Console Server Port'), 'consoleserverport'),
        (FRONT_PORT, _('Front Port'), 'frontport'),
        (REAR_PORT, _('Rear Port'), 'rearport'),
    ]


class CableConsoleServerPortTerminationChoices(ChoiceSet):
    CONSOLE_PORT = 'consoleport'
    FRONT_PORT = 'frontport'
    REAR_PORT = 'rearport'

    CHOICES = [
        (CONSOLE_PORT, _('Console Port'), 'consoleport'),
        (FRONT_PORT, _('Front Port'), 'frontport'),
        (REAR_PORT, _('Rear Port'), 'rearport'),
    ]


class CableInterfaceTerminationChoices(ChoiceSet):
    INTERFACE = 'interface'
    CIRCUIT_TERMINATION = 'circuittermination'
    FRONT_PORT = 'frontport'
    REAR_PORT = 'rearport'

    CHOICES = [
        (INTERFACE, _('Interface'), 'interface'),
        (CIRCUIT_TERMINATION, _('Circuit Termination'), 'circuittermination'),
        (FRONT_PORT, _('Front Port'), 'frontport'),
        (REAR_PORT, _('Rear Port'), 'rearport'),
    ]


class CableFrontPortTerminationChoices(ChoiceSet):
    CONSOLE_PORT = 'consoleport'
    CONSOLE_SERVER_PORT = 'consoleserverport'
    INTERFACE = 'interface'
    FRONT_PORT = 'frontport'
    REAR_PORT = 'rearport'
    CIRCUIT_TERMINATION = 'circuittermination'

    CHOICES = [
        (CONSOLE_PORT, _('Console Port'), 'consoleport'),
        (CONSOLE_SERVER_PORT, _('Console Server Port'), 'consoleserverport'),
        (INTERFACE, _('Interface'), 'interface'),
        (FRONT_PORT, _('Front Port'), 'frontport'),
        (REAR_PORT, _('Rear Port'), 'rearport'),
        (CIRCUIT_TERMINATION, _('Circuit Termination'), 'circuittermination'),
    ]


class CablePowerFeedTerminationChoices(ChoiceSet):
    POWER_PORT = 'powerport'

    CHOICES = [
        (POWER_PORT, _('Power Port'), 'powerport'),
    ]


class CablePowerOutletTerminationChoices(ChoiceSet):
    POWER_PORT = 'powerport'

    CHOICES = [
        (POWER_PORT, _('Power Port'), 'powerport'),
    ]


class CablePowerPortTerminationChoices(ChoiceSet):
    POWER_OUTLET = 'poweroutlet'
    POWER_FEED = 'powerfeed'

    CHOICES = [
        (POWER_OUTLET, _('Power Outlet'), 'poweroutlet'),
        (POWER_FEED, _('Power Feed'), 'powerfeed'),
    ]


class CableRearPortTerminationChoices(ChoiceSet):
    CONSOLE_PORT = 'consoleport'
    CONSOLE_SERVER_PORT = 'consoleserverport'
    INTERFACE = 'interface'
    FRONT_PORT = 'frontport'
    REAR_PORT = 'rearport'
    CIRCUIT_TERMINATION = 'circuittermination'

    CHOICES = [
        (CONSOLE_PORT, _('Console Port'), 'consoleport'),
        (CONSOLE_SERVER_PORT, _('Console Server Port'), 'consoleserverport'),
        (INTERFACE, _('Interface'), 'interface'),
        (FRONT_PORT, _('Front Port'), 'frontport'),
        (REAR_PORT, _('Rear Port'), 'rearport'),
        (CIRCUIT_TERMINATION, _('Circuit Termination'), 'circuittermination'),
    ]


COMPATIBLE_TERMINATION_TYPES = {
    'circuittermination': ['interface', 'frontport', 'rearport', 'circuittermination'],
    'consoleport': ['consoleserverport', 'frontport', 'rearport'],
    'consoleserverport': ['consoleport', 'frontport', 'rearport'],
    'interface': ['interface', 'circuittermination', 'frontport', 'rearport'],
    'frontport': ['consoleport', 'consoleserverport', 'interface', 'frontport', 'rearport', 'circuittermination'],
    'powerfeed': ['powerport'],
    'poweroutlet': ['powerport'],
    'powerport': ['poweroutlet', 'powerfeed'],
    'rearport': ['consoleport', 'consoleserverport', 'interface', 'frontport', 'rearport', 'circuittermination'],
}


def get_cable_form(a_type, b_type):

    class FormMetaclass(forms.models.ModelFormMetaclass):

        def __new__(mcs, name, bases, attrs):

            for cable_end, term_cls in (('a', a_type), ('b', b_type)):
                print(f"cable_end: {cable_end} term_cls: {term_cls}")
                print(f"term_cls._meta.model_name: {term_cls._meta.model_name}")
                attrs[f'termination_{cable_end}_termination_type'] = forms.ChoiceField(
                    label=_('Termination type'),
                    choices=CableTerminationChoices,
                    initial=term_cls._meta.model_name,
                    widget=HTMXSelect()
                )

                # Device component
                if hasattr(term_cls, 'device'):

                    attrs[f'termination_{cable_end}_device'] = DynamicModelChoiceField(
                        queryset=Device.objects.all(),
                        label=_('Device'),
                        required=False,
                        selector=True,
                        initial_params={
                            f'{term_cls._meta.model_name}s__in': f'${cable_end}_terminations'
                        }
                    )
                    attrs[f'{cable_end}_terminations'] = DynamicModelMultipleChoiceField(
                        queryset=term_cls.objects.all(),
                        label=term_cls._meta.verbose_name.title(),
                        disabled_indicator='_occupied',
                        query_params={
                            'device_id': f'$termination_{cable_end}_device',
                            'kind': 'physical',  # Exclude virtual interfaces
                        }
                    )

                # PowerFeed
                elif term_cls == PowerFeed:

                    attrs[f'termination_{cable_end}_powerpanel'] = DynamicModelChoiceField(
                        queryset=PowerPanel.objects.all(),
                        label=_('Power Panel'),
                        required=False,
                        selector=True,
                        initial_params={
                            'powerfeeds__in': f'${cable_end}_terminations'
                        }
                    )
                    attrs[f'{cable_end}_terminations'] = DynamicModelMultipleChoiceField(
                        queryset=term_cls.objects.all(),
                        label=_('Power Feed'),
                        disabled_indicator='_occupied',
                        query_params={
                            'power_panel_id': f'$termination_{cable_end}_powerpanel',
                        }
                    )

                # CircuitTermination
                elif term_cls == CircuitTermination:

                    attrs[f'termination_{cable_end}_circuit'] = DynamicModelChoiceField(
                        queryset=Circuit.objects.all(),
                        label=_('Circuit'),
                        selector=True,
                        initial_params={
                            'terminations__in': f'${cable_end}_terminations'
                        }
                    )
                    attrs[f'{cable_end}_terminations'] = DynamicModelMultipleChoiceField(
                        queryset=term_cls.objects.all(),
                        label=_('Side'),
                        disabled_indicator='_occupied',
                        query_params={
                            'circuit_id': f'$termination_{cable_end}_circuit',
                        }
                    )

            return super().__new__(mcs, name, bases, attrs)

    class _CableForm(CableForm, metaclass=FormMetaclass):

        def __init__(self, *args, **kwargs):
            # TODO: Temporary hack to work around list handling limitations with utils.normalize_querydict()
            for field_name in ('a_terminations', 'b_terminations'):
                if field_name in kwargs.get('initial', {}) and type(kwargs['initial'][field_name]) is not list:
                    kwargs['initial'][field_name] = [kwargs['initial'][field_name]]

            super().__init__(*args, **kwargs)

            if self.instance and self.instance.pk:
                # Initialize A/B terminations when modifying an existing Cable instance
                self.initial['a_terminations'] = self.instance.a_terminations
                self.initial['b_terminations'] = self.instance.b_terminations

        def clean(self):
            super().clean()

            # Set the A/B terminations on the Cable instance
            self.instance.a_terminations = self.cleaned_data['a_terminations']
            self.instance.b_terminations = self.cleaned_data['b_terminations']

    return _CableForm
