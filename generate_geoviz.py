import warnings
from bokeh.palettes import brewer, inferno
from bokeh.io import curdoc
from sklearn.preprocessing import MinMaxScaler
import pandas as pd
import numpy as np
import json

from bokeh.io import show
from bokeh.io import output_notebook, show, output_file
from bokeh.models import (CDSView, ColorBar, ColumnDataSource,BooleanFilter, GroupFilter,
                          CustomJS, CustomJSFilter, 
                          GeoJSONDataSource, HoverTool,
                          PanTool,WheelZoomTool,BoxZoomTool,
                          LinearColorMapper, Slider, WMTSTileSource)
from bokeh.layouts import column, row, widgetbox
from bokeh.palettes import brewer, Category10
from bokeh.plotting import figure

from bokeh.plotting import figure, output_file, show
from bokeh.tile_providers import Vendors, get_provider
from pyproj import Proj, transform


terrorism_df = pd.read_csv('terrorism_fixed.csv')
terrorism_df[['city', 'Target', 'Summary', 'Motive']] = terrorism_df[['city', 'Target', 'Summary', 'Motive']].fillna("Missing")
plot_df = terrorism_df.dropna()
plot_df = plot_df[plot_df['total_effected'] > 0]
plot_df['total_effected'] = plot_df['total_effected'] 

def scale_data(df):
    df['total_effected_scaled'] = (scaler.fit_transform(df['total_effected'].values.reshape(-1,1)) *200) + 5
    return df

def get_year_data(year):
    terrorism_year = plot_df[plot_df['Year'] == year]
    return terrorism_year



attack_types = list(plot_df['AttackType'].unique())
num_groups = len(attack_types)
palette = Category10 
colors = palette[num_groups]
# colors = inferno(num_groups)
color_map = {}

for i,g in enumerate(plot_df['AttackType'].unique()):
    color_map[g] = colors[i]

scaler = MinMaxScaler()
plot_df['color'] = [ color_map[x] for x in list(plot_df['AttackType'].values)]

plot_df = scale_data(plot_df)

start_year = get_year_data(2017)
left = min(start_year['E']) - 1000
right = max(start_year['E']) + 1000
bottom = min(start_year['N']) - 1000
top = max(start_year['N']) + 1000

hover = HoverTool(tooltips = [ ('Killed','@Killed'),('Wounded', '@Wounded'), ('city','@city'), ('Target','@Target'), ('Summary','@Summary'), ('Motive','@Motive')])
p = figure(x_range=(left,right), y_range=(bottom,top),x_axis_type="mercator",y_axis_type="mercator", plot_width=1500, plot_height=1000, tools=[hover, WheelZoomTool(),BoxZoomTool(), PanTool()])
p.add_tile(get_provider(Vendors.CARTODBPOSITRON_RETINA))
p.axis.visible=False
p.xgrid.grid_line_color = None
p.ygrid.grid_line_color = None

source0 = ColumnDataSource(start_year[start_year['AttackType'] == attack_types[0]])
source1 = ColumnDataSource(start_year[start_year['AttackType'] == attack_types[1]])
source2 = ColumnDataSource(start_year[start_year['AttackType'] == attack_types[2]])
source3 = ColumnDataSource(start_year[start_year['AttackType'] == attack_types[3]])
source4 = ColumnDataSource(start_year[start_year['AttackType'] == attack_types[4]])
source5 = ColumnDataSource(start_year[start_year['AttackType'] == attack_types[5]])
source6 = ColumnDataSource(start_year[start_year['AttackType'] == attack_types[6]])
source7 = ColumnDataSource(start_year[start_year['AttackType'] == attack_types[7]])
source8 = ColumnDataSource(start_year[start_year['AttackType'] == attack_types[8]])

source_list = [source0, source1, source2, source3, source4, source5, source6, source7, source8]
for s in source_list:
    p.scatter(source=s,
         x='E', 
         y='N', 
         size = 'total_effected_scaled',
         line_color='color', 
         fill_color="color", 
         legend_group='AttackType', 
         muted_color='color', 
         muted_alpha=0.2,fill_alpha=0.45)

def update_plot(attr,old, new):
    year = slider.value
    new_df = get_year_data(year)
    source0.data = new_df[new_df['AttackType'] == attack_types[0]]
    source1.data = new_df[new_df['AttackType'] == attack_types[1]]
    source2.data = new_df[new_df['AttackType'] == attack_types[2]]
    source3.data = new_df[new_df['AttackType'] == attack_types[3]]
    source4.data = new_df[new_df['AttackType'] == attack_types[4]]
    source5.data = new_df[new_df['AttackType'] == attack_types[5]]
    source6.data = new_df[new_df['AttackType'] == attack_types[6]]
    source7.data = new_df[new_df['AttackType'] == attack_types[7]]
    source8.data = new_df[new_df['AttackType'] == attack_types[8]]
    p.title.text = 'Total effected by terrorism in {}'.format(year)

    
p.legend.location = "bottom_left"
p.legend.click_policy="hide"
slider = Slider(title= 'Year', start=1970, end=2017, step=1, value=2017)
slider.on_change('value', update_plot)
layout = column(p, widgetbox(slider))
curdoc().add_root(layout)
show(layout)
