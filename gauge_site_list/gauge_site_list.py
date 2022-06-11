# -*- coding: utf-8 -*-
"""
Created on Thu Mar 25 13:00:57 2021

@author: IHiggins
"""
import fpdf #pip3 install fpdf
import pyodbc
import pandas as pd
from datetime import date
import webbrowser
import plotly.express as px
import plotly.io
import plotly.graph_objects as go
import datetime as dt
from dateutil import relativedelta
from datetime import timedelta
from urllib.request import urlopen
import json
import re
import configparser
# dev server KCITSQLDEVNRP01
# server NRDOSQLPrX01
conn = pyodbc.connect('Driver={SQL Server};'
                          'Server=10.82.12.39;'
                          'Database=gData;'
                          'Trusted_Connection=yes;')

#Title = 'SITES'
#Gauger = 2

# tbl dataprocessor
# Dave Funke =1
# Brendan 2
# Andrew 42
# Dan 5
# Bailey = 55
# IAN = 47


''' Total site count is based on the raw number of active sites
    Count of site type is an undercount as a few sits do not have
    a site type attributed to them and were not queried'''
administrative_time = .2
# Number of Discharge Sites in a Day
discharge_field = 5
# Office is a modifier of total days; office days needed for a complete field day of activity type (sites per day)
discharge_office = 4
discharge_visits = 10
# Extra work is days per site per year
discharge_extra_work = 1
discharge_days_per_site = ((((1/discharge_field)+(1/discharge_office))*discharge_visits)+discharge_extra_work)*(1+administrative_time)
# Number of Precipitation Sites in a Day
precipitation_field = 6
precipitation_office = 4
precipitation_visits = 4
precipitation_extra_work = 0.5
precipitation_days_per_site = ((((1/precipitation_field)+(1/precipitation_office))*precipitation_visits)+precipitation_extra_work)*(1+administrative_time)
#water level accounts for staff, well level, and lake level

# A gauger can get more then 6 done in a day, however we generally complete
# one projuect per day, so this number should be closer to average
# project size as opposed to the maximum theoretical rate
level_field = 6
level_office = 6
level_visits = 4
level_extra_work = 0.75
level_days_per_site = ((((1/level_field)+(1/level_office))*level_visits)+level_extra_work)*(1+administrative_time)

water_temperature_field = 10
water_temperature_office = 0.5
water_temperature_visits = 2
water_temperature_extra_work = 0.2
water_temperature_days_per_site = ((((1/water_temperature_field)+(1/water_temperature_office))*water_temperature_visits)+water_temperature_extra_work)*(1+administrative_time)

