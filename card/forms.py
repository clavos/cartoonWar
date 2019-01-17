from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from card.models import Deck, Card, UserProfile


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2'
        )

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']

        if commit:
            user.save()

        return user


class EditProfileForm(UserChangeForm):
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={
            'class': 'form-control',
            'id': 'email',
        }
    ))
    first_name = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'id': 'first_name',
        }
    ))
    last_name = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'id': 'last_name',
        }
    ))

    class Meta:
        model = User
        fields = (
            'email',
            'first_name',
            'last_name',
        )

class EditExtraProfileForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea(
        attrs={
            'class': 'form-control',
            'id': 'description',
        }
    ))
    class Meta:
        model = UserProfile
        fields = (
            'description',
            'phone',
        )


class DeckForm(forms.ModelForm):
    deck_name = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Nom du deck',
        }
    ))

    class Meta:
        model = Deck
        fields = (
            'deck_name',
        )

    def save(self, commit=True):
        deck = super(DeckForm, self).save(commit=False)
        deck.deck_name = self.cleaned_data['deck_name']

        if commit:
            deck.save()

        return deck

