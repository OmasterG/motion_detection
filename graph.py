from script1 import df
from bokeh.plotting import figure,show,output_file
from bokeh.models import ColumnDataSource,HoverTool

df["Start_string"]=df["START"].dt.strftime("%Y-%m-%d %H:%M:%S")
df["End_string"]=df["END"].dt.strftime("%Y-%m-%d %H:%M:%S")

cds=ColumnDataSource(df)

p= figure(title="Motion Graph", height=200,width=500,x_axis_type="datetime")
p.yaxis.minor_tick_line_color=None
p.ygrid[0].ticker.desired_num_ticks=1
output_file("Graph.html")

hover=HoverTool(tooltips=[("Start","@Start_string"),("END","@End_string")])
p.add_tools(hover)
p.quad(top=1,bottom=0,left="START",right="END",color="green",source=cds)
show(p)