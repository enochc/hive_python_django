from django.shortcuts import render
from django.http import HttpResponse

from django.views.decorators.csrf import csrf_exempt

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

