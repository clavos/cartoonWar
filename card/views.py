from django.conf import settings
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail, BadHeaderError
from django.db.models import Count
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse
from django.views.generic import TemplateView
from card.forms import (
    RegistrationForm,
    EditProfileForm,
    EditExtraProfileForm,
    DeckForm
)
from card.models import Card, Collection, Deck, Collec, UserProfile
from card.game import game
from random import randint
from card.token import activation_token


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
        current_user.userprofile.money -= 100
        current_user.userprofile.save()
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


def other_profile(request, **kwargs):
    user = User.objects.get(pk=kwargs['pk'])
    collec = user.collec_set.all()
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
    return render(request, 'collection/other_profile.html', {"gamer": user, "collec": collec, "values": values})


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
            instance = form.save(commit=False)
            instance.is_active = False
            instance.save()
            site = get_current_site(request)
            subject = "Confirmation message"
            message = render_to_string('registration/confirm_email.html', {
                'user':instance,
                'domain':site.domain,
                'uid':instance.id,
                'token':activation_token.make_token(instance)
            })
            from_email = settings.EMAIL_HOST_USER
            if subject and message and from_email:
                try:
                    send_mail(subject, message, from_email, [instance.email], fail_silently=True)
                except BadHeaderError:
                    return HttpResponse('Invalid header found.')
                return HttpResponseRedirect('/')
            else:
                return HttpResponse('Make sure all fields are entered and valid.')
        else:
            return render(request, 'registration/register.html', {'form': form})
    else:
        form = RegistrationForm()

        args = {'form': form}
        return render(request, 'registration/register.html', args)


def activate(request, **kwargs):

    User.objects.filter(pk=kwargs['uid']).update(is_active=True)
    return redirect('login')


def view_profile(request, pk=None):
    if pk:
        user = User.objects.get(pk=pk)
    else:
        user = request.user
    args = {'user': user}
    return render(request, 'registration/profile.html', args)


def edit_profile(request):
    user = UserProfile.objects.get(user=request.user)
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        extra_form = EditExtraProfileForm(request.POST, instance=user)

        if form.is_valid():
            form.save()
            extra_form.save()
            return redirect('edit_profile')
        else:
            return render(request, 'registration/edit_profile.html', {'form': form, 'extra_form': extra_form})
    else:
        form = EditProfileForm(instance=request.user)
        extra_form = EditExtraProfileForm(request.POST, instance=user)
        args = {'form': form, 'extra_form': extra_form, 'test': user}
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
    nb_card = deck.cards.all().count()
    if operation == 'add' and nb_card < 30:
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


def change_follows(request, operation, pk):
    follower = UserProfile.objects.get(user=User.objects.get(pk=pk))
    if operation == 'add':
        UserProfile.follow_user(request.user, follower)
    elif operation == 'remove':
        UserProfile.unfollow_user(request.user, follower)
    return redirect('get_research')


def partie(request):
    decks = Deck.objects.annotate(nb_card=Count('cards')).filter(nb_card=30, gamer=request.user)
    if request.method == 'POST':
        if request.POST.get("opponent") == "bot":
            return redirect('bot_game', deck_pk=request.POST.get("deck"))
    return render(request, 'game/home_game.html', {'decks': decks})


def bot_game(request, deck_pk):
    current_user = request.user
    deck_player = Deck.objects.get(pk=deck_pk)
    bot_user = User.objects.get(username="root")
    deck_bot = Deck.objects.get(gamer=bot_user, deck_name="Base")

    class Gamer:
        def __init__(self, user, deck, win):
            self.user = user
            self.deck = deck
            self.win = win

    shizawa = Gamer(current_user, deck_player.cards.all(), 0)
    bot = Gamer(bot_user, deck_bot.cards.all(), 0)

    winner = game(shizawa, bot)
    if winner == current_user.username:
        UserProfile.objects.filter(user=current_user).update(money=current_user.userprofile.money+25)
    elif winner == "Nobody":
        UserProfile.objects.filter(user=current_user).update(money=current_user.userprofile.money + 10)

    first = current_user.userprofile.money

    return render(request, 'game/game.html', {'winner': winner, 'first': first})


def get_research(request):
    user_profile = UserProfile.objects.get(user=request.user)
    followers = user_profile.following.all()
    values = {}
    if request.method == 'POST':
        cards = Card.objects.filter(card_name__startswith=request.POST.get("research"))
        users = User.objects.filter(username__startswith=request.POST.get("research"))
    else:
        cards = Card.objects.filter(card_name__startswith="")
        users = User.objects.filter(username__startswith="")
    for all_user in users:
        temp = False
        for my_follower in followers:
            if all_user.pk == my_follower.user.pk:
                temp = True
        if temp is False:
            values[all_user] = False
        else:
            values[all_user] = True
    return render(request, 'research_result.html', {'cards': cards, 'users': users, 'values': values})




