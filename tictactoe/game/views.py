from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from cent.core import Client
from time import time
import hmac


CENT = {
    'PROJECT_ID': '57a9577a3a414779bf05a6b079b1cf7a',
    'SECRET': '08cea16723b04fcf8b2795798f964ed3'
}

def get_client_token(user, timestamp):
    """
    Create token to validate information provided by new connection.
    """
    sign = hmac.new(CENT['SECRET'])
    sign.update(CENT['PROJECT_ID'])
    sign.update(user)
    sign.update(timestamp)
    token = sign.hexdigest()
    print 'TOKEN = ' + token
    return token


client = Client("http://localhost:8000/api", CENT['PROJECT_ID'], CENT['SECRET'])


def select_player(request):
    return render_to_response('index.html')


def page_x(request):
    timestamp = str(int(time()))
    return render_to_response('game.html', dict({
        'me': 'x',
        'enemy': 'o',
        'timestamp': timestamp,
        'token': get_client_token('x', timestamp)
    }.items() + CENT.items()))


def page_o(request):
    timestamp = str(int(time()))
    return render_to_response('game.html', dict({
        'me': 'o',
        'enemy': 'x',
        'timestamp': timestamp,
        'token': get_client_token('o', timestamp)
    }.items() + CENT.items()))


def turn_x(request):
    client.add("publish", {
            "channel": "turn_x",
            "data": request.POST.get('cell', '')
    })
    result, error = client.send()
    return HttpResponse(request.POST.get('cell', ''))


def turn_o(request):
    client.add("publish", {
            "channel": "turn_o",
            "data": request.POST.get('cell', '')
    })
    result, error = client.send()
    return HttpResponse(request.POST.get('cell', ''))
