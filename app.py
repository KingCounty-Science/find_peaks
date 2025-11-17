import dash
from dash import dcc, html, Input, Output, State, ctx
import dash_ag_grid as dag
import pandas as pd
import plotly.express as px
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks, peak_widths
import dash_daq as daq
import plotly.express as px
import plotly.graph_objects as go
import warnings
from dash import ctx  # Import ctx for triggered_id
from dash import Dash, dcc, html, dash_table, Input, Output, State, callback

import base64
import datetime
import io
import gunicorn
import pandas as pd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__, external_stylesheets=external_stylesheets)
warnings.simplefilter(action='ignore', category=FutureWarning)
# Sample DataFrame
#df = pd.read_csv(r"data/test_data/waterlevel_test.csv", parse_dates=[0])

#df['initial'] = 

# Initialize the Dash app

#app = dash.Dash(__name__)
server = app.server  # This is important for Render

app.layout = html.Div([
    html.H1("Find Peaks, Dips and Offsets Editor"),
    
  
    html.Div([
        html.Label("Import data or use test data (datetime, data)"),
        dcc.Upload(id='upload-data',children=html.Div(['Drag and Drop or ',html.A('Select Files')]),),
        dcc.Markdown( "data download"),
        html.Button("Download CSV", id="csv-button", n_clicks=0),
            ], style={'display': 'flex', 'gap': '10px', 'border': '2px solid black', 'padding': '10px', 'border-radius': '5px', 'align-items': 'center', 'backgroundColor': 'lightblue' }),
        # find peaks selector within find peaks
        html.Div([
            html.Div(style={'border-left': '2px solid #ccc', 'height': '100%', 'margin': '0 15px'}),  # Vertical divider
            html.Label("find_peaks"),
            daq.BooleanSwitch(id='find_peaks_btn', on=True),
            html.Div([
            html.Label("peaks vs dips"),
            daq.BooleanSwitch(id='compute_dips', on=False),
            html.Label("Select Area Under Peaks"),
            daq.BooleanSwitch(id='select_area_under_peaks', on=True),
            html.Button('Select/Re-Select Peaks', id='re_select_peaks_btn', n_clicks=0),
    ], id='peak-controls-div', style={'display': 'none'}),  # Initially hidden
        #html.Div(id='boolean-switch-result')
            ], style={'display': 'flex', 'gap': '10px', 'border': '2px solid black', 'padding': '10px', 'border-radius': '5px', 'align-items': 'center'}),
    ### tabs
    
    
    
   
    # variables in columns
    html.Div([
        # peak distance column
        html.Div([
            html.Label("peak distance:"),
            dcc.Input(id='peak_distance', type='number', min=0, max=100, step=0.01, value = 0),
            html.Label("distance between peaks"),
        ], style={'display': 'flex', 'flex-direction': 'column', 'gap': '5px'}),

        html.Div(style={'border-left': '2px solid #ccc', 'align-self': 'stretch', 'margin': '0 15px'}),  # Vertical divider
        # peak height column
        html.Div([
            html.Label("peak height (min/max):"),
            dcc.Input(id='height_min', type='number', min=0, max=100, step=0.01, value = 0),
            dcc.Input(id='height_max', type='number', min=0, max=100, step=0.01, value = 0),
        ], style={'display': 'flex', 'flex-direction': 'column', 'gap': '5px'}),

        html.Div(style={'border-left': '2px solid #ccc', 'align-self': 'stretch', 'margin': '0 15px'}),  # Vertical divider
        # width column
        html.Div([
            html.Label("width (min/max):"),
            dcc.Input(id='width_min', type='number', min=0, max=100, step=0.01, value = 0),
            dcc.Input(id='width_max', type='number', min=0, max=100, step=0.01, value = 0),
        ], style={'display': 'flex', 'flex-direction': 'column', 'gap': '5px'}),

        html.Div(style={'border-left': '2px solid #ccc', 'align-self': 'stretch', 'margin': '0 15px'}),  # Vertical divider
        # relative height column
        html.Div([
            html.Label("relative height (Precent as 0-1):"),
            dcc.Input(id='rel_height', type='number', min=0, max=1, step=0.01, value = .8),
            html.Label("% height used to find peak base"),
        ], style={'display': 'flex', 'flex-direction': 'column', 'gap': '5px'}),

        html.Div(style={'border-left': '2px solid #ccc', 'align-self': 'stretch', 'margin': '0 15px'}),  # Vertical divider
        # prominence column
        html.Div([
            html.Label("prominence (min/max):"),
            dcc.Input(id='prominence_min', type='number', min=0, max=100, step=0.01, value = 0),
            dcc.Input(id='prominence_max', type='number', min=0, max=100, step=0.01, value = 0),
        ], style={'display': 'flex', 'flex-direction': 'column', 'gap': '5px'}),

        html.Div(style={'border-left': '2px solid #ccc', 'align-self': 'stretch', 'margin': '0 15px'}),  # Vertical divider
        # wlen column
        html.Div([
            html.Label(" wlen: "),
            dcc.Input(id='wlen', type='number', min=0, max=100, step=0.01, value = 0),
            html.Label("window size"),
        ], style={'display': 'flex', 'flex-direction': 'column', 'gap': '5px'}),

        html.Div(style={'border-left': '2px solid #ccc', 'align-self': 'stretch', 'margin': '0 15px'}),  # Vertical divider
        # threshold column
        html.Div([
            html.Label("threshold (min/max):"),
            dcc.Input(id='threshold_min', type='number', min=0, max=100, step=0.01, value=0, placeholder='min'),
            dcc.Input(id='threshold_max', type='number', min=0, max=100, step=0.01, value=0, placeholder='max'),
        ], style={'display': 'flex', 'flex-direction': 'column', 'gap': '5px'}),
        
        html.Div(style={'border-left': '2px solid #ccc', 'align-self': 'stretch', 'margin': '0 15px'}),  # Vertical divider
        # plateau column
        html.Div([
            html.Label("plateau (min/max):"),
            dcc.Input(id='plateau_min', type='number', min=0, max=100, step=0.01, value=0, placeholder='min'),
            dcc.Input(id='plateau_max', type='number', min=0, max=100, step=0.01, value=0, placeholder='max'),
            ], style={'display': 'flex', 'flex-direction': 'column', 'gap': '5px'}),
    ], id='peak-parameters-div', style={'display': 'none'}),
        
     html.Div([
        html.Label("selection"),
    
        #html.Button('Select Area Under Peaks', id='select_area_under_peaks_btn', n_clicks=0),  # Clear button
        #daq.BooleanSwitch(id='select_all_peaks', on=False),
        html.Button('clear selection', id='clear_selection', n_clicks=0),  # Clear button
        html.Button('remove prominence', id='remove_prominence', n_clicks=0),  # Clear button
        html.Label("Fill Selection with Value:"),
        dcc.Input(id='fill_selection_value', type='number', step=0.01),  # Numeric input
        html.Button('Fill Selection', id='fill_selection_button', n_clicks=0),
        
        html.Button('null_selection', id='null_selection_button', n_clicks=0),
        html.Button('delete_selection', id='delete_selection_button', n_clicks=0),
            ], style={'display': 'flex', 'gap': '10px', 'border': '2px solid black', 'padding': '10px', 'border-radius': '5px', 'align-items': 'center'}),

    html.Div([
        html.Label("interpolation"),
        html.Label("direction: "),
        dcc.Dropdown(id="interpolation_direction",
        options=[{"label": "Forward", "value": "forward"},{"label": "Backward", "value": "backward"},{"label": "Both", "value": "both"}],
        value="both", clearable=False,style={"width": "200px"}),
        html.Button('run interpolation', id='run_interoplation', n_clicks=0),
        
            ], style={'display': 'flex', 'gap': '10px', 'border': '2px solid black', 'padding': '10px', 'border-radius': '5px', 'align-items': 'center'}),
    
     html.Div([
        html.Label("offset (if blank offset will use first selection value)"),
        html.Label("initial selection offset (row will equal this) :"),
        dcc.Input(id='offset_value_a', type='number', step=0.01),  # Numeric input
        html.Label("final selection offset (row will equal this):"),
        dcc.Input(id='offset_value_b', type='number', step=0.01),  # Numeric input
        html.Button('run offset', id='run_offset_button', n_clicks=0),


            ], style={'display': 'flex', 'gap': '10px', 'border': '2px solid black', 'padding': '10px', 'border-radius': '5px', 'align-items': 'center'}),
    html.Div([dcc.Graph(id="line-graph")]),
    dag.AgGrid(
        id="data-grid",
        #rowData=df.to_dict("records"),
        #columnDefs=[{"field": col, "editable": True} for col in df.columns],
        defaultColDef={"editable": True, "resizable": True, "sortable": True},
        dashGridOptions={
                "undoRedoCellEditing": True,
                "undoRedoCellEditingLimit": 20,
                "editType": "fullRow",
                "animateRows": False,
                "suppressScrollOnNewData": True,
                #"rowSelection": "multiple",  # Allow row selection
            },
    
    ),
    
])
# control visability of peak controsl
@app.callback(
    Output('peak-controls-div', 'style'),  # controls "select area under peaks" etc
    Output('peak-parameters-div', 'style'), # controls peak height etc
    Input('find_peaks_btn', 'on')
)
def toggle_peak_controls(find_peaks_btn):
    if find_peaks_btn is True:
        controls_style = {'display': 'flex', 'gap': '10px', 'border': '2px solid black', 
                'padding': '10px', 'border-radius': '5px', 'align-items': 'center'}

        parameters_style =  {'display': 'flex', 'gap': '10px', 'border': '2px solid black', 
                'padding': '10px', 'border-radius': '5px', 'align-items': 'center',
                'justify-content': 'center', 'margin': '0 auto'}, 
        return {'display': 'flex', 'gap': '10px', 'border': '2px solid black', 
                'padding': '10px', 'border-radius': '5px', 'align-items': 'center'}, {'display': 'flex', 'gap': '10px', 'border': '2px solid black', 
                'padding': '10px', 'border-radius': '5px', 'align-items': 'center',
                'justify-content': 'center', 'margin': '0 auto'}
    else:
        # Hide the div
        return {'display': 'none'}, {'display': 'none'}

