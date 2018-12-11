from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import TemplateView
from random import randint

from card.forms import (
    RegistrationForm,
    EditProfileForm,
    DeckForm
)

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

from card.models import Card, Collection, Deck, Collec


def home(request):
    return render(request, 'home.html')


def get_all_cards(request):
    cards = Card.objects.all()
    return render(request, 'cards/cards.html', {"cards": cards, "title": "All the cards"})


def get_one_card(request, **kwargs):
    card = Card.objects.get(pk=kwargs['pk'])
    return render(request, 'cards/detail_card.html', {"card": card})


def get_new_cards(request):
    current_user = request.user
    if current_user.userprofile.money > 100:
        # current_user.userprofile.money -= 100
        # current_user.userprofile.save()
        card_count = Card.objects.all().count()
        cards = []
        for i in range(8):
            id = randint(1, card_count)
            cards.append(Card.objects.get(pk=id))
            collection = Collec.objects.get_or_create(current_user=current_user, cards=Card.objects.get(pk=id))
            quantity = Collec.objects.get(current_user=current_user, cards=Card.objects.get(pk=id)).quantity
            collection = Collec.objects.filter(current_user=current_user, cards=Card.objects.get(pk=id)).update(
                quantity=quantity + 1)
        return render(request, 'cards/detail_pack.html', {"cards": cards})
    else:
        return render(request, 'cards/no_pack.html')


def profile(request):
    current_user = request.user
    collec = current_user.collec_set.all()
    cards = Card.objects.all()
    values = {}
    for all_card in cards:
        temp = False
        for my_collec in collec:
            if all_card.pk == my_collec.cards.pk:
                temp = True
        if temp is False:
            values[all_card] = False
        else:
            values[all_card] = True

    return render(request, 'registration/profile.html', {"gamer": current_user, "collec": collec, "values": values})


def get_one_deck(request, **kwargs):
    deck = Deck.objects.get(pk=kwargs['pk'])
    current_user = request.user
    cards = current_user.cards.all()
    return render(request, 'cards/detail_deck.html', {"cards": cards, "deck": deck})


class DeckView(TemplateView):
    template_name = 'cards/add_deck.html'

    def get(self, request):
        form = DeckForm()
        decks = Deck.objects.filter(gamer=request.user)

        args = {
            'form': form, 'decks': decks
        }
        return render(request, self.template_name, args)

    def post(self, request):
        form = DeckForm(request.POST)
        if form.is_valid():
            deck = form.save(commit=False)
            deck.gamer = request.user
            # deck.deck_name = form.cleaned_data['deck_name']
            # deck.cards.set(form['cards'])
            deck.save()

            return redirect('gamer_deck')

        text = form.cleaned_data['deck_name']
        form = DeckForm()
        args = {'form': form, 'text': text}
        return render(request, self.template_name, args)


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'home.html')
        else:
            return render(request, 'registration/register.html', {'form': form})
    else:
        form = RegistrationForm()

        args = {'form': form}
        return render(request, 'registration/register.html', args)


def view_profile(request, pk=None):
    if pk:
        user = User.objects.get(pk=pk)
    else:
        user = request.user
    args = {'user': user}
    return render(request, 'registration/profile.html', args)


def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = EditProfileForm(instance=request.user)
        args = {'form': form}
        return render(request, 'registration/edit_profile.html', args)


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('profile')
        else:
            return render(request, 'registration/change_password.html', {'form': form})
    else:
        form = PasswordChangeForm(user=request.user)

        args = {'form': form}
        return render(request, 'registration/change_password.html', args)


def change_cards(request, operation, pk, deck_pk):
    card = Card.objects.get(pk=pk)
    deck = Deck.objects.get(pk=deck_pk)
    if operation == 'add':
        Deck.make_card(deck, request.user, card)
    elif operation == 'remove':
        Deck.lose_card(deck, request.user, card)
    return redirect('one_deck', pk=deck_pk)


def trade_cards(request, operation, pk):
    current_user = request.user
    card = Card.objects.get(pk=pk)
    if operation == 'sell':
        Collec.swap_card(card, current_user)
    elif operation == 'remove':
        Collec.swap_card(card, current_user)
    return redirect('profile')
