from django.shortcuts import render
from django.views import generic
import datetime
import sqlite3
from sqlite3 import Error



# Create your views here.
def home(request):
    return render(request,'index.html',context={'error':0})

def sell(request):
    return render(request, 'sell.html',context={'error':0})  
      

def sell_insert(request):
    id_list = []
    foreign_list = []
    #i_list = []
    
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
                try:
                    con.execute("INSERT INTO sell(item_id, quantity, unit_price, cust_name, cust_phone,date_time) VALUES(?,?,?,?,?,?)",(id,int(quantity),float(price),c_name,c_no,str(datetime.datetime.now())))
                    con.commit()
                    con.close()
                except Error as e:
                    foreign_list.append(id)

                
                
            elif id=='':
                break
                #return render(request,'sell.html',context={'error':0})

            elif id!='' and (quantity=='' or price=='' or c_name=='' or c_no==''):
                id_list.append(id)
                #return render(request,'sell.html',context={'error':1,'i':i+1,'id':id}) 
    
        if len(id_list)==0 and len(foreign_list)==0:
            return render(request,'sell.html',context={'error':0})    

        elif len(id_list)!=0 and len(foreign_list)==0:
            return render(request,'sell.html',context={'error':1,'ids':id_list})      

        elif len(id_list)==0 and len(foreign_list)!=0:
            return render(request,'sell.html',context={'error':2,'foreigns':foreign_list})        

        else:
            return render(request,'sell.html',context={'error':3,'ids':id_list,'foreigns':foreign_list})    



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
                con.execute("INSERT INTO bought(item_id, s_id, quantity, unit_price,date_time) VALUES(?,?,?,?,?)", (id,s_id,int(quantity),float(price),str(datetime.datetime.now())))
                con.commit()
                con.close() 
                

            elif id=='':
                return render(request,'buy.html',context={'error':0})


            elif id!='' and (s_id=='' or price=='' or quantity==''): 
                
                return render(request,'buy.html',context={'error':1,'i':i+1,'id':id})

              

        return render(request,'buy.html',context={'error':0})



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
    con.close()    

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
            con.close()
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
            
            coon.close()
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
            
            con.close()
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
                    'rating':i[2]
                }) 
            
            con.close()
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
            
            con.close()
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

            con.close()
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
            
            con.close()
            return render(request,'detail_result.html', context={'header':5,'products':storage_list})   





def change(request):
    return render(request,'change.html')   

def change_result(request):
    if request.method=="GET":
        choice = request.GET.get("change")
        submitbutton = request.GET.get('submit_button')
        print(change)

        if choice=='add':
            return render(request,'add.html',context={'error1':0,'error2':0,'error3':0,'error4':0})

        elif choice=='update':
            return render(request,'update.html')  

        else:
            return render(request,'change.html')            


def add_item(request):
    if request.method=='GET':
        id = request.GET.get('id')
        name = request.GET.get('name')
        brand = request.GET.get('brand')
        c_id = request.GET.get('c_id')
        size = request.GET.get('size')
        color = request.GET.get('color')
        price = request.GET.get('price')
        w_id = request.GET.get('w_id')
        quantity = request.GET.get('quantity')

        if id!='' and name!='' and brand!='' and c_id!='' and price!='' and w_id!='' and quantity!='':
            con = sqlite3.connect('/home/clown/DB/Inventory.db')
            con.execute("PRAGMA foreign_keys=ON") 
            try:
                con.execute("INSERT INTO item VALUES(?,?,?,?,?,?,?)",(id,name,brand,c_id,size,color,float(price)))    
                

            except Error as e:
                return render  (request,'add.html',context={'error':5}) 

            try:
                con.execute("INSERT INTO stored VALUES(?,?,?)",(id,w_id,int(quantity))) 
                con.commit() 

            except Error as e:
                return render(request,'add.html',context={'error':6})      


            return render(request,'add.html',context={'error':0})

        elif id!='' and (name=='' or brand=='' or c_id=='' or price=='' or w_id=='' or quantity==''):
            return render(request,'add.html',context={'error':1})

        else:
            return render(request,'add.html',context={'error':0})    



