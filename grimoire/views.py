from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return HttpResponse("Page Grimoire que l'utilisateur atteint quand il souhaite consulter ses deck et cartes")
