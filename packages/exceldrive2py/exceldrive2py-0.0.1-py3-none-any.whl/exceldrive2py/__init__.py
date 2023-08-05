# -*- coding: utf-8 -*-
"""
Created on Thu Oct  1 12:13:15 2020

@author: Afsar
"""

import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint
import matplotlib.pyplot as plt
import pandas as pd
def load_data(filename,json_path):
    scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]

    creds = ServiceAccountCredentials.from_json_keyfile_name(json_path, scope)

    client = gspread.authorize(creds)
    sheet = client.open(filename).sheet1
    data = sheet.get_all_records()  
    dataframe = pd.DataFrame(sheet.get_all_records())
    print(dataframe.head())
    return dataframe
    
def plot_data(df,x,y):
    plt.plot(df[x],df[y],'bo')
    plt.xlabel(x)
    plt.ylabel(y)
    plt.title("plotting")
    plt.legend()
    plt.show()
    








