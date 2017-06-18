import requests
import json
from pandas import *
import pandas as pd
from datetime import datetime, timedelta
import numpy as np
from bokeh.layouts import gridplot
from bokeh.plotting import figure, show, output_file, output_notebook
from bokeh.layouts import row
from flask import Flask, render_template, request, redirect, url_for
import cgi
import os
from bokeh import embed

def stock_price_basic():
    ts1 = figure(plot_width=500, plot_height=400)
    ts1.line([1,2,3,4], [-1,-2,4,5])
    return ts1

def stock_price():
    #ticker = request.form['ticker'].upper()
    ticker = 'GOOG'
    end_date = datetime.now().strftime("%Y%m%d")
    start_date = (datetime.now() - timedelta(days=30)).strftime("%Y%m%d")
    search_url = 'https://www.quandl.com/api/v3/datatables/WIKI/PRICES.json?' + 'date.gte=' + str(start_date) + '&date.lt=' + str(end_date) + '&ticker=' + ticker +'&api_key=WSUJv2tGoh2Wb_2_saYW'
    search_r = requests.get(search_url)
    search_data = search_r.json()
    interested_list = search_data['datatable']['data']
    df = DataFrame(interested_list)
    data_cols = [l['name'] for l in search_data['datatable']['columns']]   
    df.columns= [x.encode('UTF8') for x in data_cols]    
    #output_file("stock_price1.html")
#    ts1 = figure(plot_width=500, plot_height=400, x_axis_type='datetime')
    ts1 = figure(plot_width=500, plot_height=400)
    x_vals = np.array(df['date'],dtype=np.datetime64)
    #ts1.line(x_vals, df['close'])
    ts1.line([1,2,3,4], [-1,-2,4,5])
    #output_notebook()
    #show(ts1)
    return ts1
    #return show(ts1)
    #stock_price('GOOG')
    # print date_list
        
app = Flask(__name__)

#selector = {}

@app.route('/')
def main():
  return redirect('/index')

@app.route('/index', methods=['GET','POST'])
def index():
  #print 'rendering index.html'
  return render_template('index2.html')
    
@app.route('/output',methods=['GET','POST'])
def plot_page():
    plot = stock_price_basic()
    print 'output'
    script, div = embed.components(plot)
    return render_template('output.html', script=script, div=div)
#    return render_template('index3.html')


if __name__ == '__main__':
    #stock_price()
    port = int(os.environ.get("PORT", 33507))
    app.run(host='0.0.0.0', port=port)
