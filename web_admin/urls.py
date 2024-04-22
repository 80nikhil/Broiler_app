from django.urls import path
from . views import CorporateAliasView, RateView,StateAliasView,RegionAliasView

urlpatterns = [
    path('add-rate', RateView.as_view(),name='add-rate'),
    path('add-corporate-alias',CorporateAliasView.as_view(),name='add-corporate'),
    path('add-state-alias',StateAliasView.as_view(),name='add-state-alias'),
    path('region-alias',RegionAliasView.as_view(),name='region_alias'),
]
