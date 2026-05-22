from django import forms
from django.utils.translation import gettext_lazy as _


class MultipleFileInput(forms.ClearableFileInput):
    """
    Extends the standard file input to allow selecting multiple files at once.
    Works with <input type="file" multiple>.
    """
    allow_multiple_selected = True

    def __init__(self, attrs=None):
        default_attrs = {
            "multiple":  True,
            "accept":    "image/*",
            "class":     "multiple-file-input",
        }
        if attrs:
            default_attrs.update(attrs)
        super().__init__(attrs=default_attrs)


class MultipleFileField(forms.FileField):
    """
    A FileField variant that accepts multiple file uploads.
    Returns a list of InMemoryUploadedFile objects.
    """
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        """Clean each uploaded file individually and return a list."""
        single_file_clean = super().clean

        if isinstance(data, (list, tuple)):
            # Multiple files submitted
            result = [single_file_clean(d, initial) for d in data if d]
        elif data:
            # Single file submitted through the multi-input
            result = [single_file_clean(data, initial)]
        else:
            result = []

        if not result and self.required:
            raise forms.ValidationError(self.error_messages["required"])

        return result