@app.callback(
    Output("peak_distance", "max"),
    Input("data-grid", "rowData"), 
)
def distance(rows):
    return len(rows)

@app.callback(
    Output("height_min", "max"),
    Output("height_max", "max"),
    Input("data-grid", "rowData"), 
)
def heights(rows):
    # returns the maximimum allowed value based on data max
    if rows:
        df = pd.DataFrame(rows)
        min_value = df.iloc[:, 1].min()  # Assuming column 1 is your signal
        max_value = df.iloc[:, 1].max()  # Assuming column 1 is your signal
        return max_value, max_value
    return 0, 100  # Default fallback

@app.callback(
    Output("width_min", "max"),
    Output("width_max", "max"),
    Output("rel_height", "max"),
    Input("data-grid", "rowData"), 
)
def widths(rows):
    return len(rows), len(rows), len(rows)

@app.callback(
    Output("prominence_min", "max"),
    Output("prominence_max", "max"),
    Output("wlen", "max"),
    Input("data-grid", "rowData"), 
)
def widths(rows):
    return len(rows), len(rows), len(rows)


@app.callback(
    Output("threshold_min", "max"),
    Output("threshold_max", "max"),
    Input("data-grid", "rowData"), 
)
def heights(rows):
    return len(rows), len(rows)


