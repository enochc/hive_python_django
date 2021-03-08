from django.shortcuts import render
from django.http import HttpResponse

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import DHive

# Create your views here.
print("RUN HIVE <<<<")
h = DHive("mop")


def index(request):
    return render(request, 'hive/index.html', {'hive': h})


@csrf_exempt
def save(request, name, value):
    t = request.POST['type']
    response = "You're saving me %s"
    h.save(name, value, t)
    return HttpResponse(response % name+value+t)


@csrf_exempt
def up(request):
    response = "Going up"
    h.save("moveup", "true", "bool")
    return HttpResponse(response)


@csrf_exempt
def get(request):
    # data = {
    #     'pt': 0,
    #     'turn': 1,
    #     'speed': 0,
    #     'name': "REST"
    # }
    data = h.properties()
    return JsonResponse(data)


@csrf_exempt
def down(request):
    response = "Going Down"
    h.save("movedown", "true", "bool")
    return HttpResponse(response)

@csrf_exempt
def stop(request):
    response = "Stopping"
    h.save("moveup", "false", "bool")
    h.save("movedown", "false", "bool")
    return HttpResponse(response)

@csrf_exempt
def send(request, name):
    response = "You're sending me %s"
    msg = request.POST['msg']
    h.send_to_peer(name, msg)
    return HttpResponse(response % name+msg)
