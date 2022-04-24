from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponse
from django.shortcuts import redirect
from django.views.generic import *
from .models import Post,Category
from.filters import PostFilter
from .forms import PostForm, UserForm



class IndexView(View):
    def get(self, request):
        return HttpResponse('Hello!')


class PostsList(LoginRequiredMixin, ListView):
    model = Post
    ordering = '-time_in'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 4  # поставим постраничный вывод в один элемент


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        context['is_not_author'] = not self.request.user.groups.filter(name='authors').exists()
        context['categories'] = Category.objects.all()
        return context


# дженерик для получения деталей о товаре
class PostDetailView(LoginRequiredMixin,DetailView):
    template_name = 'post_detail.html'
    queryset = Post.objects.all()


# дженерик для создания объекта. Надо указать только имя шаблона и класс формы, который мы написали в прошлом юните. Остальное он сделает за вас
class PostCreateView(PermissionRequiredMixin, LoginRequiredMixin,CreateView):
    permission_required = ('news.add_post','news.change_post')
    template_name = 'post_create.html'
    form_class = PostForm



class PostsListSearch(LoginRequiredMixin,ListView):
    model = Post
    ordering = '-time_in'
    template_name = 'posts_search.html'
    context_object_name = 'posts'
    paginate_by = 2  # поставим постраничный вывод в один элемент

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET,queryset=self.get_queryset())  # вписываем наш фильтр в контекст
        return context


class PostUpdateView(PermissionRequiredMixin,LoginRequiredMixin,UpdateView):
    permission_required = ('news.add_post', 'news.change_post')
    template_name = 'post_create.html'
    form_class = PostForm

    # метод get_object мы используем вместо queryset, чтобы получить информацию об объекте, который мы собираемся редактировать
    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)





# дженерик для удаления товара
class PostDeleteView(LoginRequiredMixin,DeleteView):
    template_name = 'post_delete.html'
    queryset = Post.objects.all()
    success_url = '/news/'


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'profile_update.html'
    form_class = UserForm
    success_url = '/news/'

    # метод get_object мы используем вместо queryset, чтобы получить информацию об объекте, который мы собираемся редактировать
    def get_object(self, **kwargs):
        return self.request.user


class CategoryView (DetailView):
    model = Category
    template_name = 'categories_posts.html'

    # метод get_object мы используем вместо queryset, чтобы получить информацию об объекте, который мы собираемся редактировать
    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Category.objects.get(pk=id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        id = self.kwargs.get('pk')
        cat = Category.objects.get(pk=id)
        context['posts'] = Post.objects.filter(category=cat)
        return context

class SubscribeForm(View):
    def post(self,request, pk):
        category = Category.objects.get(pk=pk)
        category.addsubscriber(request.user)
        return redirect ('/news/')