@app.callback(
    Output("plateau_min", "max"),
    Output("plateau_max", "max"),
    Input("data-grid", "rowData"), 
)
def heights(rows):
    return len(rows), len(rows)


@app.callback(
    [Output("data-grid", "rowData"), 
    Output("data-grid", "columnDefs")],
    Input("data-grid", "rowData"),
    Input("line-graph", "selectedData"),# Capture lasso selection
    Input('find_peaks_btn', 'on'),
    Input("peak_distance", "value"),
    Input("height_min", "value"),
    Input("height_max", "value"),
    Input("width_min", "value"),
    Input("width_max", "value"),
    Input('rel_height', "value"),
    Input("prominence_min", "value"),
    Input("prominence_max", "value"),
    Input("wlen", "value"),
    Input("threshold_min", "value"),
    Input("threshold_max", "value"),
    Input("plateau_min", "value"),
    Input("plateau_max", "value"),
    Input('compute_dips', 'on'),
    Input("data-grid", "cellValueChanged"),  
    Input('re_select_peaks_btn', 'n_clicks'),
    Input('select_area_under_peaks', 'on'),
    Input('clear_selection', 'n_clicks'),  # Trigger when the button is clicked
    Input('fill_selection_value', 'value'),  # Clear button
    Input('fill_selection_button', 'n_clicks'),  # Clear button
    Input('remove_prominence', 'n_clicks'),  # Clear button
    Input('upload-data', 'contents'),
    State('upload-data', 'filename'),
    Input("null_selection_button", "n_clicks"),
    Input("delete_selection_button", "n_clicks"),
    State('interpolation_direction', 'value'),
    Input("run_interoplation", "n_clicks"),
    State('offset_value_a', 'value'),
    State('offset_value_b', 'value'),
    Input('run_offset_button', "n_clicks"),
)

