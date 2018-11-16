from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from card.models import Deck, Card


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
    template_name = '/something/else'

    class Meta:
        model = User
        fields = (
            'email',
            'first_name',
            'last_name',
            'password'
        )


class DeckForm(forms.ModelForm):
    # cards = forms.ModelMultipleChoiceField(queryset=Card.objects.all())

    class Meta:
        model = Deck
        fields = (
            'deck_name',
            # 'cards'
        )

    def save(self, commit=True):
        deck = super(DeckForm, self).save(commit=False)
        deck.deck_name = self.cleaned_data['deck_name']
        # deck.cards = self.cards

        if commit:
            deck.save()

        return deck

