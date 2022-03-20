import dash
from dash import dcc
from dash import html
from dash.dependencies import Output, Input
import dash_daq as daq
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd
import datetime


#Datos (comienzo) ______________________________________________________________________________________________

df = pd.read_csv("aguatratadalasirena.csv")
pd.to_datetime(df['Time'],errors='ignore')
pd.to_datetime(df['Date'],errors='ignore')

df.rename(columns = {'AP03AT9002TEMP':'temperatura', 'AP03AT9002TURB':'turbiedad', 'AP03AT9002CL2':'cloro', 'AP03AT9002PH':'ph'}, inplace = True)
df['ph']=pd.Series([round(val, 2) for val in df['ph']])
df['turbiedad']=pd.Series([round(val, 2) for val in df['turbiedad']])
df['cloro']=pd.Series([round(val, 3) for val in df['cloro']])
df['temperatura']=pd.Series([round(val, 3) for val in df['temperatura']])

dff = df.groupby('Date', as_index=False)[['ph','turbiedad', 'cloro', 'temperatura']].max()

dff_max = df.groupby('Date', as_index=False)[['ph','turbiedad', 'temperatura', 'cloro']].max()
dff2_min = df.groupby('Date', as_index=False)[['ph','turbiedad','temperatura', 'cloro']].min()
dff3_mean = df.groupby('Date', as_index=False)[['ph','turbiedad','temperatura', 'cloro']].mean()
dff4_tail = df.groupby('Date', as_index=False)[['ph','turbiedad','temperatura', 'cloro']].tail(1)



dff_max['Indicador']= 'max'
dff2_min['Indicador']= 'min'
dff3_mean['Indicador']= 'promedio'
dff4_tail['Indicador']='ultimo'
df_max_min = pd.concat([dff_max, dff2_min, dff3_mean])

turbiedad_max = df["turbiedad"].max()
turbiedad_prom = df["turbiedad"].mean()
turbiedad_min = df["turbiedad"].min()
turbiedad_ulti = df["turbiedad"].tail(1)


ph_max = df["ph"].max()
ph_prom = df["ph"].mean()
ph_min = df["ph"].min()
ph_ulti = df["ph"].tail(1)

cloro_max = df["cloro"].max()
cloro_prom = df["cloro"].mean()
cloro_min = df["cloro"].min()
cloro_ulti = df["cloro"].tail(1)

temperatura_max = df["temperatura"].max()
temperatura_prom = df["temperatura"].mean()
temperatura_min = df["temperatura"].min()
temperatura_ulti = df["temperatura"].tail(1)

#datos maximos con graficos

turbiedad_creciente = dff_max.sort_values(by="turbiedad")
ph_creciente = dff_max.sort_values(by="ph")
cloro_creciente = dff_max.sort_values(by="cloro")
temperatura_creciente = dff_max.sort_values(by="temperatura")


#Datos (fin) ______________________________________________________________________________________________

FONT_AWESOME = "https://use.fontawesome.com/releases/v5.10.2/css/all.css"
app = dash.Dash(external_stylesheets=[dbc.themes.CYBORG, FONT_AWESOME])

card_icon = {
    "color": "white",
    "textAlign": "center",
    "fontSize": 20,
    "margin": "auto",
}

card_content1 = [daq.LEDDisplay(
        id='our-LED-display',
        value=6
    ),]
    
card_content = dbc.CardGroup(
    [
        dbc.Card(
            dbc.CardBody(
                ["SOLEDAD",
                ]
            )
        ),
        dbc.Card(
            html.Div(className="fa fa-globe", style=card_icon),
            className="bg-info",
            style={"maxWidth": 90},
        ),
    ],className="mt-4 shadow",
)

card2 = dbc.Card(dbc.Button( id="alerta", className="me-1", n_clicks=0))

card3 = dbc.Card(dbc.Button( id="alerta2", className="me-1", n_clicks=0))

card4 = dbc.Card(dbc.Button( id="alerta3", className="me-1", n_clicks=0))

card5 = dbc.Card(dbc.Button( id="alerta5", className="me-1", n_clicks=0))

card_soledad = dbc.Card(
    [
        dbc.CardImg(src="/assets/ptap.jpg", top=True, bottom=False,
                    title="Image by Kevin Dinkel", alt='Learn Dash Bootstrap Card Component'),
        dbc.CardBody(
            [
                html.P(
                    "PARAMETROS MONITOREADOS.",
                    className="card-text",
                ),
                dcc.Dropdown(
             
        id= 'segundo dropdown',
        options = [
            {'label': 'cloro', 'value': 'cloro'},
            {'label':'turbiedad','value':'turbiedad'},
            {'label':'ph','value':'ph'},
            {'label':'temperatura','value':'temperatura'}    
        ],
        value= 'cloro',
        multi= False
    
             
             ),
                dbc.Button("ALERTA TECNICO", color="primary"),
                dbc.CardLink("PLANTA", href="http://www.sapvirtual.com/joomla30/index.php/centro-de-control-maestro", target="_blank"),
            ]
        ),
    ],
    color="solar",   
    inverse=True,   
    outline=False,  
)

