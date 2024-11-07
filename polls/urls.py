from django.urls import path
# from django.views.decorators.csrf import csrf_exempt

# from graphene_django.views import GraphQLView
from . import views
# from .schema import schema


app_name = 'polls'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:question_id>/', views.detail, name='detail'),
    path('<int:question_id>/results/', views.results, name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
    # path("graphql", csrf_exempt(GraphQLView.as_view(graphiql=True, schema=schema))),
]