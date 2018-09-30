from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from rest_framework.response import Response

from rango.forms import PageForm, CategoryForm
from rango.models import Category, Page


def base_bootstrap(request):
    """首页, 基础模板"""
    if request.method == "GET":
        return render(request, 'rango/base_bootstrap.html')


def index(request):
    """rango首页"""
    if request.method == 'GET':
        category_list = Category.objects.order_by('-likes')[:5]
        page_list = Page.objects.order_by('-views')[:5]
        context_dict = {'categories': category_list, 'pages': page_list}

        return render(request, 'rango/index.html', context_dict)


def about(request):
    """about页面"""
    if request.method == 'GET':
        return render(request, 'rango/about.html')


def add_category(request):
    """增加分类"""
    form = CategoryForm()
    if request.method == 'GET':
        return render(request, 'rango/add_category.html', {'form': form})
    elif request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save(commit=True)  # 默认是 True
            return HttpResponseRedirect(reverse('rango:index'))


    
def show_category(request, category_name_slug):
    """展示所有分类"""
    if request.method == 'GET':
        slug = category_name_slug
        category = Category.objects.filter(slug=slug).first()
        category.likes += 1
        category.save()
        pages = Page.objects.filter(category=category)
        context_dict = {
            'category':category,
            'pages': pages,
            'query': slug,
            'result_list': None,
        }
        return render(request, 'rango/category.html', context_dict)


def add_page(request, category_name_slug):
    form = PageForm()   # page 模型  forms.Models
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None

    if request.method == 'GET':
        context_dict = {'form': form, 'category': category}
        return render(request, 'rango/add_page.html', context_dict)
    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            if category:
                page = form.save(commit=False)
                page.category = category    # 后台自动添加分类和 views
                page.views = 0
                page.save()
                return HttpResponseRedirect(reverse('rango:all_pages'))
        else:  # 表单提交有错误, 返回表单, 让用户重新填写提交
            context_dict = {'form': form, 'category': category}
            return render(request, 'rango/add_page.html', context_dict)


def goto(request):
    """查看页面内容"""
    page_id = None
    if request.method == 'GET':
        if 'page_id' in request.GET:
            page_id = request.GET['page_id']
    if page_id:
        try:
            page = Page.objects.get(id=page_id)
            page.views += 1
            page.save()
            return redirect(page.url)
        except:
            return HttpResponse('没有找到id={0}的页面'.format(page_id))
    return redirect(reverse('rango:index'))


def all_categories(request):
    """所有的分类"""
    if request.method == 'GET':
        page_num = request.GET.get('page_num', 1)
        categories = Category.objects.all()
        num = len(categories)
        paginator = Paginator(categories, 5)
        category_list = paginator.page(int(page_num))
        context_dict = {'pages': category_list, 'num': num}
        return render(request, 'rango/all_categories.html', context_dict)


def all_pages(request):
    """所有的页面"""
    if request.method == 'GET':
        page_num = request.GET.get('page_num', 1)
        pages = Page.objects.all()
        num = len(pages)
        paginator = Paginator(pages, 5)
        page_list = paginator.page(int(page_num))
        context_dict = {'pages': page_list, 'num':num}
        return render(request, 'rango/all_pages.html', context_dict)



def post_profile(request):
    """上传资料页面"""
    if request.method == 'GET':
        return render(request, 'rango/profile.html')

def list_profile(request):
    """展示资料页面"""
    if request.method == 'GET':
        return render(request, 'rango/list_profiles.html')


""" API """

from rest_framework import mixins, viewsets, status

from utils.serializer import CategorySerializer


class api_all_category(mixins.ListModelMixin,
                       mixins.CreateModelMixin,
                       mixins.RetrieveModelMixin,
                       viewsets.GenericViewSet):

    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        # data.get('slug')
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    # def



