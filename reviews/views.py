from django.shortcuts import render
from django.http import HttpResponse


def reviews(request):
    return HttpResponse("J'accède au flux")
