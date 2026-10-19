from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.utils.text import slugify
from hitcount.views import HitCountMixin
from hitcount.templatetags.hitcount_tags import get_hit_count
from hitcount.utils import get_hitcount_model
from unicodedata import category

from .models import News, Category
from django.views.generic import ListView, DetailView, TemplateView, UpdateView, CreateView, DeleteView
from django.views.generic.edit import FormView
from .forms import ContactForm, CommentForm
from django.contrib.auth.mixins import LoginRequiredMixin
from news_project.custom_permissions import OnlyLoggedSuperUser


# Create your views here.

def news_list(request):
    news_list = News.objects.filter(status=News.Status.Published)
    context = {
        "news_list": news_list
    }
    return render(request, "news/news_list.html", context)
#
#
def news_detail(request, news):
    news = get_object_or_404(News, slug=news, status=News.Status.Published)
    context = {}
    # 1st view count method
    # news.view_count = news.view_count + 1
    # news.save()
    # 2nd method
    hit_count = get_hitcount_model().objects.get_for_object(news)
    hits = hit_count.hits
    hitcontext = context['hitcount'] = {'pk': hit_count.pk}
    hit_count_response = HitCountMixin.hit_count(request, hit_count)
    if hit_count_response.hit_counted:
        hits = hits + 1
        hitcontext['hit_counted'] = hit_count_response.hit_counted
        hitcontext['hit_message'] = hit_count_response.hit_message
        hitcontext['total_hits'] = hits




    comments = news.comments.filter(active=True)
    comments_count = comments.count()
    new_comment = None
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.news = news
            # assigning comment to user
            new_comment.user = request.user
            #saving comment to DB
            new_comment.save()
            comment_form = CommentForm()
    else:
        comment_form = CommentForm()
    context = {
        "news":news,
        'comments': comments,
        'comments_count': comments_count,
        'new_comment': new_comment,
        'comment_form': comment_form
    }

    return render(request, 'news/news_detail.html', context)

# class NewsListView(ListView):
#     model = News
#     template_name = "news/news_list.html"
#     context_object_name = "news_list"
#
#     def get_queryset(self):
#         return News.objects.filter(status=News.Status.Published)

class NewsDetailView(DetailView):
    model = News
    template_name = "news/news_detail.html"
    context_object_name = 'news'
    slug_field = 'slug'
    slug_url_kwarg = 'news'

    def get_queryset(self):
        return News.objects.filter(status=News.Status.Published)

class HomePageView(ListView):
    model = News
    template_name = "news/index.html"
    context_object_name = "news_list"

    def get_queryset(self):
        return News.objects.order_by('-published_time')[:3]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        context["world_news"] = News.objects.filter(category__name="World").order_by('-published_time')[:5]
        context["business_news"] = News.objects.filter(category__name="Business").order_by('-published_time')[:5]
        context["science_news"] = News.objects.filter(category__name="Science").order_by('-published_time')[:5]
        context["technology_news"] = News.objects.filter(category__name="Technology").order_by('-published_time')[:5]
        context["latest_news"] = News.objects.all().order_by('-published_time')[:5]
        return context


class ContactPageView(FormView):
        template_name = "news/contact.html"
        form_class = ContactForm

        def form_valid(self, form):
            form.save()
            return HttpResponse("<h2>Thanks for contacting us!</h2>")


# def contactPageView(request):
#     form = ContactForm(request.Post or None)
#     if request.method == "POST" and form.is_valid():
#         form.save()
#         return HttpResponse("<h2> Thanks for contacting us!</h2>")
#     context = {
#           "form": form
#       }
#
#     return render(request, "news/contact.html", context)

class AboutPageView(TemplateView):
    template_name = "news/about.html"


class WorldNewsView(ListView):
    model = News
    template_name = "news/world.html"
    context_object_name = "world_news"

    def get_queryset(self):
        news = self.model.published.all().filter(category__name="World")
        return news

class  BusinessNewsView(ListView):
    model = News
    template_name = "news/business.html"
    context_object_name = "business_news"

    def get_queryset(self):
        news = self.model.published.all().filter(category__name="Business")
        return news

class TechnologyNewsView(ListView):
    model = News
    template_name = "news/technology.html"
    context_object_name = "technology_news"

    def get_queryset(self):
        news = self.model.published.all().filter(category__name="Technology")
        return news

class ScienceNewsView(ListView):
    model = News
    template_name = "news/science.html"
    context_object_name = "science_news"

    def get_queryset(self):
        news= self.model.published.all().filter(category__name ="Science")
        return news



class CategoryNewsView(ListView):
    model = News
    template_name = "news/category_news.html"
    context_object_name = "news_list"

    def get_queryset(self):
        return News.objects.filter(
            category__name__iexact=self.kwargs['category_slug'],
            status=News.Status.Published
        ).order_by('-published_time')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_name'] = self.kwargs['category_slug']
        return context

class NewsUpdateView(OnlyLoggedSuperUser, UpdateView):
    model = News
    fields = ('title', 'body', 'image', 'category', 'status')
    template_name = 'crud/news_edit.html'
    slug_field = 'slug'
    slug_url_kwarg = 'news'

    def get_success_url(self):
        return self.object.get_absolute_url()

class NewsDeleteView(OnlyLoggedSuperUser, DeleteView):
    model = News
    template_name = 'crud/news_delete.html'
    slug_field = 'slug'
    slug_url_kwarg = 'news'
    success_url = reverse_lazy('home_page')

class NewsCreateView(OnlyLoggedSuperUser, CreateView):
    model = News
    template_name = 'crud/news_create.html'
    fields = ('title','title_uz','title_en','title_ru', 'slug', 'body','body_uz','body_en','body_ru', 'image', 'category', 'status')
    slug_field = 'slug'
    slug_url_kwarg = 'news'

    def get_success_url(self):
        return self.object.get_absolute_url()




@login_required
@user_passes_test(lambda u:u.is_superuser)
def admin_page_view(request):
    admin_users = User.objects.filter(is_superuser=True)
    context = {
        'admin_users': admin_users
    }
    return render(request, 'pages/admin_page.html', context)

class SearchResultsList(ListView):
    model = News
    template_name = 'news/search_result.html'
    context_object_name = 'all_news'

    def get_queryset(self):
        query = self.request.GET.get('q')
        return News.objects.filter(
            Q(title__icontains=query) | Q(body__icontains=query)
        )