#net total days is total possible (260) - Holidays (11) = net (237), excludes vacation time
Total_Days_Available = 249
'''
pdf = fpdf.FPDF(format='letter') #pdf format
#set defult line hite
h = 6
secondary_bar = 110
#Page 1 pdf of assumptions
pdf.add_page() #create new page
pdf.set_font("Arial", size=12)
pdf.set_font("Arial", style = 'B', size = 12) 
pdf.cell(200, h, txt="Assumptions for Site Lists", ln=1, align="C")
pdf.cell(200, h = 0, txt = '', border = 0, ln = 10, align = '', fill = True, link = '')
pdf.set_font("Arial", size=12)

pdf.cell(200, h, txt=" ", ln=6, align="L")
pdf.set_font("Arial", style = 'B', size = 12) 

pdf.cell(200, h, txt="Budget Time Per Project Type", ln=2, align="L")
pdf.set_font("Arial", size=12)
pdf.cell(200, h = 0, txt = '', border = 0, ln = 10, align = '', fill = True, link = '')
pdf.cell(200, h, txt=" ", ln=6, align="L")
pdf.cell(200, h, txt="Budget Time For Discharge Sites: ", ln=3, align="L")
pdf.cell(secondary_bar, h = 0, txt = '', border = 0, ln = 10, align = '', fill = True, link = '')
pdf.cell(200, h, txt="        Discharge Sites Per Field Day: "+str(discharge_field), ln=4, align="L")
pdf.cell(200, h, txt="        Discharge Office Days Per Field Day: "+str(discharge_office), ln=5, align="L")
pdf.cell(200, h, txt="        Discharge Visits Per Year: "+str(discharge_visits), ln=5, align="L")
pdf.cell(200, h, txt="        Discharge Extra Work Per Site/Year: "+str(discharge_extra_work), ln=6, align="L")
pdf.cell(200, h, txt=" ", ln=6, align="L")

pdf.cell(200, h, txt="Budget Time For Water Level Sites: ", ln=3, align="L")
pdf.cell(secondary_bar, h = 0, txt = '', border = 0, ln = 10, align = '', fill = True, link = '')
pdf.cell(200, h, txt="        Water Level Sites Per Field Day: "+str(level_field), ln=4, align="L")
pdf.cell(200, h, txt="        Water Level Office Days Per Field Day: "+str(level_office), ln=5, align="L")
pdf.cell(200, h, txt="        Water Level Visits Per Year: "+str(level_visits), ln=5, align="L")
pdf.cell(200, h, txt=" ", ln=6, align="L")

pdf.cell(200, h, txt="Budget Time For Precipitation Sites: ", ln=3, align="L")
pdf.cell(secondary_bar, h = 0, txt = '', border = 0, ln = 10, align = '', fill = True, link = '')
pdf.cell(200, h, txt="        Precipitation Sites Per Field Day: "+str(precipitation_field), ln=4, align="L")
pdf.cell(200, h, txt="        Precipitation Office Days Per Field Day: "+str(precipitation_office), ln=5, align="L")
pdf.cell(200, h, txt="        Precipitation Visits Per Year: "+str(precipitation_visits), ln=5, align="L")
pdf.cell(200, h, txt=" ", ln=6, align="L")

pdf.cell(200, h, txt="Budget Time For Water Temperature Sites: ", ln=3, align="L")
pdf.cell(secondary_bar, h = 0, txt = '', border = 0, ln = 10, align = '', fill = True, link = '')
pdf.cell(200, h, txt="        Water Temperature Sites Per Field Day: "+str(water_temperature_field), ln=4, align="L")
pdf.cell(200, h, txt="        Water Temperature Office Days Per Field Day: "+str(water_temperature_office), ln=5, align="L")
pdf.cell(200, h, txt="        Water Temperature Visits Per Year: "+str(water_temperature_visits), ln=5, align="L")
pdf.cell(200, h, txt=" ", ln=6, align="L")

pdf.cell(200, h, txt="Budget Time For Administrative Tasks: ", ln=3, align="L")
pdf.cell(secondary_bar, h = 0, txt = '', border = 0, ln = 10, align = '', fill = True, link = '')
pdf.cell(200, h, txt="        "+str(administrative_time*100)+"%", ln=5, align="L")
pdf.cell(200, h, txt=" ", ln=6, align="L")

pdf.set_font("Arial", style = 'B', size = 12) 
pdf.cell(200, h, txt="Assumptions for Total Time", ln=1, align="L")
pdf.set_font("Arial", size=12)
pdf.cell(200, h = 0, txt = '', border = 0, ln = 10, align = '', fill = True, link = '')
pdf.cell(200, h, txt="        Total Days of Work Per Year: 260", ln=1, align="L")
pdf.cell(200, h, txt="              Vacation Days Per Year: Based on County Tenure", ln=1, align="L")
pdf.cell(200, h, txt="              Holiday Days Per Year: 11", ln=1, align="L")
pdf.cell(200, h, txt="        Net Days of Work (excluding vacation time): "+str(Total_Days_Available), ln=1, align="L")
'''
# get all sites
active_sites = pd.read_sql_query('select G_ID, SITE_CODE, SITE_NAME, GAUGER_NAME, LAT, LON, STATUS, DATE_INSTA, COMMENT, GAGETAG, Precip, Turbidity, WaterTemp, FlowLevel, Piezometer, LakeLevel from tblGaugeLLID;',conn)
# filter by active sites, I messed up the SQL query, this is lazy
active_sites = active_sites[active_sites.STATUS=='Active']
# remove activive sites column
# remove columns
active_sites = active_sites.drop(['STATUS'], axis=1)
# get list of gaugers
gaugers = pd.read_sql_query('select Data_Processor_ID, Processor_Name from tblDataProcessor;',conn)
print("gaugers")
print(gaugers)
# match name to numbers
active_sites = active_sites.merge(gaugers, left_on='GAUGER_NAME', right_on='Data_Processor_ID', how="left")
# remove excess columns
active_sites = active_sites.drop(['GAUGER_NAME','Data_Processor_ID'], axis=1)
active_sites.to_csv(r"W:\STS\hydro\GAUGE\Temp\Ian's Temp\Site Lists\\gaugers "+str(date.today())+".csv")
# length oLength of monitoring. 
active_sites['DATE_INSTA'] = pd.to_datetime(active_sites['DATE_INSTA'])
active_sites["Length of Monitoring (Years)"] = active_sites['DATE_INSTA'].subtract(dt.datetime.now()).dt.days
active_sites["Length of Monitoring (Years)"] = active_sites["Length of Monitoring (Years)"].abs()
active_sites["Length of Monitoring (Years)"] = (active_sites["Length of Monitoring (Years)"]/360).round(1)
active_sites['Date Installed'] = active_sites['DATE_INSTA']
active_sites = active_sites.drop(['Date Installed'], axis=1)


# Projects
active_sites.sort_values(by='SITE_CODE', inplace=True)
#COMBO_CODES = pd.read_excel('W:\STS\hydro\GAUGE\zzz_Project_Numbers_Current_2021.xlsx', sheet_name='2021 gager combo codes_current', header=1)
project_id = pd.read_sql_query('select G_ID, project_id from tblProjectGauge;',conn)

active_sites = active_sites.merge(project_id, on='G_ID', how='left')

projects = pd.read_sql_query('select id, project_name, start_date, end_date, description, project_number from tblProject;',conn)
projects = projects.rename(columns={"id": "project_id"})

active_sites = active_sites.merge(projects, on='project_id', how='left')

# adds eres modifier to projects, creates a new project df to not mess anything up
active_sites.loc[active_sites['project_name'].str.contains('eres', case=False, na=False, regex=False), "loan out"] = "ERES"
# adds rfms modifier to projects, creates a new project df to not mess anything u
active_sites.loc[active_sites['project_name'].str.contains('rfms', case=False, na=False, regex=False), "loan out"] = "RFMS"

# add telemetry status
tele_status = pd.read_sql_query('select G_ID, SITE_CODE, RealTime from tblGaugeLLID;',conn)
tele_status.sort_values(by='G_ID', inplace=True)
tele_status.sort_values(by='G_ID', inplace=True)
active_sites = active_sites.merge(tele_status, on='G_ID')

