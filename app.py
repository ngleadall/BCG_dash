# -*- coding: utf-8 -*-
import os

import dash
import dash_core_components as dcc
import dash_html_components as html

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# Server
server = app.server

app.layout = html.Div(children=[
    html.H1(children='BGC UKBBv2 Validation Status'),
    html.Div(children=[
        dcc.Tabs(id='tabs', children=[
            dcc.Tab(label='Panel Status', children=[
                html.Div(
                    className="container",
                    style={
                        'width': '92%',
                        'max-width': 'none',
                        'font-size': '1.5rem',
                        'padding': '10px 10px'
                    },
                    children=[dcc.Graph(
                        id='g1',
                        figure={
                            'data': [
                                {'x': [1, 2, 3], 'y': [4, 1, 2],
                                    'type': 'bar', 'name': 'SF'},
                                {'x': [1, 2, 3], 'y': [2, 4, 5],
                                 'type': 'bar', 'name': u'Montréal'},
                            ],
                            'layout': {
                                'title': 'Dash Data Visualization'
                            }
                        }
                    )])
            ]),
            dcc.Tab(label='Antigens Collected', children=[
                html.Div(
                    className="container",
                    style={
                        'width': '92%',
                        'max-width': 'none',
                        'font-size': '1.5rem',
                        'padding': '10px 10px'
                    },
                    children=[dcc.Graph(
                        id='g2',
                        figure={
                            'data': [
                                {'x': [1, 2, 3], 'y': [4, 1, 2],
                                    'type': 'bar', 'name': 'SF'},
                                {'x': [1, 2, 3], 'y': [2, 4, 5],
                                 'type': 'bar', 'name': u'Montréal'},
                            ],
                            'layout': {
                                'title': 'Dash Data Visualization'
                            }
                        }
                    )])
            ]),
            dcc.Tab(label='Sample Status', children=[]),
            dcc.Tab(label='Sample QC', children=[])

        ])
    ])
])

if __name__ == '__main__':
    app.run_server(debug=True)
