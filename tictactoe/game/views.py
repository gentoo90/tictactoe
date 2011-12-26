from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
import pusher

PUSHER = {
    'APP_ID':'9983',
    'KEY':'bc9867d3dadaea0b8a27',
    'SECRET':'ac1dba415b21fde5245e'
}

pusher.app_id = PUSHER['APP_ID']
pusher.key = PUSHER['KEY']
pusher.secret = PUSHER['SECRET']
p = pusher.Pusher()

def select_player(request):
    return render_to_response('index.html')

def page_x(request):
    return render_to_response('game.html',dict({'me':'x', 'enemy':'o'}.items() + PUSHER.items()))

def page_o(request):
    return render_to_response('game.html',dict({'me':'o', 'enemy':'x'}.items() + PUSHER.items()))

def turn_x(request):
    p['turn_x'].trigger('turn_is_done', request.POST.get('cell', ''))
    return HttpResponse(request.POST.get('cell', ''))

def turn_o(request):
    p['turn_o'].trigger('turn_is_done', request.POST.get('cell', ''))
    return HttpResponse(request.POST.get('cell', ''))