card_soledad2 = dbc.Card(
    [
        dbc.CardImg(src="/assets/ptap2.jpg", top=True, bottom=False,
                    title="Image by Kevin Dinkel", alt='Learn Dash Bootstrap Card Component'),
        dbc.CardBody(
            [
                html.P(
                    "PARAMETROS MONITOREADOS.",
                    className="card-text",
                ),
                dcc.Dropdown(),
                dbc.Button("ALERTA TECNICO", color="primary"),
                dbc.CardLink("PLANTA", href="http://www.sapvirtual.com/joomla30/index.php/centro-de-control-maestro", target="_blank"),
            ]
        ),
    ],
    color="solar",   
    inverse=True,   
    outline=False,  
)



app.layout = html.Div(
    [
        dbc.Row([dbc.Col(dbc.Card("Ultimo DATO")),
                dbc.Col(dbc.Card("MAXIMO")),
                dbc.Col(dbc.Card("PROMEDIO")),
                dbc.Col(dbc.Card("MINIMO"))], className="g-0")
        ,
        
        dbc.Row(
            [
                dbc.Col((card5)), 
                dbc.Col((card2)),
                dbc.Col((card3)), 
                dbc.Col(card4),
            ],className="g-0",)
        ,
        
        dbc.Row(
            [
                dbc.Col(html.Div([card_soledad],style={"width": "18rem"},), width=3,
                        ),
                dbc.Col(html.Div(dbc.Card(dcc.Graph(id = 'my_graph3', figure = {})))),
                dbc.Col(html.Div(dbc.Card([dcc.Graph(id = 'my_graph4', figure = {})],style={"width": "18rem"},)), width=3),
            ],className="g-0",)
        ,
        
        dbc.Row([dbc.Col(dbc.Card(dbc.Button("SIN NOVEDAD", color="success"))),
                dbc.Col(dbc.Card(dbc.Button("BLOQUEAR ENTRADA", color="danger"))),
                dbc.Col(dbc.Card(dbc.Button("TRATAMIENTO", color="warning"))),
                dbc.Col(dbc.Card(dbc.Button("ENVIAR REPORTE", color="primary")))]),
        
        dbc.Row()
        
        ]
)


# PRIMER Callback______________________________________________________________________________________

@app.callback(
    Output('my_graph3', component_property='figure'),
    [Input('segundo dropdown', component_property='value')])

def update_graph(value):
    
    if value == 'cloro':
        fig = px.line(
            data_frame = df,
            x = 'Date',
            y = 'cloro',
            template="plotly_dark")
        fig.update_layout(xaxis=dict(showgrid=False, zeroline=False), yaxis=dict(showgrid=False, zeroline=False))
        fig.update_layout(autosize=False, margin=dict(l=5, r=5, b=5, t=5, pad=4),)
        
    elif value == 'turbiedad':
        fig = px.line(
            data_frame= df,
            x = 'Date',
            y = 'turbiedad',
            template= "plotly_dark")
        fig.update_layout(xaxis=dict(showgrid=False, zeroline=False), yaxis=dict(showgrid=False, zeroline=False))
        fig.update_layout(autosize=False, margin=dict(l=5, r=5, b=5, t=5, pad=4),)
        
    elif value =='temperatura':
        fig = px.line(
            data_frame = df,
            x = 'Date',
            y = 'temperatura',
            template="plotly_dark")
        fig.update_layout(xaxis=dict(showgrid=False, zeroline=False), yaxis=dict(showgrid=False, zeroline=False))
        fig.update_layout(autosize=False, margin=dict(l=5, r=5, b=5, t=5, pad=4),)
    else:
        fig = px.line(
            
            data_frame= df,
            x = 'Date',
            y = 'ph',
            template= "plotly_dark")
        fig.update_layout(xaxis=dict(showgrid=False, zeroline=False), yaxis=dict(showgrid=False, zeroline=False))
        fig.update_layout(autosize=False, margin=dict(l=5, r=5, b=5, t=5, pad=4),)
    return fig

# SEGUNDO Callback______________________________________________________________________________________

@app.callback(
    Output('my_graph4', component_property='figure'),
    [Input('segundo dropdown', component_property='value')])

