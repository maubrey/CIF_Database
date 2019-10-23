# -*- coding: utf-8 -*-
#! C:\PROGRA~2\CCDC\PYTHON~2\MINICO~1\

#local imports
import structure_database

import json, os
from dash import Dash
import dash_core_components as dcc
import dash_html_components as html
from dash_table import DataTable
from pandas.io.json import json_normalize
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
from dash.exceptions import PreventUpdate






external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = Dash(__name__, external_stylesheets=external_stylesheets)
colors={
    'background': '#fff',
    'text': '#333'
}


#######################
# import the raw data #
#######################
with open('./database_files/inhouse.json', 'r') as filehandle:
    data = filehandle.read()
data = json.loads(data)
df = json_normalize(data)

with open('./database_files/search_results.json', 'r') as filehandle:
    data2 = filehandle.read()
data2 = json.loads(data2)
reduced_cell_df = json_normalize(data2)

common_names = {
    '_cell_length_a': 'a',
    '_cell_length_b': 'b',
    '_cell_length_c': 'c',
    '_cell_angle_alpha': 'alpha', 
    '_cell_angle_beta':  'beta',
    '_cell_angle_gamma':  'gamma',
    '_symmetry_cell_setting': 'Bravais',
    '_symmetry_space_group_name_H-M': 'Space Group',
    '_diffrn_ambient_temperature': 'Temperature',
    '_cell_formula_units_Z':'Z',
    '_audit_creation_date':'Date Created',
    '_cell_volume': 'Volume'
}


#name the app
if 'DYNO' in os.environ:
    app_name = os.environ['DASH_APP_NAME']
else:
    app_name = 'dash-tableplot'



