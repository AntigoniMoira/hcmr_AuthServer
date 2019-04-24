"""
Django forms for use with the dot-restrict-scopes package.
"""

from django import forms

from oauth2_provider.scopes import get_scopes_backend


class DelimitedListField(forms.MultipleChoiceField):
    """
    Django form field that allows for the use of list widgets with a text field
    containing a delimited list.
    """
    delimiter = ','

    def __init__(self, delimiter = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.delimiter = delimiter or self.delimiter

    def prepare_value(self, value):
        # If the value is already a list or tuple, just use it as-is
        if isinstance(value, (list, tuple)): return value
        # Otherwise, prepare the value by splitting on the delimiter, trimming
        # leading and trailing whitespace and excluding empty values
        return [p.strip() for p in value.split(self.delimiter) if p.strip()]

    def clean(self, value):
        # Let the parent clean the value first, then join the result using the
        # specified delimiter
        return self.delimiter.join(super().clean(value))


class RestrictedApplicationForm(forms.ModelForm):
    """
    Form for creating or updating a restricted application.
    """
    # allowed_scope is a space-delimited list, but we want to present
    # a selection of valid scopes with checkboxes
    allowed_scope = DelimitedListField(
        label = 'Allowed scopes',
        # The choices and initial values are callables, because the scopes might
        # not be available at import type, e.g. if coming from the database
        choices = lambda: get_scopes_backend().get_all_scopes().items(),
        initial = lambda: get_scopes_backend().get_default_scopes(),
        delimiter = ' ',
        widget = forms.CheckboxSelectMultiple
    )

    class Meta:
        exclude = ()
