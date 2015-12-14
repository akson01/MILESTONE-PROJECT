import os
from flask import Flask,session, render_template, url_for, request, redirect
import pandas as pd
from bokeh.embed import components
from bokeh.plotting import figure, output_file, show
import jinja2
app = Flask(__name__)

@app.route('/')
def main():
  return redirect('/index')

dataset=''
list=''

@app.route('/index',methods=['GET','POST'])
def index():
  
  if request.method=='POST':
     name=request.form['ticker']
     choice=request.form['features']
     global dataset
     global list
     list=choice
     dataset=name
     if name and choice:
        return redirect('/graph')
  return render_template('index.html')

@app.route('/graph')
def graph():
  global dataset
  global list

  url='https://www.quandl.com/api/v3/datasets/WIKI/'+dataset+'/data.csv'
  df=pd.read_csv(url,parse_dates=['Date'])
  output_file('graph.html')
  p=figure(title='Data from Quandle WIKI set',x_axis_label='Date',x_axis_type='datetime')  
  att=list
  p.line(df['Date'],df[att],legend=att,color="blue",line_width=1)
  comp=dataset

  template = jinja2.Template("""
  <!DOCTYPE html>
  <html>
    <head>
    <link rel="stylesheet" href="http://cdn.pydata.org/bokeh/release/bokeh-0.9.2.min.css" type="text/css" />
    <script type="text/javascript" src="http://cdn.pydata.org/bokeh/release/bokeh-0.9.2.min.js"></script>
    {{ script | safe }}
    </head>
    <body>
      <div class=page>
        <h1>Generated graph for {{ comp }} </h1>
        {{ div | safe }}
      </div>
    </body>
  </html> 
   """)
  script, div = components(p)

  return template.render(script=script, div=div,comp=comp)  

if __name__ == '__main__':
  app.run()