app.layout = html.Div(style={'backgroundColor':colors['background'], }, children=[
    html.H1(children='Karunadasa Group Structures',
            style={
                'textAlign':'center',
                'color': colors['text']
            }),

    html.Div(children='''All solved structures, published and unpublished''',
            style={
                'textAlign':'center',
                'color': colors['text']
            }),
    dcc.Markdown(children='''
    ## Instructions
    1. The multiselect box has most useful properties from the cif files. The CSD populates certain properties that Olex does not and visa versa. If something is missing search the list of properties for something similar
    2. Every row was generated from a cif file. If there are multiple entries that look similar check the `hash` property to confirm. If they are not identical then they are unique and you may want to take a closer look at both
    3. If you need to get a cif file, its filepath can be found in the `path` property
    4. you can search and filter using the [syntax shown here](https://dash.plot.ly/datatable/filtering). 
    
    '''),


    dcc.Markdown(style={'paddingTop': 4},children='''
    
    ---

    ## Reduced Cell Search
    Enter cell parameters and lattice-centring and hit submit. Matches will be printed below.

    ###### lattice parameters
    '''),

    dcc.Input(
        id = 'user_input_a',
        placeholder='a-length...',
        type='text',
        value=''
    ),

    dcc.Input(
        id = 'user_input_b',
        placeholder='b-length...',
        type='text',
        value=''
    ),

    dcc.Input(
        id = 'user_input_c',
        placeholder='c-length...',
        type='text',
        value=''
    ),

    dcc.Input(
        id = 'user_input_alpha',
        placeholder='alpha...',
        type='text',
        value=''
    ),

    dcc.Input(
    id = 'user_input_beta',
        placeholder='beta...',
        type='text',
        value=''
    ),

    dcc.Input(
        id = 'user_input_gamma',
        placeholder='gamma...',
        type='text',
        value=''
    ),

    html.Div(className="row", children=[
        html.H6('length tolerance (%)'), 
        dcc.Input(
            id = 'user_input_length_tol',
            placeholder='1.5',
            type='text',
            value=1.5
        ),
        html.H6('angle tolerance (°)'), 
        dcc.Input(
            id = 'user_input_angl_tol',
            placeholder='1.0',
            type='text',
            value=1.0
        ),
    ]),


    dcc.Markdown('''###### lattice centering:'''),
    dcc.Dropdown(
        id = 'user_input_centring',
        options=[
            {'label': 'primitive', 'value': 'primitive'},
            {'label': 'C-centred', 'value': 'C-centred'},
            {'label': 'F-centred', 'value': 'F-centred'},
            {'label': 'I-centred', 'value': 'I-centred'},
            {'label': 'R-obverse', 'value': 'R-obverse'},
            {'label': '?', 'value': 'unknown centring'},
            {'label': 'B-centred', 'value': 'B-centred'},
            {'label': 'A-centred', 'value': 'A-centred'}
        ],
        value='primitive',
        style={'width':200}
    ),  

    html.Div(style={'paddingTop':0}, className='row',
    children=html.Button('Search', id='reduced_cell_button', ),),

    DataTable(
        id='datatable_interactivity_reduced_cell',
        columns= [ {"name": i[0], "id": i[1], "deletable": True, "selectable": False} for i in [[common_names[j], j] if j in common_names.keys() else [j,j] for j in ['parent', '_cell_length_a',
                                                                                                                                                                    '_cell_length_b',
                                                                                                                                                                    '_cell_length_c',
                                                                                                                                                                    '_cell_angle_alpha',
                                                                                                                                                                    '_cell_angle_beta',
                                                                                                                                                                    '_cell_angle_gamma',
                                                                                                                                                                    '_symmetry_cell_setting',
                                                                                                                                                                    '_symmetry_space_group_name_H-M',
                                                                                                                                                                    '_audit_creation_date',
                                                                                                                                                                    '_cell_volume','hash', 'path']]],
        data= reduced_cell_df.to_dict('records'),
        editable=False,
        filter_action="native",
        sort_action="native",
        sort_mode="multi",
        column_selectable="single",
        # row_selectable="multi",
        row_deletable=False,
        selected_columns=[],
        selected_rows=[],
        page_action="native",
        page_current= 0,
        page_size= 100,
        export_format='csv',
        fill_width=False,
        style_cell={
        # all three widths are needed
        'minWidth': '100px', 'width': '100px', 'maxWidth': '400px',
        'overflow': 'hidden',
        'textOverflow': 'ellipsis',
    }
        
       
    ),

    html.Div(style={'paddingTop':50}, className='row',
    children=[dcc.Markdown(''' 
                    ---

                    ## Complete Structure Database

                    
                    '''),
        html.Button('Update cif Database', id='button')]),

    html.Div(id='output-container-button',
             children='Enter a value and press submit'),

    dcc.Dropdown(id='column-selected',multi=True, value=['parent', '_symmetry_space_group_name_H-M', '_cell_length_a', '_cell_length_b', '_cell_length_c'],
                        options=[{"label": i[0], 'value': i[1]} for i in [[common_names[j], j] if j in common_names.keys() else [j,j] for j in df.columns]],
                        style={"display": "block", "margin-left": "auto", "margin-right": "auto", "width": "100%", "padding": 0, 'height':'auto'}, className="row", ),

    # html.Div([dcc.Graph(id="my-graph")],  style={"padding": 0}, className="row"),
    
    DataTable(
        id='datatable-interactivity',
        columns=[ {"name": i, "id": i, "deletable": True, "selectable": False} for i in df.columns], 
        data=df.to_dict('records'),
        editable=False,
        filter_action="native",
        sort_action="native",
        sort_mode="multi",
        column_selectable="single",
        # row_selectable="multi",
        row_deletable=False,
        selected_columns=[],
        selected_rows=[],
        page_action="native",
        page_current= 0,
        page_size= 100,
        export_format='csv',
        fill_width=False,
       
    ),
    
])

    

@app.callback(
    Output('output-container-button', 'children'),
    [Input('button', 'n_clicks')])
