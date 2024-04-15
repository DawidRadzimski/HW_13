from django.forms import (
    ModelForm,
    CharField,
    TextInput,
)

from quotesapp.models import Tag


class TagForm(ModelForm):

    name = CharField(min_length=3, max_length=25, widget=TextInput())

    class Meta:
        model = Tag
        fields = ["name"]
