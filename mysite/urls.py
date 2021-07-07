import sys
sys.path.append("..")

from django.contrib import admin
from django.urls import include, path
from django.views.decorators.csrf import csrf_exempt

from graphene_django.views import GraphQLView

from polls.schema import schema

urlpatterns = [
    path('polls/', include('polls.urls')),
    path('admin/', admin.site.urls),
    path("graphql", csrf_exempt(GraphQLView.as_view(graphiql=True, schema=schema))),
]