def update_output(n_clicks):
    if n_clicks is None:
        raise PreventUpdate
    else:

        # cifs = structure_database.get_all_cifs()
        # data = structure_database.parse_cifs(cifs)
        # clean_data = structure_database.cleanup_parsed_cifs(data)
        before = structure_database.hash_file('./database_files/inhouse.json')
        structure_database.update_databases()
        after = structure_database.hash_file('./database_files/inhouse.json')
        if before == after: 
            return 'No changes made.'
        else:
            with open('./database_files/inhouse.json', 'r') as filehandle:
                data = filehandle.read()
            data = json.loads(data)
            
            df = json_normalize(data)
            return 'Updated {} times! Add a column to update the table.'.format(n_clicks)


@app.callback(
    [Output("datatable-interactivity", "data"),
    Output("datatable-interactivity", "columns")],
    [Input("column-selected", "value"),
    Input('button', 'n_clicks')])
def update_graph(column, n_clicks):
    value_header = []# ['parent', '_symmetry_space_group_name_H-M', '_symmetry_cell_setting']
    value_cell = [df[i] for i in value_header]
    for col in column:
        value_header.append(col)
        value_cell.append(df[col])

    if n_clicks >= 1:
        with open('./database_files/inhouse.json', 'r') as filehandle:
            data = filehandle.read()
        data = json.loads(data)
        df_new = json_normalize(data)[value_header]
        columns_out = [ {"name": i[0], "id": i[1], "deletable": True, "selectable": False} for i in [[common_names[j], j] if j in common_names.keys() else [j,j] for j in df_new.columns]]
        return df_new.to_dict('records'), columns_out
    else:
        df_out=df[value_header]
        columns_out = [ {"name": i[0], "id": i[1], "deletable": True, "selectable": False} for i in [[common_names[j], j] if j in common_names.keys() else [j,j] for j in df_out.columns]]
        return df_out.to_dict('records'), columns_out


@app.callback(
    [Output("datatable_interactivity_reduced_cell", "data"),
    Output("datatable_interactivity_reduced_cell", "columns")],
    [Input('reduced_cell_button', 'n_clicks')],
    [State("user_input_a", "value"),
    State("user_input_b", "value"),
    State("user_input_c", "value"),
    State("user_input_alpha", "value"),
    State("user_input_beta", "value"),
    State("user_input_gamma", "value"),
    State("user_input_centring", "value"), 
    State("user_input_angl_tol", "value"),
    State("user_input_length_tol", "value")])
def update_reduced_cell(n_clicks, a, b, c, alpha, beta, gamma, centring, angle_tol, length_tol):
    if n_clicks is None:
        raise PreventUpdate
    else:
        structure_database.my_reduced_cell_search(float(a), float(b), float(c), float(alpha), float(beta), float(gamma), centring, length_tolerance=length_tol, angle_tolerance=angle_tol)

        value_header = ['parent', '_symmetry_space_group_name_H-M', '_symmetry_cell_setting', '_cell_length_a', '_cell_length_b', '_cell_length_c', '_cell_angle_alpha', '_cell_angle_beta', '_cell_angle_gamma', '_symmetry_cell_setting', '_symmetry_space_group_name_H-M', '_audit_creation_date', '_cell_volume', '_database_code_CSD', 'hash', 'path']
        # try:
        #     value_cell = [reduced_cell_df[i] for i in value_header]
        # except: [reduced_cell_df[i] for i in []]

        with open('./database_files/search_results.json', 'r') as filehandle:
            data2 = filehandle.read()
        data2 = json.loads(data2)
        df_2 = json_normalize(data2)


        columns_out = [ {"name": i[0], "id": i[1], "deletable": True, "selectable": False} for i in [[common_names[j], j] if j in common_names.keys() else [j,j] for j in value_header]]
        return df_2.to_dict('records'), columns_out




if __name__ == '__main__':
    app.run_server(debug=False)