def add_supplier(request):
    if request.method=='GET':
        id = request.GET.get('id')
        name = request.GET.get('name')
        rating = request.GET.get('rating')
  
        if id!='' and name!='' and rating!='':
            con = sqlite3.connect('/home/clown/DB/Inventory.db')
            con.execute("PRAGMA foreign_keys=ON") 
            con.execute("INSERT INTO supplier VALUES(?,?,?)",(id,name,float(rating)))
            con.commit()
            con.close()
            return render(request,'add.html',context={'error':0})

        elif id!='' and (name=='' or rating==''):
            return render(request,'add.html',context={'error':2})    

        else:
            return render(request,'add.html',context={'error':0})



def add_category(request):
    if request.method=='GET':
        id = request.GET.get('id')
        name = request.GET.get('name')
        
  
        if id!='' and name!='':
            con = sqlite3.connect('/home/clown/DB/Inventory.db')
            con.execute("PRAGMA foreign_keys=ON") 
            con.execute("INSERT INTO category VALUES(?,?)",(id,name))
            con.commit()
            con.close()
            return render(request,'add.html',context={'error':0})

        elif id!='' and name=='':
            return render(request,'add.html',context={'error':3})  

        else:
            return render(request,'add.html',context={'error':0})

def add_warehouse(request):
    if request.method=='GET':
        id = request.GET.get('id')
        adress = request.GET.get('adress')
        capacity = request.GET.get('capacity')
  
        if id!='' and adress!='' and capacity!='':
            con = sqlite3.connect('/home/clown/DB/Inventory.db')
            con.execute("PRAGMA foreign_keys=ON") 
            con.execute("INSERT INTO warehouse VALUES(?,?,?)",(id,adress,int(capacity)))
            con.commit()
            con.close()
            return render(request,'add.html',context={'error':0})

        elif id!='' and (adress=='' or capacity==''):
            return render(request,'add.html',context={'error':4})    

        else:
            return render(request,'add.html',context={'error':0})


def update_price(request):
    if request.method=='GET':
        id = request.GET.get('id')
        price = request.GET.get('price')

        if id!='' and price!='':
            con = sqlite3.connect('/home/clown/DB/Inventory.db')
            con.execute("PRAGMA foreign_keys=ON")
            ids = con.execute("SELECT item_id FROM item") 
            id_list = []
            for i in ids:
                id_list.append(i[0])

            temp = 0    
            for i in range(len(id_list)):
                if id_list[i]==id:
                    temp = 0
                    break
                else:
                    temp = 1
            
            if temp==1:
                return render(request,'update.html',context={'error':4})

            con.execute("UPDATE item SET item_price=? WHERE item_id=?",(float(price),id))
            con.commit()
            con.close()
            return render(request,'update.html',context={'error':0})

        elif id!='' and price=='':
            return render(request,'update.html',context={'error':1})

        else:
            return render(request,'update.html',context={'error':0})


def update_rating(request):
    if request.method=='GET':
        id = request.GET.get('id')
        rating = request.GET.get('rating')

        if id!='' and rating=='':
            return render(request,'update.html',context={'error':2})        


        elif int(rating)<0 or int(rating)>5:
            return render(request,'update.html',context={'error':3})

        elif id!='' and rating!='':
            con = sqlite3.connect('/home/clown/DB/Inventory.db')
            con.execute("PRAGMA foreign_keys=ON")
            ids = con.execute("SELECT item_id FROM item") 
            id_list = []
            for i in ids:
                id_list.append(i[0])

            temp = 0    
            for i in range(len(id_list)):
                if id_list[i]==id:
                    temp = 0
                    break
                else:
                    temp = 1
            
            if temp==1:
                return render(request,'update.html',context={'error':5})
                 
            con.execute("UPDATE supplier SET rating=? WHERE s_id=?",(float(rating),id))
            con.commit()
            con.close()
            return render(request,'update.html',context={'error':0})

       
        else:
            return render(request,'update.html',context={'error':0})

    

                        




