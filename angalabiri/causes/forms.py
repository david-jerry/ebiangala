from django import forms
from angalabiri.causes.models import Cause
from ckeditor_uploader.widgets import CKEditorUploadingWidget

# from .models import Comment
import datetime


class CauseCreateForm(forms.ModelForm):
    class Meta:
        model = Cause
        exclude = ["added_by", "created", "updated", "tt_amount", "author", "slug"]
