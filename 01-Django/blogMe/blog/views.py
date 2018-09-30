from django.shortcuts import render


def index(request):
    if request.method == 'GET':

        return render(request, 'index.html')


def base(request):
    if request.method == 'GET':

        return render(request, 'temp/base.html')


def article(request):

    return render(request, 'article.html')


def about(request):

    return render(request, 'about.html')


def mood(request):

    return render(request, 'mood.html')


def article_detail(request):

    return render(request, 'article_detail.html')


def board(request):

    return render(request, 'board.html')


def upload(request):
    """上传文件"""

    return render(request, 'article/upload.html')