def update_graph(value):
    
    if value == 'turbiedad':
        fig = px.bar(
            data_frame = turbiedad_creciente,
            x = 'Date',
            y = 'turbiedad',
            template="plotly_dark")
        fig.update_layout(xaxis=dict(showgrid=False, zeroline=False), yaxis=dict(showgrid=False, zeroline=False))
        fig.update_layout(autosize=False, margin=dict(l=5, r=5, b=5, t=5, pad=4),)
    elif value == 'ph':
        fig = px.bar(
            data_frame= ph_creciente,
            x = 'Date',
            y = 'ph',
            template= "plotly_dark")
        fig.update_layout(xaxis=dict(showgrid=False, zeroline=False), yaxis=dict(showgrid=False, zeroline=False))
        fig.update_layout(autosize=False, margin=dict(l=5, r=5, b=5, t=5, pad=4),)
    elif value =='temperatura':
        fig = px.bar(
            data_frame = turbiedad_creciente,
            x = 'Date',
            y = 'temperatura',
            template="plotly_dark")
        fig.update_layout(xaxis=dict(showgrid=False, zeroline=False), yaxis=dict(showgrid=False, zeroline=False))
        fig.update_layout(autosize=False, margin=dict(l=5, r=5, b=5, t=5, pad=4),)
    else:
        fig = px.bar(
            
            data_frame= cloro_creciente,
            x = 'Date',
            y = 'cloro',
            template= "plotly_dark")
        fig.update_layout(xaxis=dict(showgrid=False, zeroline=False), yaxis=dict(showgrid=False, zeroline=False))
        fig.update_layout(autosize=False, margin=dict(l=5, r=5, b=5, t=5, pad=4),)
    return fig

#SEGUNDO CALLBACK


@app.callback(Output('alerta','children'),[Input('segundo dropdown','value')])

def update_graph(value):
    
    if value == 'turbiedad':
        card_content = dbc.CardGroup(dbc.Card(dbc.CardBody(dbc.Alert(turbiedad_max, color="danger"),)))
    elif value == 'ph':
        card_content = dbc.CardGroup(dbc.Card(dbc.CardBody(dbc.Alert(ph_max, color="danger"),)))
    elif value == 'temperatura':
        card_content = dbc.CardGroup(dbc.Card(dbc.CardBody(dbc.Alert(temperatura_max, color="danger"),)))
    else:
        card_content = dbc.CardGroup(dbc.Card(dbc.CardBody(dbc.Alert(cloro_max, color="danger"),)))
    return card_content


@app.callback(Output('alerta2','children'),[Input('segundo dropdown','value')])

def update_graph(value):
    
    if value == 'turbiedad':
        card_content = dbc.CardGroup(dbc.Card(dbc.CardBody(dbc.Alert(turbiedad_prom, color="primary"),)))
    elif value == 'ph':
        card_content = dbc.CardGroup(dbc.Card(dbc.CardBody(dbc.Alert(ph_prom, color="primary"),)))
    elif value == 'temperatura':
        card_content = dbc.CardGroup(dbc.Card(dbc.CardBody(dbc.Alert(temperatura_prom, color="primary"),)))
    else:
        card_content = dbc.CardGroup(dbc.Card(dbc.CardBody(dbc.Alert(cloro_prom, color="primary"),)))
    return card_content


@app.callback(Output('alerta3','children'),[Input('segundo dropdown','value')])

def update_graph(value):
    
    if value == 'turbiedad':
        card_content = dbc.CardGroup(dbc.Card(dbc.CardBody(dbc.Alert(turbiedad_min, color="success"),)))
    elif value == 'ph':
        card_content = dbc.CardGroup(dbc.Card(dbc.CardBody(dbc.Alert(ph_min, color="success"),)))
    elif value == 'temperatura':
        card_content = dbc.CardGroup(dbc.Card(dbc.CardBody(dbc.Alert(temperatura_min, color="success"),)))
    else:
        card_content = dbc.CardGroup(dbc.Card(dbc.CardBody(dbc.Alert(cloro_min, color="success"),)))
    return card_content


@app.callback(Output('alerta5','children'),[Input('segundo dropdown','value')])

def update_graph(value):
    
    if value == 'turbiedad':
        card_content = dbc.CardGroup(dbc.Card(dbc.CardBody(dbc.Alert(turbiedad_ulti, color="secondary"),)))
    elif value == 'ph':
        card_content = dbc.CardGroup(dbc.Card(dbc.CardBody(dbc.Alert(ph_ulti, color="secondary"),)))
    elif value == 'temperatura':
        card_content = dbc.CardGroup(dbc.Card(dbc.CardBody(dbc.Alert(temperatura_ulti, color="secondary"),)))
    else:
        card_content = dbc.CardGroup(dbc.Card(dbc.CardBody(dbc.Alert(cloro_ulti, color="secondary"),)))
    return card_content




if __name__ == '__main__':
    app.run_server(debug=True, port=3000)