def f(x):
    if (x['FlowLevel'] == True):
        return "discharge"
    else:
        return ""
active_sites['discharge'] = active_sites.apply(f, axis=1)

# discharge remove lake level duplicates
def f(x):
    if (x['LakeLevel'] == True):
        return ""
    else:
        return x['discharge']
active_sites['discharge'] = active_sites.apply(f, axis=1)

# discharge remove wel level duplicates
def f(x):
    if (x['Piezometer'] == True):
        return ""
    else:
        return x['discharge']
active_sites['discharge'] = active_sites.apply(f, axis=1)

# water level sites
def f(x):
    if x['LakeLevel'] == True:
        return "water_level"
    else:
        return ""
active_sites['water_level'] = active_sites.apply(f, axis=1)

# groundwater sitews
def f(x):
    if (x['Piezometer'] == True) and (x['LakeLevel'] == ""):
        return "water_level"
    else:
        return x['water_level']
active_sites['water_level'] = active_sites.apply(f, axis=1)

# water temperature only -remove flow
def f(x):
    if (x['WaterTemp'] == True) and (x['FlowLevel'] == ""):
        return "water_temperature"
    else:
        return ""
active_sites['water_temperature'] = active_sites.apply(f, axis=1)

# rain gages
def f(x):
    if x['Precip'] == True:
        return "rain_gauge"
    else:
        return ""
active_sites['rain_gauge'] = active_sites.apply(f, axis=1)

# turbidity
def f(x):
    if (x['Turbidity'] == True) and (x['FlowLevel'] == False):
        return "turbidity"
    else:
        return ""
active_sites['turbidity'] = active_sites.apply(f, axis=1)

# sites
# combine
active_sites["type"] = active_sites['discharge'].astype(str) +" "+ active_sites['water_level'].astype(str) +" "+ active_sites['water_temperature'].astype(str) +" "+ active_sites['rain_gauge'].astype(str) +" "+ active_sites['turbidity'].astype(str)
# strip
active_sites["type"] = active_sites["type"].str.strip()


# remove columns
active_sites = active_sites.drop(['Precip','WaterTemp','FlowLevel','Piezometer','LakeLevel','discharge', 'water_level', 'water_temperature', 'rain_gauge', 'Turbidity', 'turbidity'], axis=1)

# calculate days of work
#calculate site days
active_sites.loc[active_sites['type'].str.contains('discharge', case=False, na=False, regex=False), "days"] = discharge_days_per_site
active_sites.loc[active_sites['type'].str.contains('water_level', case=False, na=False, regex=False), "days"] = level_days_per_site
active_sites.loc[active_sites['type'].str.contains('rain_gauge', case=False, na=False, regex=False), "days"] = precipitation_days_per_site
active_sites.loc[active_sites['type'].str.contains('water_temperature', case=False, na=False, regex=False), "days"] = water_temperature_days_per_site
active_sites.loc[active_sites['type'].str.contains('turbidity', case=False, na=False, regex=False), "days"] = discharge_days_per_site


print(active_sites)
active_sites.to_csv(r"W:\STS\hydro\GAUGE\Temp\Ian's Temp\Site Lists\\all sites "+str(date.today())+".csv")
discharge_filter = active_sites[(active_sites.type == "discharge") & (active_sites.type == "discharge")]
print("discharge filter")
print(discharge_filter)