def update_grid_data(rows, graph_selection, find_peaks_btn, peak_distance, height_min, height_max, width_min, width_max, rel_height, prominence_min, prominence_max, wlen, threshold_min, threshold_max, plateau_min, plateau_max, compute_dips, event, re_select_peaks_btn, select_area_under_peaks, clear_selection, fill_selection_value, fill_selection_button, remove_prominence, upload_data_contents, upload_data_filename, null_selection_button, delete_selection_button, interpolation_direction, run_interpolation, offset_value_a, offset_value_b, run_offset_button):
    triggered_id = ctx.triggered_id
    
    if not rows or triggered_id == 'upload-data':
        if upload_data_contents or triggered_id == 'upload-data': # if there is data to upload
            content_type, content_string = upload_data_contents.split(',')
            decoded = base64.b64decode(content_string)
    
            try:
                if upload_data_filename.endswith('.csv'):
                    df = pd.read_csv(io.StringIO(decoded.decode('utf-8')), names=["datetime", "data"],  parse_dates=["datetime"], header=0, usecols = [0,1])
                    df['selection'] = False
                    df['initial_data'] = df['data']
                elif upload_data_filename.endswith('.xlsx'):
                    df = pd.read_excel(io.StringIO(decoded.decode('utf-8')), names=["datetime", "data"],  parse_dates=["datetime"], header=0, usecols = [0,1])
                    df['selection'] = False
                    df['initial_data'] = df['data']
            except Exception as e:
                print(e)
                return dash.no_update
        else:
            df = pd.read_csv(r"data/test_data/waterlevel_test.csv", names=["datetime", "data"], parse_dates=["datetime"], header=0)

            df['selection'] = False
            df['initial_data'] = df['data']
    
    else:
        
        df = pd.DataFrame(rows)
        
    # Get triggered_id
    if graph_selection and "points" in graph_selection:
        
        # Extract indices from selection
        selected_indices = [point["pointIndex"] for point in graph_selection["points"]]
        
        df.loc[df.index.isin(selected_indices), "selection"] = True

    #if select_all_peaks is True and find_peaks_btn is True:
    #        #df["selection"] = False
    #       df.loc[~df["peaks"].isna(), "selection"] = True
        
    if triggered_id == 'clear_selection':# and clear_selection > 0:
        df["selection"] = False

    if triggered_id == 'fill_selection_button' and fill_selection_value is not None:
            df.loc[df["selection"] == True, "data"] = fill_selection_value
            df["selection"] = False
    if triggered_id == 'null_selection_button':
            df.loc[df["selection"] == True, "data"] = np.nan

    if triggered_id == 'delete_selection_button':
            df.loc[df["selection"] == True, "datetime"] = np.nan
            df.dropna(subset = "datetime", inplace=True)
            #df["selection"] = False

    if triggered_id == 'run_interoplation':
            mask = df["selection"] == True  # Boolean mask
            #df.loc[mask, "data"] = df.loc[mask, "data"].interpolate(method='linear', direction=interpolation_direction)
            df["data"] = df["data"].interpolate(method='linear', direction=interpolation_direction)
            df["data"] = df['data'].round(2)

    if triggered_id == 'run_offset_button':
        
        # Boolean mask
        mask = df["selection"] == True  

        # Filter DataFrame based on the mask
        filtered_df = df[mask].copy()
        if not filtered_df.empty:
            # Initialize 'offset' with NaNs
            filtered_df["offset"] = np.nan
            
            # Set first and last values of 'offset'
            first_idx = filtered_df.index[0]
            last_idx = filtered_df.index[-1]
            print("offset a ", offset_value_a, " offset b ", offset_value_b)
            # if offset value is given use that, otherwise use first selection value
            #if offset_value_a is None and offset_value_b is None:
            #    print("first")
            #    filtered_df.loc[first_idx, "offset"] = df.loc[first_idx, "data"]
            #    filtered_df.loc[last_idx, "offset"] = df.loc[last_idx, "data"]
                
                #filtered_df["offset"] = filtered_df['data'] - filtered_df["offset"]
            #    filtered_df["offset"] = filtered_df["offset"].interpolate(method='linear', direction="both")
            #    filtered_df["offset"] = filtered_df["data"] - filtered_df["offset"]
            #    filtered_df["data"] = round(filtered_df["data"] - filtered_df["offset"], 2)
            #    df.loc[filtered_df.index, ["data"]] = filtered_df[["data"]]
            if offset_value_a is None:
                filtered_df.loc[first_idx, "offset"] = df.loc[first_idx, "data"]
                print("blank offset a", offset_value_a)
            else:
                filtered_df.loc[first_idx, "offset"] = offset_value_a
                print("offset a value", offset_value_a)
                
            if offset_value_b is None:
                filtered_df.loc[last_idx, "offset"] = df.loc[last_idx, "data"]
                print("blank offset b", offset_value_b)
            else:
                filtered_df.loc[last_idx, "offset"] = offset_value_b
                print("offset b value", offset_value_b)
            filtered_df.loc[~filtered_df["offset"].isna(), "offset"] = filtered_df.loc[~filtered_df["offset"].isna(), "data"] - filtered_df.loc[~filtered_df["offset"].isna(), "offset"]
            print("offset calc")
            print(filtered_df)
            print("offset pre fill")
            print(filtered_df)
            filtered_df["offset"] = filtered_df["offset"].interpolate(method='linear', direction="both")
            filtered_df["offset"] = filtered_df["offset"].ffill()
            filtered_df["offset"] = filtered_df["offset"].bfill()
            print("offset fill")
            print(filtered_df)
                #if offset_value_a and offset_value_b:
                #    filtered_df.loc[first_idx, "offset"] = df.loc[first_idx, "data"] - offset_value_a
                #    print(filtered_df)
                #    filtered_df.loc[last_idx, "offset"] = df.loc[last_idx, "data"] - offset_value_b
                #    print(filtered_df)
                #    filtered_df["offset"] = filtered_df["offset"].interpolate(method='linear', direction="both")
                #    print(filtered_df)
                #elif offset_value_a and not offset_value_b:
                #     filtered_df.loc[first_idx, "offset"] = df.loc[first_idx, "data"] - offset_value_a
                #     
                #     filtered_df["offset"] = filtered_df["offset"].bfill()
                #elif offset_value_b and not offset_value_a:
                #     filtered_df.loc[last_idx, "offset"] = df.loc[last_idx, "data"] - offset_value_b
                #     filtered_df["offset"] = filtered_df["offset"].ffill()
            filtered_df["data"] = round(filtered_df["data"] - filtered_df["offset"], 2)
            df.loc[filtered_df.index, ["data"]] = filtered_df[["data"]]
            #if offset_value_a:
                #    filtered_df.loc[first_idx, "offset"] = df.loc[first_idx, "data"] - offset_value_a
                #else:
                #    
                #if offset_value_b:
                #    filtered_df.loc[last_idx, "offset"] = df.loc[last_idx, "data"] - offset_value_b
                #else:
                    
            # Interpolate missing values in 'offset'
            #filtered_df["offset"] = filtered_df["offset"].interpolate(method='linear', direction="both")

            # Adjust 'data' column
            #filtered_df["data"] = filtered_df["data"] - filtered_df["offset"]

            # Assign the updated values back to the original DataFrame
            #df.loc[filtered_df.index, ["data", "offset"]] = filtered_df[["data", "offset"]]

    if triggered_id == 'remove_prominence' and remove_prominence > 0 and find_peaks_btn is True:
            if compute_dips is False:
                df.loc[df["selection"] == True, "data"] -= round(((df["left_thresholds"] + df["right_thresholds"]) / 2), 2)
            if compute_dips is True:
                #df.loc[df["selection"] == True, "air_temperature"] += round(((df["left_thresholds"] + df["right_thresholds"]) / 2), 2)
                df.loc[df["selection"] == True, "data"] += df['prominences']
            df["selection"] = False
    
    if find_peaks_btn is True or triggered_id == 're_select_peaks_btn':  # button turns blue when false so lets go with this though it doesnt make any sense
        print("run find peaks")
        #df["selection"] = False # cleaR SELECTION
            # Extract data
        x = df.iloc[:, 0]  # Datetime column
        x = df["datetime"]
        y = df.iloc[:, 1]  # Measurement column
        
        if compute_dips is False:
                y = df["data"]
        if compute_dips is True:
                y = -(df["data"])



        # Find peaks
        peak_distance = None if peak_distance < .01 else peak_distance
        # convert to .1 decimal
        height_min = None if height_min < .01 else height_min 
        height_max = None if height_max < .01 else height_max

        if compute_dips is True:
                if height_min != None:
                    height_min = -height_min
                if height_max != None:
                    height_max = -height_max
        
        # width_min = None if width_min < .01 else width_min    
        width_max = None if width_max < .01 else width_max
        width_min = None if width_min < .01 else width_min  
            
        if rel_height < .01:
                rel_height = None
                
        #prominence_min = None if prominence_min < .01 else prominence_min
        #prominence_max = None if prominence_max < .01 else prominence_max
        prominence_min = None if (prominence_min is not None and prominence_min < 0.01) else prominence_min
        prominence_max = None if (prominence_max is not None and prominence_max < 0.01) else prominence_max
        # wlen is the prominence window size so it has to be none if there is no prominace window
        if (prominence_min is None or prominence_max is None) and wlen < 0.01:
            wlen = None
    
        #ddd 
        threshold_min = None if threshold_min < .01 else threshold_min
        threshold_max = None if threshold_max < .01 else threshold_max

        plateau_min = None if plateau_min < .01 else plateau_min
        plateau_max = None if plateau_max < .01 else plateau_max
        
        
        params = {
            'distance': peak_distance,
            'height': (height_min, height_max),
            'width': (width_min, width_max),
            'rel_height': (rel_height),
            'prominence': (prominence_min, prominence_max),
            'wlen': (wlen),
            'threshold': (threshold_min, threshold_max), 
            'plateau_size': (plateau_min, plateau_min)
       
            }
        
        # Filter out None values or completely unused ones
        filtered_params = {k: v for k, v in params.items() if v is not None}

            # Call find_peaks with only the active parameters
        peaks, peak_properties = find_peaks(y, **filtered_params)


        # peak widths
       
        #peak_widths(x, peaks, rel_height=0.5, prominence_data=None, wlen=None)
        
        height = peak_properties['peak_heights'] # index value of right base
        right_thresholds = peak_properties['right_thresholds'] # round this at the end
        left_thresholds = peak_properties['left_thresholds'] # round this at the end
        widths = peak_properties['widths'] # index value of right base
        #prominence = np.round(peak_properties['prominences'], 5) # height: I think its peak-right base
        prominences = peak_properties['prominences'] # round this at the end
            
        left_ips = peak_properties["left_ips"]
        left_ips = left_ips.round(0).astype(int)
        
        right_ips = peak_properties["right_ips"]
        right_ips = right_ips.round(0).astype(int)
       
        df["peaks"] = np.nan
        #df["height"] = np.nan
        #df["left_thresholds"] = np.nan
        #df["right_thresholds"] = np.nan
        #df["widths"] = np.nan
        #df["prominences"] = np.nan
        #df["left_ips"] = np.nan
        #df["right_ips"] = np.nan
            
            
        df.loc[peaks, "peaks"] = df.iloc[peaks, 1]  # Store peak values
        #df.loc[peaks, 'height'] = np.round(height, 2) # store peak prominence on peak row
        #df.loc[peaks, 'widths'] = np.round(widths, 2) 
        # store peak prominence on peak row
        #df.loc[peaks, 'left_thresholds'] = np.round(left_thresholds, 2) # store peak prominence on peak row
        #df.loc[peaks, 'right_thresholds'] = np.round(right_thresholds, 2) # store peak prominence on peak row

        #df.loc[peaks, 'prominences'] = np.round(prominences, 2) # store peak prominence on peak row
        

        df["selection"] = False
        df.loc[peaks, "selection"] = True
        if select_area_under_peaks is True: 
            for left_ip, right_ip in zip(left_ips, right_ips):
                start = max(0, left_ip)
                end = min(len(df), right_ip + 1)
                df.iloc[start:end, df.columns.get_loc("selection")] = True
        
    
    desired_order = ["datetime", "data", "initial_data", "selection"]
    df = df[[col for col in desired_order if col in df.columns]].copy()
        
    return df.to_dict("records"), [{"field": col, "editable": True} for col in df.columns]


