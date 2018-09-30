from django.shortcuts import render


def register(request):

    if request.method == 'GET':

        return render(request, 'user/register.html')
    if request.method == 'POST':

        pass


def login(request):

    return render(request, 'user/login.html')
