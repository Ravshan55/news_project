from django.urls import path
# from .views import news_list, news_detail
from .views import NewsListView, NewsDetailView, HomePageView, ContactPageView, AboutPageView, WorldNewsView, \
    BusinessNewsView, TechnologyNewsView, ScienceNewsView, CategoryNewsView

# urlpatterns = [
#     path('all/', news_list, name="all_news_list"),
#     path('<int:id>/', news_detail, name="news_detail_page")
# ]

urlpatterns = [
    path('', HomePageView.as_view(), name="home_page"),
    path('all/', NewsListView.as_view(), name="all_news_list"),
    path('contact/', ContactPageView.as_view(), name='contact_page'),
    path('about-us/', AboutPageView.as_view(), name='about_page'),
    path('category/<str:category_slug>/', CategoryNewsView.as_view(), name='category_news'),
    path('world/', WorldNewsView.as_view(), name="world_news_page"),
    path('business/', BusinessNewsView.as_view(), name="business_news_page"),
    path('technology/', TechnologyNewsView.as_view(), name="technology_news_page"),
    path('science/', ScienceNewsView.as_view(), name="science_news_page"),
    path('<slug:news>/', NewsDetailView.as_view(), name='news_detail_page')
]