def Gauge_Assignments():
    # kinda a hacky way of doing this but its an add on
    global Global_Discharge_Days_With_Extra
    global Global_Level_Days
    global Global_Precipitation_Days
    global Global_Water_Temperature_Days
    global Global_Other_Project
    global Global_Vacation_Days
    global Total_Discharge
    global Total_Water_Level
    global Total_Groundwater_Well
    global Total_Precipitation
    global Total_Water_Temperature
    
    #NAME
    print("")
    print(str(Name))
    # Total Sites
   # print(""+str(sites_active.shape[0]))
    pdf.set_font("Arial", style = 'B', size = 12) 
    pdf.cell(200, h, txt=str(Name)+" Site List", ln=1, align="C")
    # ANNON
    #pdf.cell(200, h, "GAUGER Site List", ln=1, align="C")
    pdf.set_font("Arial", size=12) # font and textsize
    pdf.cell(200, h = 0, txt = '', border = 0, ln = 10, align = '', fill = True, link = '')
    pdf.cell(200, h, txt="Total Sites "+str(sites_active.shape[0])+" *", ln=2, align="C")
    pdf.cell(200, h = 0, txt = '', border = 0, ln = 10, align = '', fill = True, link = '')
    # Parsed Sites
    # Stream gauge recording

    Gauge_Type_Input = "Discharge"
    sites_filter = sites_active[sites_active.FlowLevel == True]
    raw_discharge = sites_filter.shape
    raw_discharge = raw_discharge[0]

    # Modifier to remove duplicates
    # Gauge_Type_Input = "Water Level and Discharge"
    dual_waterlevel_filter = sites_active[sites_active.LakeLevel & sites_active.FlowLevel == True]
    dual_waterlevel = dual_waterlevel_filter.shape
    dual_waterlevel = dual_waterlevel[0]

    # Gauge_Type_Input = "Piezometer and Discharge"
    sites_filter = sites_active[sites_active.Piezometer & sites_active.FlowLevel == True ]
    dual_piezometer = sites_filter.shape
    dual_piezometer = dual_piezometer[0]
    print(f"raw_discharge {raw_discharge}")
    print(f"dual_waterlevel {dual_waterlevel}")
    print(f"dual_piezometer {dual_piezometer}")
    Discharge_Sites = raw_discharge-(dual_waterlevel+dual_piezometer)
    print(f"Discharge_Sites {Discharge_Sites}")
    ### CONFUSED? somesites are actually lake level or piezometer and incorrectly labeled as both discharge and lake level
    pdf.cell(200, h, txt=Gauge_Type_Input+" Sites: "+str(Discharge_Sites), ln=3, align="L")

    discharge_days = (((Discharge_Sites/Discharge_Field)*(1+Discharge_Office))*Discharge_Visits)
    discharge_field_days = Discharge_Sites/Discharge_Field
    print(f"discharge field days ({Discharge_Field} sites/day) = {discharge_field_days}")
    discharge_office_days = discharge_field_days*Discharge_Office
    print(f"discharge office days ({Discharge_Office} days/field day) = {discharge_office_days}")
    discharge_days_per_visit = discharge_field_days+discharge_office_days
    print(f"discharge days per visit (field days + office days) ({discharge_office_days} + {discharge_days_per_visit}) = {discharge_days_per_visit}")
    discharge_days_per_year = discharge_days_per_visit*Discharge_Visits
    print(f"discharge days per year (days to visit each site once * visits per year) ({discharge_days_per_visit} * {Discharge_Visits}) = {discharge_days_per_year}")
    discharge_extra = Discharge_Sites*discharge_extra_work
    print(f"discharge extra days ({discharge_extra_work}/site) {discharge_extra}")
    print(f"origional discharge days {discharge_days}")
    discharge_days = discharge_days_per_year + discharge_extra
    print(f"total discharge days {discharge_days}")
    

    pdf.cell(200, h, txt=Gauge_Type_Input+" Sites: "+str(groundwater), ln=5, align="L")
    print(f"water level (lake level) sites {waterlevel_sites}")
    print(f"groundwater (piezometer) sites {groundwater}")
    level_sites = waterlevel_sites+groundwater
    print(f"level sites (water level + groundwater) = {level_sites}")
   
    # Level Sites Calculation
    Level_Days = (((level_sites/level_field)*(1+level_office))*level_visits)
    
    level_field_days = round(level_sites/level_field,1)
    print(f"level field days ({level_field} sites/day) = {level_field_days}")
    level_office_days = level_field_days*level_office
    print(f"level office days ({level_office} days/field day) = {level_office_days}")
    level_days_per_visit = level_field_days+level_office_days
    print(f"level days per visit (field days + office days) ({level_office_days} + {level_days_per_visit}) = {level_days_per_visit}")
    level_days_per_year = level_days_per_visit*level_visits
    print(f"origional {Level_Days}")
    level_days = level_days_per_year
    print(f"total level days {level_days}")

    Gauge_Type_Input = "Rain Gauge"
    sites_filter = sites_active[sites_active.Precip == True]
    Number_Basic = sites_filter.shape
    Number = Number_Basic[0]
    Rain_Sites = Number
    print(Number)
    pdf.cell(200, h, txt=Gauge_Type_Input+" Sites: "+str(Number), ln=8, align="L")
    #print(((Gauge_Type()/Precipitation)*2).round(0))
    Precipitation_Days = (((Number/Precipitation_Field)*(1+Precipitation_Office))*Precipitation_Visits)
    
    Gauge_Type_Input = "Water Temperature"
    sites_filter = sites_active[sites_active.GAGETAG == "Water Temperature Recorder"]
    Number_Basic = sites_filter.shape
    Number = Number_Basic[0]
    Water_Temp_Sites = Number


    Water_Temperature_Days = (((Number/Water_Temperature_Field)*(1+Water_Temperature_Office))*Water_Temperature_Visits)
    
    pdf.cell(200, h, txt=Gauge_Type_Input+" Sites: "+str(Number), ln=9, align="L")
    
    Total_Days = discharge_days+Level_Days+Precipitation_Days+Water_Temperature_Days+Other_Project_Days
    Total_Days_With_Admin = (Total_Days+((Total_Days*Administrative_Time)))
    
    Open_Time = (Total_Days_Available-Total_Days_With_Admin-Vacation_Days)
    #pdf.cell(200, h = 0, txt = '', border = 0, ln = 10, align = '', fill = True, link = '')
    pdf.cell(200, h, txt=" ", ln=6, align="L")
    pdf.set_fill_color(182, 208, 226) # BLUE
    pdf.cell(200, h, txt=" Days of Work", ln=11, align="L", fill = True)
    pdf.set_fill_color(0, 0, 0) # BLACK
    pdf.cell(200, h = .3, txt = '', border = 0, ln = 10, align = '', fill = True, link = '')
    pdf.set_fill_color(182, 208, 226)
    # converting to an integer and rounding is probably a bit excessive but they started as floats and it seemed easier to just change it to int
    pdf.cell(200, h, txt="    Discharge Days "+str(int(round(discharge_days,0))), ln=12, align="L", fill = True)
    
    pdf.cell(200, h, txt="    Water Level Days "+str(int(round(Level_Days,0))), ln=13, align="L", fill=True)
    pdf.cell(200, h, txt="    Precipitation Days "+str(int(round(Precipitation_Days,0))), ln=14, align="L", fill=True)
    pdf.cell(200, h, txt="    Temperature Days "+str(int(round(Water_Temperature_Days,0))), ln=15, align="L", fill=True)
    pdf.cell(200, h, txt="    Additional Projects: "+str(Other_Project)+" "+str(int(round(Other_Project_Days,0))), ln=15, align="L", fill=True)
    
    pdf.cell(200, h, txt="    Administrative Time "+str(round(Total_Days*Administrative_Time,0)), ln=16, align="L", fill=True)
    pdf.cell(200, h, txt="    Vacation Days "+str(int(round(Vacation_Days))), ln=16, align="L", fill=True)
    pdf.cell(200, h, txt="    Total Days Comitted To "+str(int(round(Total_Days_With_Admin,0))), ln=117, align="L", fill=True)
    pdf.cell(200, h, txt=" ", ln=6, align="L", fill=True)
    pdf.set_font("Arial", style = 'B', size = 12) 
    if Open_Time < 0:
        pdf.set_text_color(255,0,0)  # change font color to red
        pdf.cell(200, h, txt="    Available Days "+str(int(round(Open_Time,0))), ln=18, align="L", fill=True)
        pdf.set_text_color(0,0,0)  # reset back to black
    if Open_Time >= 0:
        pdf.cell(200, h, txt="    Available Days "+str(int(round(Open_Time,0))), ln=18, align="L", fill=True)
    pdf.set_font("Arial", size=12) # font and textsize
    pdf.set_fill_color(0, 0, 0) # BLACK
    # Create PIE chart
    d = {'col1': ['Discharge Days', 'Level Days','Precipitation Days','Water Temperature Days', 'Additional Projects'], 'col2': [discharge_days, Level_Days, Precipitation_Days, Water_Temperature_Days, Other_Project_Days]}
    df = pd.DataFrame(data=d)
    
    
    
    
    fig_width = 350
    fig_height = 350
    fig = px.pie(values=df['col2'], names=df['col1'],title='Site Breakdown', width=fig_width, height=fig_height)
    fig.update_layout(legend=dict(
    yanchor="top",
    y=0.0001,
    xanchor="left",
    x=0.01))
    fig.update_layout(legend= {'itemsizing': 'constant'})
    #fig.update_layout(width=fig_width, height=fig_height)
    map_width = 350
    map_height = 350
    fig_map = px.scatter_mapbox(lat=sites_active['LAT'], lon=sites_active['LON'], width=map_width, height=map_height)
    fig_map.update_layout(mapbox_style="open-street-map")
    fig_map.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

    # pie chart
    plotly.io.write_image(fig,file='pltx '+str(Name)+'.jpeg',format='jpeg')
    # map
    plotly.io.write_image(fig_map,file='pltx_map '+str(Name)+'.jpeg',format='jpeg')
    #fig=(os.getcwd()+'/'+"pltx.png")
    ### define a method
    #def charts(self):
     #   self.set_xy(40.0,25.0)
      #  self.image(fig,  link='', type='', w=700/5, h=450/5)
   
    img_width = 110
    img_height = 110
    img_y = 130
    pdf.image(r'C:\Users\ihiggins\.spyder-py3\pltx '+str(Name)+'.jpeg', x=4, y=img_y, w=img_width, h=img_height)
    pdf.image(r'C:\Users\ihiggins\.spyder-py3\pltx_map '+str(Name)+'.jpeg', x=100, y=img_y, w=img_width, h=img_height)
     ### FOOTER
    pdf.set_y(250)

        # Page number
    pdf.set_font("Arial", size=10)
    pdf.set_text_color(128,128,128)  # reset back to black
    pdf.cell(0, h = 0, txt = '', border = 0, ln = 10, align = '', fill = True, link = '')
    pdf.cell(0, h, '* Obtained from site assignment, number may differ from total site count as they are two independent metrics', 0, 0, 'C')
    pdf.set_y(253)
    pdf.cell(0, h, str(date.today()), 0, 0, 'C')
    
    
    pdf.set_font("Arial", size=12)
    pdf.set_text_color(0,0,0)  # reset back to black
    
    #sites_active['Type'] = sites_active['Precip']+sites_active['Precip']
   # print(sites_active['Type'])
    sites_active['Gauger']  = str(Name)
    sites_active = sites_active[['G_ID','SITE_CODE','SITE_NAME','LAT','LON', 'Date Installed', "Length of Monitoring (Years)",'Gauger','COMMENT','Precip', 'Turbidity', 'WaterTemp', 'FlowLevel', 'Piezometer', 'LakeLevel']]
    sites_active.to_csv(r"W:\STS\hydro\GAUGE\Temp\Ian's Temp\Site Lists\\"+str(Name)+" Sites "+str(date.today())+".csv")
    
    # counter for all guagers
    if discharge_days == "":
        discharge_days = 0
    if level_days == "":
        level_days = 0
    if Precipitation_Days == "":
        Precipitation_Days = 0
    if Water_Temperature_Days == "":
        Water_Temperature_Days = 0

    if Discharge_Sites == "":
        Discharge_Sites = 0
    if waterlevel_sites == '':
        Waterlevel_sites = 0   
    if Water_Temp_Sites == "":
        Water_Temp_Sites = 0
    if Rain_Sites == "":
        Rain_Sites = 0
    if groundwater == "":
        groundwater = 0
    Total_Discharge = Total_Discharge+Discharge_Sites
    Total_Water_Level = Total_Water_Level + waterlevel_sites
    Total_Precipitation = Total_Precipitation+Rain_Sites
    Total_Water_Temperature = Total_Water_Temperature + Water_Temp_Sites
    Total_Groundwater_Well = Total_Groundwater_Well + groundwater

    Global_Discharge_Days_With_Extra = Global_Discharge_Days_With_Extra+float(discharge_days)
    Global_Level_Days = Global_Level_Days+float(Level_Days)
    Global_Precipitation_Days =  Global_Precipitation_Days+float(Precipitation_Days)
    Global_Water_Temperature_Days = Global_Water_Temperature_Days+float(Water_Temperature_Days)
    Global_Other_Project = Global_Other_Project+float(Other_Project_Days)
    Global_Vacation_Days = Global_Vacation_Days+float(Vacation_Days)
    

    return sites_active


