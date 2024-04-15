from django.forms import (
    ModelForm,
    CharField,
    ModelMultipleChoiceField,
    ModelChoiceField,
    TextInput,
    CheckboxSelectMultiple,
)
from .models import Tag, Author, Quote


class QuoteForm(ModelForm):
    quote = CharField(max_length=1000, widget=TextInput())

    author = ModelChoiceField(queryset=Author.objects.all())

    tags = ModelMultipleChoiceField(
        queryset=Tag.objects.all(), widget=CheckboxSelectMultiple
    )

    class Meta:
        model = Quote
        fields = ["quote", "author", "tags"]
