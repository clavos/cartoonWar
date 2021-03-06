"""cartoonWar URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include

from django.conf import settings
from django.conf.urls.static import static

from card import views as card_views
from forum import views as forum_views

urlpatterns = [
    path('', card_views.home, name='home'),
    path('admin/', admin.site.urls),

    path('accounts/register/', card_views.register, name='register'),
    re_path(r'^accounts/activate/(?P<uid>.+)/(?P<token>.+)', card_views.activate, name='activate'),
    re_path(r'^profile/edit/$', card_views.edit_profile, name='edit_profile'),
    re_path(r'^profile/change-password/$', card_views.change_password, name='change_password'),

    re_path(r'^follow/(?P<operation>.+)/(?P<pk>\d+)/$', card_views.change_follows, name='change_follows'),

    re_path(r'^friendship/(?P<operation>.+)/(?P<pk>\d+)/$', card_views.invite_friend, name='invite_friend'),
    path('invites/', card_views.all_invites, name='all_invites'),
    path('friends/', card_views.all_friends, name='all_friends'),
    re_path(r'^research/$', card_views.get_research, name='get_research'),

    path('card/all/', card_views.get_all_cards, name='all_cards'),
    path('card/buy/', card_views.get_new_cards, name='new_cards'),
    re_path(r'^card/(?P<pk>\d+)/', card_views.get_one_card, name='one_card'),
    re_path(r'^deck/(?P<pk>\d+)/', card_views.get_one_deck, name='one_deck'),
    re_path(r'^connect/(?P<operation>.+)/(?P<deck_pk>\d+)/(?P<pk>\d+)/$', card_views.change_cards, name='change_cards'),
    re_path(r'^connect/(?P<operation>.+)/(?P<pk>\d+)/$', card_views.trade_cards, name='sell_cards'),
    path('accounts/profile/', card_views.profile, name='profile'),

    re_path(r'^profile/$', card_views.view_profile, name='view_profile'),
    re_path(r'^profile/(?P<pk>\d+)/$', card_views.other_profile, name='view_profile_with_pk'),
    re_path(r'^profile/decks/$', card_views.DeckView.as_view(), name='gamer_deck'),

    re_path(r'^game$', card_views.partie, name='game'),
    re_path(r'^game/(?P<deck_pk>\d+)/$', card_views.bot_game, name='bot_game'),
]

urlpatterns += [
    path('forum/article/all', forum_views.get_all_articles, name='all_articles'),
    re_path(r'^forum/article/(?P<pk>\d+)/', forum_views.get_one_article, name='one_article'),
]

urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)