Global_Discharge_Days_With_Extra = 0
Global_Level_Days = 0
Global_Precipitation_Days = 0
Global_Water_Temperature_Days = 0
Global_Other_Project = 0
Global_Vacation_Days = 0
Total_Discharge = 0
Total_Water_Level = 0
Total_Precipitation = 0
Total_Water_Temperature = 0
Total_Groundwater_Well = 0

# this is taken from tblDataProcessor
Gauger = 2
Name = "Brendan Grant"
# service years as of 9/2021 = 30 add 2 extra days
Vacation_Days = 32
Other_Project = "Team Lead"
Other_Project_Days = 100
List_1 = Gauge_Assignments()

Gauger = 42
Name = "Andrew Miller"
# service years as of 9/2021 = 9 add 2 extra days
Vacation_Days = 0
Other_Project = ""
Other_Project_Days = 0
List_2 = Gauge_Assignments()

Gauger = 5
Name = "Dan Smith"
# service years as of 9/2021 = 22 add 2 extra days
Vacation_Days = 28
Other_Project = ""
Other_Project_Days = 0
List_3 = Gauge_Assignments()

Gauger = 55
Name = "Bailey Keeler"
# service years as of 9/2021 = 4 add 2 extra days
Vacation_Days = 12
Other_Project = "ADAP Work"
Other_Project_Days = 15
List_4 = Gauge_Assignments()

