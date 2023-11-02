from faker import Faker
from datetime import datetime
import pandas as pd
import numpy as np
import random

#importing libraries
from faker import Faker
from datetime import datetime
import pandas as pd
import numpy as np
import random

#declaring fake variable
fake = Faker()

#Function declaration

#fake orders - except order_value

def make_orders(num):
    
    start_date = datetime.strptime('2022-09-01', '%Y-%m-%d').date()
    end_date = datetime.strptime('2022-12-31', '%Y-%m-%d').date()

    order_source=['Others','AnyKart.Com']
    shpmt_typ=['Prime','Standard']
    fake_orders=[]
    Ord_list=[]
    
    for x in range(num):
        Ord_ID='AKT_' + fake.numerify('########')
        
        while Ord_ID in Ord_list:
            Ord_ID='AKT_' + fake.numerify('########')
        
        fake_orders_dict = {'Order_ID':Ord_ID, 
             'Order_Date':fake.date_between_dates(date_start=start_date, date_end=end_date),
             'Order_Source':fake.random_element(elements=order_source),
             'Shipment_Type':fake.random_element(elements=shpmt_typ)
            } 
        
        Ord_list.append(Ord_ID)
        fake_orders.append(fake_orders_dict)
    
    df_ord=pd.DataFrame(fake_orders)
    
    return df_ord

#Make SKUs table
def make_SKU(num):
    
    Product_Category=['Food','Clothing and Apparel','Home Supplies']
    
    Fd_subcat=['Frozen','Bakery','Groceries','Meat']
    CA_subcat=["Men's Clothing","Women's Clothing","Kids"]
    HS_subcat=["Pet Supplies","Utensils","Accessories","Cleaning"]
    
    Fd_Manf=['Mestle','Nyson','Allogs']
    CA_Manf=['MK','CK','H&M']
    HS_Manf=['Turina','PawLuv','PetLove']
    
    fake_SKUs=[]
    
    SKU_list=[]
    for i in range(num):
        Bp=fake.random_int(min=10, max=499)
        PC=fake.random_element(elements=Product_Category)
        SKU='SKU_' + fake.numerify('####')
        
        while SKU in SKU_list:
            SKU='SKU_' + fake.numerify('####')
                
        fake_SKUs_dict={'SKU':SKU,
             'Product_Category':PC,
             'Product_Sub_Category':fake.random_element(elements=Fd_subcat) if PC=='Food' else (fake.random_element(elements=CA_subcat) if PC=='Clothing and Apparel' else fake.random_element(elements=HS_subcat)),
             'Product_Color':fake.color_name() if PC=='Clothing and Apparel' or PC=='Home Supplies' else None,
             'Product_Manufacturer':fake.random_element(elements=Fd_Manf) if PC=='Food' else (fake.random_element(elements=CA_Manf) if PC=='Clothing and Apparel' else fake.random_element(elements=HS_Manf)),
             'Product_Buying_Price':Bp,
             'Product_Selling_Price':fake.random_int(min=Bp+1, max=500)
            }
        
        SKU_list.append(SKU)
        fake_SKUs.append(fake_SKUs_dict)

    df_SKUs=pd.DataFrame(fake_SKUs)
    
    return df_SKUs

#Sub orders table
def make_suborders(num,df_ord,df_sku):
    
    if (num<len(df_ord)):
        raise ValueError("Sub_orders need to be higher than orders")
    else:
        unq_orders=df_ord['Order_ID'].unique().tolist()
        unq_skus=df_sku['SKU'].unique().tolist()
        status=['Processing','Canceled','Order Placed','Delivered','Return']
        fulfilment=['AnyKart','Third Party']
        DID_list=[]
        
        subord=[]
