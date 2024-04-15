from django.forms import (
    ModelForm,
    CharField,
    TextInput,
    Textarea,
)

from quotesapp.models import Author


class AuthorForm(ModelForm):
    fullname = CharField(max_length=255, widget=TextInput())
    born_date = CharField(max_length=20, widget=TextInput())
    born_location = CharField(max_length=255, widget=TextInput())
    description = CharField(max_length=1500, widget=Textarea())

    class Meta:
        model = Author
        fields = ["fullname", "born_date", "born_location", "description"]
