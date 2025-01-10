from django.http import HttpRequest, HttpResponse, HttpResponseNotFound
from django.shortcuts import render

# Create your views here.
def index(request: HttpRequest):
    return HttpResponse(f"Страница приложения kinosite")


def film(request: HttpRequest, film_id):
    return HttpResponse(f"Страница приложения kinosite:\nФильм: {film_id}")


def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена :(</h1>")