#         pd.DataFrame(columns=['SubOrder_ID','SKU','Order_ID','QTY','Status','SubOrder_Value','Order_Fulfilment','Delivery_ID'])
        
        for value in unq_orders:
            
            ff=fake.random_element(elements=fulfilment)
            if ff=='Third Party':
                DID=''
            else:
                DID=f"55_{'{:2d}'.format(fake.random_number(digits=8))}"
                while DID in DID_list:
                    DID=f"55_{'{:2d}'.format(fake.random_number(digits=8))}"
                DID_list.append(DID)
                    
            
            fake_suborders = {
             'SubOrder_ID':f"{value}_{'{:2d}'.format(fake.random_number(digits=2))}", 
             'SKU':fake.random_element(elements=unq_skus), 
             'Order_ID':value,
             'QTY':fake.random_int(min=1, max=10),
             'Status':fake.random_element(elements=status),
             'Order_Fulfilment':ff,
             'Delivery_ID':DID
            } 
            
            subord.append(fake_suborders)
        
#         global df_subord
        df_subord=pd.DataFrame(subord)
        
#         unq_suborders=subord['SubOrder_ID'].unique().tolist()
        
#         while len(df_subord) < num:
#             oid = np.random.choice(unq_orders)
        for value in unq_orders:
            
            if len(subord) >= num:
                break

            #random select a number i= between 1 and 4
            rnd_n1=fake.random_int(min=1, max=4)
            #if 1, move to next order_id
            if rnd_n1==1:
                pass
            #if not, random toss 0 or 1
            else:
                rnd_n2=fake.random_int(min=0, max=1)
                
                if rnd_n2==0:
                    #if 0, then pick the suborder_id for that order_id, generate a new sku for i records
#                         print(value)
                    unq_suborders=df_subord[df_subord['Order_ID']==value]['SubOrder_ID'].unique().tolist()
                    so_val=fake.random_element(elements=unq_suborders)
                    unq_so_skus=df_subord[df_subord['SubOrder_ID']==so_val]['SKU'].unique().tolist()
                    sub_ff=df_subord[df_subord['SubOrder_ID']==so_val]['Order_Fulfilment'].iloc[0]
                    
                    if sub_ff=='Third Party':
                        del_ID=''
                    else:
                        del_ID=df_subord[df_subord['SubOrder_ID']==so_val]['Delivery_ID'].iloc[0]
                    
                    sub_status=df_subord[df_subord['SubOrder_ID']==so_val]['Status'].iloc[0]

                    for sub_cnt in range(rnd_n1):
                        
                        if len(subord) >= num:
                            break
                        
                        #updated so sku list
                        unq_so_skus=df_subord[df_subord['SubOrder_ID']==so_val]['SKU'].unique().tolist()
                        
                        new_sku=fake.random_element(elements=unq_skus)

                        while new_sku in unq_so_skus:
                            new_sku=fake.random_element(elements=unq_skus)
                            
                        fake_suborders = {
                         'SubOrder_ID':so_val, 
                         'SKU':new_sku, 
                         'Order_ID':value,
                         'QTY':fake.random_int(min=1, max=10),
                         'Status':sub_status,
                         'Order_Fulfilment':sub_ff,
                         'Delivery_ID':del_ID
                        } 

                        subord.append(fake_suborders)
                        #create df and update unq_so_skus and check that list. This could be reason why there is duplication in soborder_ID sku
                        df_subord = pd.concat([df_subord, pd.DataFrame.from_records([fake_suborders])])
#                         df_subord.append(fake_suborders,ignore_index=True)
#                         df_subord=pd.DataFrame(subord)
                else:
                    #if 1, then create a new suborder_id, pick a sku
                    

                    for sub_cnt in range(rnd_n1):
                        unq_so_skus=df_subord[df_subord['Order_ID']==value]['SKU'].unique().tolist()
                        new_sku=fake.random_element(elements=unq_skus)
                        
                        if len(subord) >= num:
                            break
                        
                        #make sure that this sku doesn't exist for this order already
                        while new_sku in unq_so_skus:
                            new_sku=fake.random_element(elements=unq_skus)
                        
                        #make sure that this suborder doesn't already exist
                        unq_so_soid=df_subord[df_subord['Order_ID']==value]['SubOrder_ID'].unique().tolist()
                        new_so_id=f"{value}_{'{:2d}'.format(fake.random_number(digits=2))}"
                        
                        while new_so_id in unq_so_soid:
                            new_so_id=f"{value}_{'{:2d}'.format(fake.random_number(digits=2))}"
                        
                        #check if fulfilled by thirdparty
                        ff=fake.random_element(elements=fulfilment)
                        if ff=='Third Party':
                            DID=''
                        else:
                            DID=f"55_{'{:2d}'.format(fake.random_number(digits=8))}"
                            while DID in DID_list:
                                DID=f"55_{'{:2d}'.format(fake.random_number(digits=8))}"
                        DID_list.append(DID)
                        
                        fake_suborders = {
                         'SubOrder_ID':new_so_id, 
                         'SKU':new_sku, 
                         'Order_ID':value,
                         'QTY':fake.random_int(min=1, max=10),
                         'Status':fake.random_element(elements=status),
                         'Order_Fulfilment':ff,
                         'Delivery_ID':DID
                        } 

                        subord.append(fake_suborders)
