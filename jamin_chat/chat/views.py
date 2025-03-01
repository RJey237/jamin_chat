from django.shortcuts import render
from django.views.generic import TemplateView
# Create your views here.
class IndexView(TemplateView):
    template_name='index.html'

def room(request, room_name):
    return render(request, "room.html", {"room_name": room_name})