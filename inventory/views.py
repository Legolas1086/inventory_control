from django.shortcuts import render
from django.views import generic
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
                con = sqlite3.connect('/home/clown/DB/Inventory')

                con.execute("INSERT INTO sell(item_id, quantity, unit_price, cust_name, cust_phone) VALUES(?,?,?,?,?)",(id,int(quantity),int(price),c_name,c_no))
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
                con = sqlite3.connect('/home/clown/DB/Inventory')
                con.execute("INSERT INTO bought(item_id, s_id, quantity, unit_price) VALUES(?,?,?,?)", (id,s_id,int(quantity),int(price)))
                con.commit()
                con.close() 
                

            else: 
                return render(request,'buy.html')

        return render(request,'buy.html')



def search(request):
    con = sqlite3.connect('/home/clown/DB/Inventory')
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
            con = sqlite3.connect('/home/clown/DB/Inventory')
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


                