#                         df_subord=pd.DataFrame(subord)
                        df_subord = pd.concat([df_subord, pd.DataFrame.from_records([fake_suborders])])
#                         df_subord.append(fake_suborders,ignore_index=True)

#                 df_subord=pd.DataFrame(subord)    
            #make sure that the order_id, suborder_id, sku combination doesn't already exist
            
#         df_subord=pd.DataFrame(subord)    
        return df_subord

#Coupons table
def make_coupons(num):
    
    st_start_date = datetime.strptime('2022-08-01', '%Y-%m-%d').date()
    st_end_date = datetime.strptime('2022-08-05', '%Y-%m-%d').date()

    ed_start_date = datetime.strptime('2023-01-01', '%Y-%m-%d').date()
    ed_end_date = datetime.strptime('2023-01-05', '%Y-%m-%d').date()
    

    
    fake_coupons=[]
    cpn_list=[]
    
    for i in range(num):
        
        PD=float(fake.pydecimal(left_digits=2, right_digits=2, min_value=5, max_value=10))
        MV=float(fake.random_int(min=200, max=499))
        cpn=fake.lexify(text='????').upper() +'_'+ str(round(PD))
        
        while cpn in cpn_list:
            cpn=fake.lexify(text='????').upper() +'_'+ str(round(PD))
        
        fake_coupons_dict = {'Coupon_Code':cpn, 
             'Percentage_Discount':PD,
             'Min_Order_Value':MV,
             'Max_Discount':fake.random_int(min=int(round(MV*0.05+(MV*PD)/100)), max=int(round(MV*0.1+(MV*PD)/100))),
             'Coupon_Start_Date':fake.date_between_dates(date_start=st_start_date, date_end=st_end_date),
             'Coupon_End_Date':fake.date_between_dates(date_start=ed_start_date, date_end=ed_end_date)
            }
        
        fake_coupons.append(fake_coupons_dict)
        cpn_list.append(cpn)
    
    df_coupons=pd.DataFrame(fake_coupons)
    

    return df_coupons

#Sales Table
def make_sales(df_subord,df_sku,df_coupons,df_ord):
    
    sales=[]
#     global x_sku
#     global x_cpn
    df_sales= pd.DataFrame(columns=['SubOrder_ID', 'SKU', 'Product_Buying_Price','Product_Selling_Price','Coupon_Code','Discount_Percentage','Delivery_Charge','Tax','SubOrder_Value'])
    for i in range(len(df_subord)):
        #print(i,"th record")
        x_subord=df_subord.iloc[i]
        sub_id=x_subord['SubOrder_ID']
        sku=x_subord['SKU']
        x_sku=df_sku[df_sku['SKU']==sku].iloc[0]
        unq_coupons=coupons['Coupon_Code'].unique().tolist()
        cpn=fake.random_element(elements=unq_coupons)
        x_cpn=df_coupons[df_coupons['Coupon_Code']==cpn].iloc[0]
        
        #check if coupon can be applied
        if (x_subord['QTY']*x_sku['Product_Selling_Price'])>=x_cpn['Min_Order_Value']:
            
            #check if max discount criteria is met
            if ((x_subord['QTY']*x_sku['Product_Selling_Price'].item()*x_cpn['Percentage_Discount'].item())/100)>x_cpn['Max_Discount'].item():
                sp=x_subord['QTY']*x_sku['Product_Selling_Price']-x_cpn['Max_Discount']
            else:
                sp=x_subord['QTY']*x_sku['Product_Selling_Price']-x_subord['QTY']*x_sku['Product_Selling_Price']*x_cpn['Percentage_Discount']/100
            
        
        #check if delivery charge is 0