Gauger = 47
Name = "Ian Higgins"
# service years as of 9/2021 = 4 add 2 extra days
Vacation_Days = 12
Other_Project = "CAO Project"
Other_Project_Days = 30
List_5 = Gauge_Assignments()

Gauger = 57
Name = "Kyle Bliss"
# service years as of 9/2021 = 4 add 2 extra days
Vacation_Days = 12
Other_Project = "Fish Work"
Other_Project_Days = (261/2)
List_6 = Gauge_Assignments()

Gauger = 59
Name = "Dean Wilson"
# service years as of 9/2021 = 4 add 2 extra days
Vacation_Days = 12
Other_Project = ""
Other_Project_Days = 0
List_7 = Gauge_Assignments()


'''
Gauger = 1
Name = "Dave Funke"
# service years as of 9/2021 = 30 add 2 extra days
Vacation_Days = 32
Other_Project = ""
Other_Project_Days = 0
List_6 = Gauge_Assignments()
'''
Total_Gaugers = 5
Net_Days_Of_Work = 249
Vacation_Time = 20
Total_Days_All = ((249)*5)-Global_Vacation_Days

# global values for all gaugers work

print(Global_Discharge_Days_With_Extra)
print(Global_Level_Days)
print(Global_Precipitation_Days)
print(Global_Water_Temperature_Days)
print(Global_Other_Project)


frames = [List_1, List_2, List_3, List_4, List_5, List_6, List_7]
result = pd.concat(frames)


    ################# CREATE ALL SITES LIST ######################################
