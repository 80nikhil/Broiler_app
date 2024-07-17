from django.urls import path
from . views import CorporateAliasView, RateView,StateAliasView,RegionAliasView,LoginView,Logout,Get_Rate_List

urlpatterns = [
    path('',LoginView.as_view(),name='login'),
    path('add-rate', RateView.as_view(),name='add-rate'),
    path('add-corporate-alias',CorporateAliasView.as_view(),name='add-corporate'),
    path('add-state-alias',StateAliasView.as_view(),name='add-state-alias'),
    path('region-alias',RegionAliasView.as_view(),name='region-alias'),
    path('get-rate-list',Get_Rate_List.as_view(),name='get-rate-list'),
    path('logout',Logout.as_view(),name='logout'),
]