#         global ord_id
        
        ord_id=x_subord['Order_ID']
        x_ord=df_ord[df_ord['Order_ID']==ord_id]
        
        if str(x_ord['Shipment_Type'])=='Prime':
            dlv_chrg=0
        else:
            dlv_chrg=float(fake.pydecimal(left_digits=2, right_digits=2, min_value=2, max_value=10))
        
        #Tax
        psp=x_sku['Product_Selling_Price'].max()
        Tax=round(sp*0.02,2)
#         Tax=float(fake.pydecimal(left_digits=2, right_digits=2, min_value=3, max_value=5))
        
        #sub_value=x['SKU']
        fake_sales = {
         'SubOrder_ID':sub_id, 
         'SKU':sku, 
         'Product_Buying_Price':x_sku['Product_Buying_Price'],
         'Product_Selling_Price':x_sku['Product_Selling_Price'],
         'Coupon_Code':cpn,
         'Discount_Percentage':x_cpn['Percentage_Discount'],
         'Delivery_Charge':dlv_chrg,
         'Tax':Tax,
         'SubOrder_Value':sp+Tax+dlv_chrg
                        }
        sales.append(fake_sales)
        
        df_sales = pd.concat([df_sales, pd.DataFrame.from_records([fake_sales])])
#         df_sales=pd.DataFrame(sales)
    
    return df_sales

#Delivery table
def make_delivery(df_subord):
    
    delivery=[]
    unq_delivery=df_subord[df_subord['Delivery_ID']!='']['Delivery_ID'].unique().tolist()
    print(len(df_subord))
    print(len(unq_delivery))
    unq_proc_st=['In Transit','Packed','Out for Delivery','Shipped']
    
    for value in unq_delivery:
        so_val=df_subord[df_subord['Delivery_ID']==value]['SubOrder_ID'].iloc[0]
        status_val=df_subord[df_subord['Delivery_ID']==value]['Status'].iloc[0]
        
        base_status=['Canceled','Delivered','Return','Order Placed']
        
        if status_val in base_status:
            del_status=status_val
        else:
            del_status=fake.random_element(elements=unq_proc_st)
            
        fake_delivery={
            'Delivery_ID':value,
#             'SubOrder_ID':so_val,
            'Warehouse_ID':f"WH_{'{:2d}'.format(fake.random_number(digits=4))}",
            'Status':del_status
        }
        delivery.append(fake_delivery)
        
    df_delivery=pd.DataFrame(delivery)
    
    return df_delivery

#Make data
#Orders
orders_df = make_orders(num=900)

#SKUs
SKU_df=make_SKU(num=50)

#Suborders
suborders_df=make_suborders(orders_df,SKU_df,num=1000)

#Coupons
coupons=make_coupons(num=10)

#Sales
sales_df=make_sales(suborders_df,SKU_df,coupons,orders_df)

#Delivery
delivery_df=make_delivery(suborders_df)

#Test
#pd.merge(suborders_df,SKU_df,on=['SKU']).groupby('Order_ID').sum('Product_Selling_Price').to_csv("downloads//order_level.csv")

#update suborders for sales values
updated_suborders=pd.merge(suborders_df,sales_df,on=['SubOrder_ID','SKU'])[['SubOrder_ID','SKU','Order_ID','QTY','Status','SubOrder_Value','Order_Fulfilment','Delivery_ID']]

#update orders with order value
updated_orders=pd.merge(orders_df,pd.merge(orders_df,updated_suborders,on='Order_ID').groupby('Order_ID').sum('SubOrder_Value'),on='Order_ID').rename(columns={"SubOrder_Value":"Order_value"})[['Order_ID','Order_Date','Order_Source','Shipment_Type','Order_value']]

#Export DFs to CSV files
updated_suborders.to_csv("suborders.csv",index=False)
updated_orders.to_csv("orders.csv",index=False)
sales_df.to_csv("sales.csv",index=False)
SKU_df.to_csv("SKUs.csv",index=False)
delivery_df.to_csv("delivery.csv",index=False)
coupons.to_csv("coupons.csv",index=False)