def All_Assignments():
    pdf.add_page() #create new page
    pdf.set_font("Arial", size=12) # font and textsize
    pdf.set_font("Arial", style = 'B', size = 12) 
    pdf.cell(200, h, "All Sites", ln=1, align="C")
    pdf.set_font("Arial", size=12) # font and textsize
    pdf.cell(200, h = 0, txt = '', border = 0, ln = 10, align = '', fill = True, link = '')
    pdf.cell(200, h, txt="Total Sites "+str(int(Total_Discharge+Total_Water_Level+Total_Groundwater_Well+Total_Precipitation+Total_Water_Temperature))+" ^", ln=2, align="C")
    pdf.cell(200, h = 0, txt = '', border = 0, ln = 10, align = '', fill = True, link = '')
    # Stream gauge recording
    #pdf.cell(200, h, txt=" ", ln=6, align="L")
    pdf.cell(200, h, txt="    Discharge Sites: "+str(int(round(Total_Discharge,0))), ln=12, align="L", fill = False)
    pdf.cell(200, h, txt="    Water Level Sites: "+str(int(round(Total_Water_Level,0))), ln=12, align="L", fill = False)
    pdf.cell(200, h, txt="    Groundwater Well Sites: "+str(int(round(Total_Groundwater_Well,0))), ln=12, align="L", fill = False)
    pdf.cell(200, h, txt="    Rain Gauge Sites: "+str(int(round(Total_Precipitation,0))), ln=12, align="L", fill = False)
    pdf.cell(200, h, txt="    Water Temperature Sites: "+str(int(round(Total_Water_Temperature,0))), ln=12, align="L", fill = False)


   # pdf.cell(200, h, txt=Gauge_Type_Input+" "+str(Number), ln=9, align="L")

    Total_Days = Global_Discharge_Days_With_Extra+Global_Level_Days+Global_Precipitation_Days+Global_Water_Temperature_Days+Global_Other_Project
    Total_Days_With_Admin = (Total_Days+((Total_Days*Administrative_Time)))

    Open_Time = (Total_Days_All-Total_Days_With_Admin)
    #pdf.cell(200, h = 0, txt = '', border = 0, ln = 10, align = '', fill = True, link = '')
    pdf.cell(200, h, txt=" ", ln=6, align="L")
    pdf.set_fill_color(182, 208, 226) # BLUE
    pdf.cell(200, h, txt=" Days of Work", ln=11, align="L", fill = True)
    pdf.set_fill_color(0, 0, 0) # BLACK
    pdf.cell(200, h = .3, txt = '', border = 0, ln = 10, align = '', fill = True, link = '')
    pdf.set_fill_color(182, 208, 226)
    pdf.cell(200, h, txt="    Discharge Days "+str(int(round(Global_Discharge_Days_With_Extra,0))), ln=12, align="L", fill = True)

    pdf.cell(200, h, txt="    Water Level Days "+str(int(round(Global_Level_Days,0))), ln=13, align="L", fill=True)
    pdf.cell(200, h, txt="    Precipitation Days "+str(int(round(Global_Precipitation_Days,0))), ln=14, align="L", fill=True)
    pdf.cell(200, h, txt="    Temperature Days "+str(int(round(Global_Water_Temperature_Days,0))), ln=15, align="L", fill=True)
    pdf.cell(200, h, txt="    Additional Projects: "+str(int(round(Other_Project_Days,0))), ln=15, align="L", fill=True)

    pdf.cell(200, h, txt="    Administrative Time "+str(int(round(Total_Days*Administrative_Time,0))), ln=16, align="L", fill=True)
    pdf.cell(200, h, txt="    Vacation Days "+str(int(round(Global_Vacation_Days))), ln=16, align="L", fill=True)
    pdf.cell(200, h, txt="    Total Days Comitted To "+str(int(round(Total_Days_With_Admin,0))), ln=117, align="L", fill=True)
    pdf.cell(200, h, txt=" ", ln=6, align="L", fill=True)
    pdf.set_font("Arial", style = 'B', size = 12) 
    if Open_Time < 0:
        pdf.set_text_color(255,0,0)  # change font color to red
        pdf.cell(200, h, txt="    Available Days "+str(int(round(Open_Time,0)))+"     ("+str(round((Open_Time/(Net_Days_Of_Work-Vacation_Time)),1))+" FTE)", ln=18, align="L", fill=True)
        pdf.set_text_color(0,0,0)  # reset back to black
    if Open_Time >= 0:
        pdf.cell(200, h, txt="    Available Days "+str(int(round(Open_Time,0)))+"     ("+str(round((Open_Time/(Net_Days_Of_Work-Vacation_Time)),1))+" FTE)", ln=18, align="L", fill=True)
    pdf.set_font("Arial", size=12) # font and textsize
    pdf.set_fill_color(0, 0, 0) # BLACK
        # Create PIE chart

    d = {'col1': ['Discharge Days', 'Level Days','Precipitation Days','Water Temperature Days', 'Additional Projects'], 'col2': [Global_Discharge_Days_With_Extra, Global_Level_Days, Global_Precipitation_Days, Global_Water_Temperature_Days, Global_Other_Project]}
    df = pd.DataFrame(data=d)

    fig_width = 350
    fig_height = 350
    fig = px.pie(values=df['col2'], names=df['col1'],title='Site Breakdown', width=fig_width, height=fig_height)
    fig.update_layout(legend=dict(
    yanchor="top",
    y=0.0001,
    xanchor="left",
    x=0.01))
    fig.update_layout(legend= {'itemsizing': 'constant'})
    #fig.update_layout(width=fig_width, height=fig_height)
    map_width = 350
    map_height = 350

    fig_map = px.scatter_mapbox(lat=result['LAT'], lon=result['LON'], width=map_width, height=map_height)
    fig_map.update_layout(mapbox_style="open-street-map")
    fig_map.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    # pie chart
    plotly.io.write_image(fig,file='pltx All.jpeg',format='jpeg')
    # map
    plotly.io.write_image(fig_map,file='pltx_map All.jpeg',format='jpeg')

    img_width = 110
    img_height = 110
    img_y = 130
    pdf.image(r'C:\Users\ihiggins\.spyder-py3\pltx All.jpeg', x=4, y=img_y, w=img_width, h=img_height)
    pdf.image(r'C:\Users\ihiggins\.spyder-py3\pltx_map All.jpeg', x=100, y=img_y, w=img_width, h=img_height)
    # FOOTER
    pdf.set_y(250)

    # Page number
    pdf.set_font("Arial", size=10)
    pdf.set_text_color(128,128,128)  # reset back to black
    pdf.cell(0, h = 0, txt = '', border = 0, ln = 10, align = '', fill = True, link = '')
    pdf.cell(0, h, '^ Obtained from sum of individual counts, may differ from individual total sites as they are independet metrics', 0, 0, 'C')
    pdf.set_y(253)
    pdf.cell(0, h, str(date.today()), 0, 0, 'C')

    pdf.set_font("Arial", size=12)
    pdf.set_text_color(0,0,0)  # reset back to black

    # all assignments return days per site
    discharge_site_days = Global_Discharge_Days_With_Extra/Total_Discharge
    level_site_days = Global_Level_Days/(Total_Water_Level + Total_Groundwater_Well)
    precipitationj_site_days = Global_Precipitation_Days/Total_Precipitation
    water_temperature_site_days = Global_Water_Temperature_Days/Total_Water_Temperature

    return (discharge_site_days, level_site_days, precipitationj_site_days, water_temperature_site_days)

