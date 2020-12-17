from django.shortcuts import render
from django.views import generic
import datetime
import sqlite3



# Create your views here.
def home(request):
    return render(request,'index.html')

def sell(request):
    return render(request, 'sell.html')  
      

def sell_insert(request):

    
    if request.method == 'GET':
        for i in range(10):
            id = request.GET.get('id_'+str(i))
            quantity = request.GET.get('quantity_'+str(i))
            price = request.GET.get('price_'+str(i))
            c_name = request.GET.get('c_name_'+str(i))
            c_no = request.GET.get('c_no_'+str(i))

            #submitbutton = request.GET.get('submit')

            if id !='' and quantity !='' and price !='' and c_name !='' and c_no !='':
                con = sqlite3.connect('/home/clown/DB/Inventory.db')
                con.execute("PRAGMA foreign_keys=ON") 
                con.execute("INSERT INTO sell(item_id, quantity, unit_price, cust_name, cust_phone,date_time) VALUES(?,?,?,?,?,?)",(id,int(quantity),int(price),c_name,c_no,str(datetime.datetime.now())))
                con.commit()
                con.close()
                

            else:
                return render(request,'sell.html') 

        return render(request,'sell.html')          



def buy(request):
    return render(request,'buy.html')     

def buy_insert(request):
    if request.method == 'GET':
        for i in range(10):
            id = request.GET.get('id_'+str(i))
            s_id = request.GET.get('s_id_'+str(i))
            quantity = request.GET.get('quantity_'+str(i))
            price = request.GET.get('price_'+str(i))
    

        #submitbutton = request.GET.get('submit')

            if id !='' and s_id !='' and price !='' and quantity !='':
                con = sqlite3.connect('/home/clown/DB/Inventory.db')
                con.execute("PRAGMA foreign_keys=ON")
                con.execute("INSERT INTO bought(item_id, s_id, quantity, unit_price,date_time) VALUES(?,?,?,?,?)", (id,s_id,int(quantity),int(price),str(datetime.datetime.now())))
                con.commit()
                con.close() 
                

            else: 
                return render(request,'buy.html')

        return render(request,'buy.html')



def search(request):
    con = sqlite3.connect('/home/clown/DB/Inventory.db')
    obj = con.execute("SELECT * FROM item_details ORDER BY item_price")
    con.commit()
    item_list=[]
    for i in obj:
        item_list.append({
            'id':i[0],
            'name':i[1],
            'brand':i[2],
            'category':i[3],
            'color':i[4],
            'size':i[5],
            'quantity':i[6],
            'price':i[7]
        })

    return render(request,'search.html',context={'item':item_list})
    
    
    

def search_result(request):
    
    
    if request.method=='GET':
        sludge = request.GET.get('search_box')
        sludge = '%' + sludge + '%'

        submitbutton = request.GET.get('search_button')    

        if sludge is not None:
            con = sqlite3.connect('/home/clown/DB/Inventory.db')
            obj = con.execute("SELECT * FROM item_details WHERE item_id like ? OR item_name like ? OR brand like ? OR c_name like ? OR color like ? ORDER BY item_price",(sludge,sludge,sludge,sludge,sludge,))
            con.commit()

            item_list=[]
            for i in obj:
                item_list.append({
                    'id':i[0],
                    'name':i[1],
                    'brand':i[2],
                    'category':i[3],
                    'color':i[4],
                    'size':i[5],
                    'quantity':i[6],
                    'price':i[7]
                }) 

            return render(request,'search.html',context={'item':item_list})     



def detail(request):
    return render(request,'detail.html')            



def detail_result(request):
    if request.method=='GET':
        if request.GET.get('details')=='sold':
            con = sqlite3.connect('/home/clown/DB/Inventory.db')
            obj = con.execute("SELECT * FROM sell ORDER BY date_time DESC")
            con.commit()
            sold_list = []
            for i in obj:
                sold_list.append({
                    'id':i[0],
                    'item':i[1],
                    'quantity':i[2],
                    'price':i[3],
                    'c_name':i[4],
                    'c_no':i[5],
                    'date_time':i[6]
                })

            return render(request,'detail_result.html',context={'header':0,'sold':sold_list})    



        elif request.GET.get('details')=='bought':
            con = sqlite3.connect('/home/clown/DB/Inventory.db')
            obj = con.execute("SELECT * FROM bought ORDER BY date_time DESC")
            con.commit()
            bought_list = []
            for i in obj:
                bought_list.append({
                    'item':i[0],
                    'supplier':i[1],
                    'quantity':i[2],
                    'price':i[3],
                    'date_time':i[4]
                })

            return render(request,'detail_result.html',context={'header':1,'bought':bought_list})    




        elif request.GET.get('details')=='suppliers':     
            con = sqlite3.connect('/home/clown/DB/Inventory.db')
            obj = con.execute("SELECT * FROM supplier")
            con.commit()
            supplier_list=[]
            for i in obj:
                supplier_list.append({
                    'id':i[0],
                    'name':i[1],
                    'c_id':i[2],
                    'rating':i[3]
                }) 

            return render(request,'detail_result.html',context={'header':2,'supplier':supplier_list})


        elif request.GET.get('details')=='warehouse':
            con = sqlite3.connect('/home/clown/DB/Inventory.db')
            obj = con.execute("SELECT warehouse.w_id,warehouse.w_adress,warehouse.w_capacity,sum(stored.quantity) AS Occupied FROM warehouse,stored WHERE warehouse.w_id=stored.w_id GROUP BY stored.w_id")
            con.commit()
            warehouse_list=[]
            for i in obj:
                warehouse_list.append({
                'id':i[0],
                'adress':i[1],
                'capacity':i[2],
                'occupied':i[3]
            })   
            
            return render(request,'detail_result.html',context={'header':3,'storage':warehouse_list})



        elif request.GET.get('details')=='category':
            con = sqlite3.connect('/home/clown/DB/Inventory.db')
            obj = con.execute("SELECT * FROM category")
            con.commit()
            category_list = []
            for i in obj:
                category_list.append({
                'id':i[0],
                'name':i[1]
            })  

          
            return render(request,'detail_result.html',context={'header':4,'categories':category_list})    



        elif request.GET.get('details')=='product stored':
            con = sqlite3.connect('/home/clown/DB/Inventory.db')
            obj = con.execute("SELECT item_id,w_id FROM stored")
            con.commit()
            storage_list = []
            for i in obj:
                storage_list.append({
                'id':i[0],
                'stored':i[1]
            })

            return render(request,'detail_result.html', context={'header':5,'products':storage_list})   





def change(request):
    return render(request,'change.html')     

