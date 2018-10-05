from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return HttpResponse("Page Home que l'utilisateur atteint en se connectant")