@app.callback(
    Output("data-grid", "scrollTo"),
    Input("line-graph", "clickData"),
    State('data-grid', 'cellValueChanged'), 
    
)
def scroll_to_row_and_col(clickData,cellValueChanged):
    if clickData is None:
        return dash.no_update


    elif clickData['points'][0]['pointIndex'] != 0:
            point_index = clickData['points'][0]['pointIndex']
            #print("new graph point selected")
            # return data and clears fill selection
            return {"rowIndex": point_index, "column": None, "rowPosition": "middle"}
    
    
    else:
        return dash.no_update


@app.callback(
    Output("line-graph", "figure"),
    Input("data-grid", "rowData")
)
def update_graph(rows):
    if rows:
        df_updated = pd.DataFrame(rows)
        #fig = px.line(df_updated, x="datetime", y="data", markers=False, title="Updated Line Graph")
        fig = px.line(df_updated, x="datetime", y="data", title="Updated Line Graph")
        fig.add_trace(go.Scatter(x=df_updated["datetime"], y=df_updated['initial_data'], mode='lines', name='initial data', line=dict(color='grey')))
        if "peaks" in df_updated.columns:
            fig.add_scatter(x=df_updated["datetime"], y=df_updated["peaks"], mode="markers", marker=dict(color="deepskyblue", size=8), name="Peaks")
        #fig.add_scatter(x=df_updated["datetime"], y=df_updated["right_bases"], mode="markers", marker=dict(color="green", size=8), name="right bases")
        
        if "selection" in df_updated.columns:
            #df_updated["selection"] = df_updated["selection"].astype(bool)
            df_updated = df_updated.loc[df_updated["selection"] == True]
            
            fig.add_scatter(x=df_updated["datetime"], y=df_updated["data"], mode="markers", marker=dict(color="red", size=8), name="Peaks")
            #fig.add_trace(go.Scatter(x=df_updated["datetime"], y=df_updated["air_temperature"], mode='lines', line=dict(color='deepskyblue', width=4),))
            fig.update_layout(uirevision='constant') 
        df_updated = pd.DataFrame(rows)
        fig.add_scatter(x=df_updated["datetime"], y=df_updated["data"], mode="markers", marker=dict(color="deepskyblue", size=0, opacity=0), name="Peaks", showlegend=False)
        return fig
    else:
        return dash.no_update
    

@callback(
    Output("data-grid", "exportDataAsCsv"),
    Output("data-grid", "csvExportParams"),
    Input("csv-button", "n_clicks"),
    State('upload-data', 'filename'),
    State("data-grid", "rowData"),
    
)
def export_data_as_csv(n_clicks, filename, rows):
    if n_clicks:
        df = pd.DataFrame(rows)
        desired_order = ["datetime", "data", "initial_data", "selection"]
        df = df[[col for col in desired_order if col in df.columns]].copy()
        #df["datetime"] = df["datetime"].dt.strftime("%Y-%m-%d %H:%M:%S")
        df["datetime"] = pd.to_datetime(df["datetime"]).dt.strftime("%Y-%m-%d %H:%M:%S")
        df.to_csv(r"W:\STS\hydro\GAUGE\Temp\Ian's Temp\edited.csv", index = False)
        if filename:
             filename = filename.split('.')[0]
        else:
             filename = "test_data"
        return True, {"fileName": f"{filename}_edited.csv"}

    return False,  {"fileName": "ag_grid_test.csv"}
# Run the app
if __name__ == "__main__":
    #app.run_server(debug=True)
    app.run(debug=False)
    #app.run_server(debug=True, host="0.0.0.0", port=8051)
