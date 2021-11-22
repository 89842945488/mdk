from django.http.response import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.urls.base import reverse_lazy  # в качестве главной
#  страницы мы бы хотели отобразить некоторый
# шаблон с именем index.html. Для этого, вначале
#  нам нужно импортировать встроенный в Django шаблонизатор.
from .utils import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, request
from django.views.generic.edit import CreateView
from women.forms import *
from women.models import Category, Women
from django.views.generic import ListView, DetailView

from django.core.paginator import Paginator
# Create your views here.

menu = [{'title': "О сайте", 'url_name': 'about'},
        {'title': "Добавить статью", 'url_name': 'add_page'},
        {'title': "Обратная связь", 'url_name': 'contact'},
        {'title': "Войти", 'url_name': 'login'}  # главное меню сайта
        ]


class WomenHome(DataMixin, ListView,):

    model = Women
    template_name = 'women/index.html'
    context_object_name = 'posts'
    extra_context = {'title': 'Главная страница'}

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Главная страница")
        context = dict(list(context.items()) + list(c_def.items()))
        return context
        # context['title'] = 'Добавление статьи'
        # context['menu'] = menu
        # context['cat_selected'] = 0

    def get_queryset(self):
        return Women.objects.filter(is_published=True)


class ShowPost(DataMixin, DetailView):
    model = Women
    template_name = 'women/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context['post'])
        return dict(list(context.items()) + list(c_def.items()))
# def show_post(request, post_slug):
#     post = get_object_or_404(Women, slug=post_slug)
#     context = {
#         'post': post,
#         'menu': menu,
#         'title': post.title,
#         # в функциях представления  мы можем передавать наше меню как параметр его как параметр
#         'cat_selected': post.cat_id,
#     }
#     return render(request, 'women/post.html', context=context)


def about(request):
    return render(request, 'women/about.html', {'menu': menu, 'title': 'О сайте'})


# def addpage(request):
#     if request.method == 'POST':
#         form = AddPostForm(request.POST, request.FILES)
#         if form.is_valid():
#             # print(form.cleaned_data)

#             form.save()
#             return redirect('home')

#     else:
#         form = AddPostForm()

#     return render(request, 'women/addpage.html', {'menu': menu, 'title': 'Добавление статьи', 'form': form})


class AddPage(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'women/addpage.html'
    success_url = reverse_lazy('home')
    login_url = reverse_lazy('home')
    raise_exception = True

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Добавление статьи")

        return dict(list(context.items()) + list(c_def.items()))


def contact(request):
    return HttpResponse("Обратная связь")  # заглушки на будущие страницы


def login(request):
    return HttpResponse("Авторизация")  # заглушки на будущие страницы


# def index(request):
#     posts = Women.objects.all()
#     context = {
#         'posts': posts,
#         'menu': menu,
#         'title': 'Главная страница',
#         'cat_selected': 0,
#     }
#     return render(request, 'women/index.html', context=context)


def about(request):

    contact_list = Women.objects.all()
    paginator = Paginator(contact_list, 3)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'women/about.html', {'page_obj': page_obj, 'menu': menu, 'title': 'О сайте'})


def categories(request, cat):
    return HttpResponse(f"<h1>Статьи по категориям</h1>{cat}</p>")


# def show_category(request, cat_id):
#     posts = Women.objects.filter(cat_id=cat_id)

#     if len(posts) == 0:
#         raise Http404()

#     context = {
#         'posts': posts,

#         'menu': menu,
#         'title': 'Рубрика',
#         'cat_selected': cat_id,
#     }

#     return render(request, 'women/index.html', context=context)

class WomenCategory(DataMixin, ListView):
    model = Women
    template_name = 'women/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        return Women.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Категория - ' + str(context['posts'][0].cat),
                                      cat_selected=context['posts'][0].cat_id)

        return dict(list(context.items()) + list(c_def.items()))


# def archive(request, year):
#     if(int(year) > 2020):
#         return redirect('/')

#     return HttpResponse(f"<h1>Архив по годам</h1>{year}</p>")
