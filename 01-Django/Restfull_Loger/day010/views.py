from django.shortcuts import render


def base(request):
    if request.method == 'GET':
        return render(request, 'base_index.html')