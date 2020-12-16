from django.urls import path
from .views import home,sell,sell_insert,buy,buy_insert,search,search_result

urlpatterns = [
    path('', home, name = 'home'),
    path('sell/', sell, name = 'sell'),
    path('sell_insert/',sell_insert, name='sell_insert'),
    path('buy/', buy, name='buy'),
    path('buy_insert/', buy_insert, name ='buy_insert'),
    path('search/',search, name='search'),
    path('search_result/',search_result,name='search_result'),
    

]
