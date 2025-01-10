import pandas as pd
import os
from datetime import datetime
folder_path = (os.path.normpath(os.path.dirname(os.path.realpath(__file__)))+"/")
xls_path = folder_path+"xls/"
output_path = folder_path+"csv/"
file_list = [f for f in os.listdir(xls_path) if ".xls" in f]
print (file_list)

actual_table = ""
prefix = input("Ki vagy?: ")
if prefix:
    prefix+="_"
else:
    prefix=""
for file_name in file_list:
    df = pd.read_html(xls_path+file_name)
    for i,table in enumerate(df):
        try:
            if table.columns.values[1] == "Forgalom típusa":
                print("Meg van a tábla!")
                table.drop(table.columns[[0]], axis=1, inplace=True)
                table.columns = table.columns.str.replace('Tranzakció időpontja', 'Date')
                table.columns = table.columns.str.replace('Összeg', 'Amount')
                table.columns = table.columns.str.replace('Forgalom típusa', 'Category')
                table.columns = table.columns.str.replace('Ellenoldali név', 'Payee')
                table["Note"] =  table["Közlemény"].map(str) + " Bank ID: " + table["Banki tranzakció azonosító"].map(str) + " Ellenoldali számlaszám: " + table["Ellenoldali számlaszám"].map(str)+" Típus: "+table['Category'].map(str)
                table.drop(["Közlemény", "Banki tranzakció azonosító","Ellenoldali számlaszám"], axis=1, inplace=True)
                table["Date"] = pd.to_datetime(table["Date"],format='%Y.%m.%d. %H:%M:%S')
                table["Date"] = table["Date"].dt.strftime("%d/%m/%Y %H:%M:%S")
                csv_name = prefix+file_name.split('.')[0]+".csv"
                print("{0} fájl mentése...".format(csv_name))
                table.to_csv(output_path+csv_name,sep=';',encoding='utf-8-sig',index=False, na_rep=None)
        except Exception as e:
            print("Hiba: "+e)
            input("Nyomj entert a folytatáshoz")

input("Nyomj entert a folytatáshoz")
