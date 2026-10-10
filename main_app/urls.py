from django.urls import path
from django.views import View

#from .views import news_list, news_detail
from .views import HomePageView, ContactPageView, AboutPageView, WorldNewsView, \
    BusinessNewsView, TechnologyNewsView, ScienceNewsView, CategoryNewsView, NewsUpdateView, NewsDeleteView, \
    NewsCreateView, admin_page_view, news_detail, news_list, SearchResultsList

# urlpatterns = [
#     path('all/', news_list, name="all_news_list"),
#     path('<int:id>/', news_detail, name="news_detail_page")
# ]
urlpatterns = [
    path('', HomePageView.as_view(), name="home_page"),
    path('all/', news_list, name="all_news_list"),
    path('contact/', ContactPageView.as_view(), name='contact_page'),
    path('about-us/', AboutPageView.as_view(), name='about_page'),
    path('create/', NewsCreateView.as_view(), name="news_create"),
    path('admin_page/', admin_page_view, name='admin_page'),
    path('searchresult/', SearchResultsList.as_view(), name='search_result'),
    path('category/<str:category_slug>/', CategoryNewsView.as_view(), name='category_news'),
    path('world/', WorldNewsView.as_view(), name="world_news_page"),
    path('business/', BusinessNewsView.as_view(), name="business_news_page"),
    path('technology/', TechnologyNewsView.as_view(), name="technology_news_page"),
    path('science/', ScienceNewsView.as_view(), name="science_news_page"),
    path('<slug:news>/edit/', NewsUpdateView.as_view(), name="news_update"),
    path('<slug:news>/delete/', NewsDeleteView.as_view(), name="news_delete"),
    path('<slug:news>/', news_detail, name='news_detail_page'),
]

