from django.shortcuts import render
from django.http import HttpResponse


def flux(request):
    return HttpResponse("J'accède au flux'")
