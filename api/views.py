from django.shortcuts import render,HttpResponse

# Create your views here.
def asset(request):
    print(request.body.decode('utf-8'))
    return HttpResponse('ok')