List_6 = All_Assignments()

result.sort_values(by='SITE_CODE', inplace=True)

#COMBO_CODES = pd.read_excel('W:\STS\hydro\GAUGE\zzz_Project_Numbers_Current_2021.xlsx', sheet_name='2021 gager combo codes_current', header=1)

PROJECT_ID = pd.read_sql_query('select G_ID, project_id from tblProjectGauge;',conn)
#print(COMBO_CODES)

result = result.merge(PROJECT_ID, on='G_ID', how='left')
#result.merge(COMBO_CODES, left_on='SITE_NAME', right_on='Description')

PROJECT_INFO = pd.read_sql_query('select id, project_name, start_date, end_date, description, project_number from tblProject;',conn)
PROJECT_INFO = PROJECT_INFO.rename(columns={"id": "project_id"})

# adds eres modifier to projects, creates a new project df to not mess anything up
projects = PROJECT_INFO
projects.loc[projects['project_name'].str.contains('eres', case=False, na=False, regex=False), "loan out"] = "ERES"
# adds rfms modifier to projects, creates a new project df to not mess anything up
projects = PROJECT_INFO
projects.loc[projects['project_name'].str.contains('rfms', case=False, na=False, regex=False), "loan out"] = "RFMS"
projects.to_csv(r"W:\STS\hydro\GAUGE\Temp\Ian's Temp\Site Lists\\All Projects "+str(date.today())+".csv")

result = result.merge(PROJECT_INFO, on='project_id', how='left')

# add telemetry status
tele_status = pd.read_sql_query('select G_ID, SITE_CODE, RealTime from tblGaugeLLID;',conn)
tele_status.sort_values(by='G_ID', inplace=True)
tele_status.sort_values(by='G_ID', inplace=True)
result = result.merge(tele_status, on='G_ID')

all_sites = result

# remove columns
all_sites = all_sites.drop(['project_id','Precip','WaterTemp','FlowLevel','Piezometer','LakeLevel','discharge', 'water_level', 'water_temperature', 'rain_gauge'], axis=1)

all_sites = all_sites.drop_duplicates(subset='G_ID', keep='first', inplace=False, ignore_index=False)
all_sites.set_index('G_ID', inplace=True)
all_sites.to_csv(r"W:\STS\hydro\GAUGE\Temp\Ian's Temp\Site Lists\\All Sites "+str(date.today())+".csv")
   
pdf.output("W:\STS\hydro\GAUGE\Temp\Ian's Temp\Site Assignments_"+str(date.today())+".pdf")
webbrowser.open_new(r"W:\STS\hydro\GAUGE\Temp\Ian's Temp\Site Assignments_"+str(date.today())+".pdf")
# upgradable sites
upgradable = all_sites.loc[(all_sites['type'] == "discharge") & (all_sites['RealTime'] == False)]
#upgradable = all_sites.loc[(all_sites['RealTime'] == True)]
print("upgradable")
print(upgradable)
upgradable.to_csv(r"W:\STS\hydro\GAUGE\Temp\Ian's Temp\Site Lists\\Upgradable Sites "+str(date.today())+".csv")
def all_sites_map():
    #all_sites_map
    result.rename(columns={
                        "SITE_NAME": "site name",
                        "LAT": "lat",
                        "LON": "lon",
                        "project_name": "project",
                    }, inplace=True)

    map_width = 1500
    map_height = 900
    base_map_opacity = 0.75
    
    with urlopen('https://opendata.arcgis.com/datasets/740bef8e7bee4a4885d58d04dd3ee02f_485.geojson') as response:
        large_water = json.load(response)
    all_sites_map = px.scatter_mapbox(result, lat=result['lat'], lon=result['lon'], color=result["Gauger"], hover_name=result.index, hover_data=["site name", "lat", "lon", "project"], width=map_width, height=map_height, )
    
    all_sites_map.update_layout(
        mapbox_style="white-bg",
        mapbox_layers=[
           {
                "below": 'traces',
                "opacity": base_map_opacity,
                "sourcetype": "raster",
                "sourceattribution": "United States Geological Survey",
                "source": [
                    "https://basemap.nationalmap.gov/arcgis/rest/services/USGSImageryOnly/MapServer/tile/{z}/{y}/{x}"
                ]
            },
            {
                "sourcetype": "raster",
                "opacity": base_map_opacity,
                "sourceattribution": "Government of Canada",
                "source": ["https://geo.weather.gc.ca/geomet/?"
                           "SERVICE=WMS&VERSION=1.3.0&REQUEST=GetMap&BBOX={bbox-epsg-3857}&CRS=EPSG:3857"
                           "&WIDTH=1000&HEIGHT=1000&LAYERS=RADAR_1KM_RDBR&TILED=true&FORMAT=image/png"],
            }
            
          ])
    all_sites_map.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    
    
    plotly.offline.plot(all_sites_map, filename=r"W:\STS\hydro\GAUGE\Temp\Ian's Temp\Site Assignments_"+str(date.today())+"_site_map.html")
    webbrowser.open_new(r"W:\STS\hydro\GAUGE\Temp\Ian's Temp\Site Assignments_"+str(date.today())+"_site_map.html")

all_sites_map()