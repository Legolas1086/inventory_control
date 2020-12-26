from django.urls import path
from .views import home,sell,sell_insert,buy,buy_insert,search,search_result,detail,change,detail_result,change_result,add_item,add_category,add_supplier,add_warehouse
from .views import update_price,update_rating,login

urlpatterns = [
    path('',login,name='login'),
    path('home/', home, name = 'home'),
    path('sell/', sell, name = 'sell'),
    path('sell_insert/',sell_insert, name='sell_insert'),
    path('buy/', buy, name='buy'),
    path('buy_insert/', buy_insert, name ='buy_insert'),
    path('search/',search, name='search'),
    path('search_result/',search_result,name='search_result'),
    path('change/',change,name='change'),
    path('detail/',detail,name='detail'),
    path('detail_result/',detail_result,name='detail_result'),
    path('change_result/',change_result,name='change_result'),
    path('add_item/',add_item,name='add_item'),
    path('add_supplier/',add_supplier,name='add_supplier'),
    path('add_category/',add_category,name='add_category'),
    path('add_warehouse/',add_warehouse,name='add_warehouse'),
    path('update_price/',update_price,name='update_price'),
    path('update_rating/',update_rating,name='update_rating'),
    

]
