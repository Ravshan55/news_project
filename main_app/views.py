

from django.http import HttpResponse
from unicodedata import category

from .models import News, Category
from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic.edit import FormView
from .forms import ContactForm


# Create your views here.

# def news_list(request):
#     news_list = News.objects.filter(status=News.Status.Published)
#     context = {
#         "news_list": news_list
#     }
#     return render(request, "news/news_list.html", context)
#
#
# def news_detail(request, news):
#     news = get_object_or_404(News, slug=news, status=News.Status.Published)
#     context = {
#         "news":news
#     }
#
#     return render(request, 'news/news_detail.html', context)

class NewsListView(ListView):
    model = News
    template_name = "news/news_list.html"
    context_object_name = "news_list"

    def get_queryset(self):
        return News.objects.filter(status=News.Status.Published)

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




