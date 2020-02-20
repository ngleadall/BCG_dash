# -*- coding: utf-8 -*-
# Importing Modules
import os
import pandas as pd
import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output, State

# Data importing


# App setup + stylesheets
external_stylesheets = [dbc.themes.BOOTSTRAP]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# Handle data input


def format_df():
    ''' 
    takes data input and formats it
    '''

    df = pd.read_excel('./static/data/web_test.data.xlsx', sheet_name=0)

    # Check if DNA extracted
    df['DNA_extracted'] = df['date_dna_extracted'].apply(
        lambda x: 1 if pd.notna(x) else 0)

    # Check if Genotyped
    df['genotyped'] = df['date_sent_for_genotype'].apply(
        lambda x: 1 if pd.notna(x) else 0)

    # Check if Data returned
    df['data_returned'] = df['best_array'].apply(
        lambda x: 1 if pd.notna(x) else 0)

    return(df)


df = format_df()

#######################################
# Functions
#######################################


def generate_header():
    '''
    makes the page header
    '''
    LOGO = "/static/img/BGC_logo_only.png"

    return dbc.Navbar(
        [
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        dbc.Col(html.Img(src=LOGO, height="50px")),
                        dbc.Col(dbc.NavbarBrand(
                            "Accreditation Project Dashboard", className="ml-2", style={'padding-top': '10px'})),
                    ],
                    align="center",
                    no_gutters=True,
                )
            ),
            dbc.NavbarToggler(id="navbar-toggler")
        ],
        color="dark",
        dark=True,
    )


def generate_info_card(card_title, card_content):
    '''
    takes text and a number and generates a nice info box
    '''
    card_content = [
        dbc.CardBody(
            [
                html.H4(card_title,
                        className="card-title"),
                html.P(card_content,
                       className="card-text",
                       style={'font-size': '150%'}
                       )]
        )
    ]

    return dbc.Card(card_content,
                    color='dark',
                    inverse=True,)


def generate_info_row(t_samples, t_dna, t_genotyped, t_returned):
    '''
    generates summary statistics row
    '''

    return html.Div([
        dbc.Container([
            dbc.CardDeck([
                generate_info_card("Total Samples", t_samples),
                generate_info_card("DNA Extracted", t_dna),
                generate_info_card("Genotyped", t_genotyped),
                generate_info_card("Data Returned", t_returned)
            ])
        ])
    ], style={'padding-top': '15px',
              'padding-bottom': '15px',
              'text-align': 'center',
              }
    )


# Server
server = app.server

# Layout
app.layout = html.Div(children=[
    generate_header(),
    generate_info_row(len(df),
                      df['DNA_extracted'].sum(),
                      df['genotyped'].sum(),
                      df['data_returned'].sum()
                      ),
    dcc.Tabs(id="tabs", value='tab-1', children=[
        dcc.Tab(label='Collection Targets', value='tab-1'),
        dcc.Tab(label='Antigens collected', value='tab-2'),
        dcc.Tab(label='Sample Table', value='tab-3'),
        dcc.Tab(label='Sample QC', value='tab-4'),
    ]),
    html.Div(id='tabs-content')

])

# Callbacks
@app.callback(Output('tabs-content', 'children'),
              [Input('tabs', 'value')])
def render_content(tab):
    if tab == 'tab-1':
        return html.Div(children=['I am div 1!'])
    if tab == 'tab-2':
        return html.Div(children=['I am div 2!'])
    if tab == 'tab-3':
        return html.Div(children=['I am div 3!'])
    if tab == 'tab-4':
        return html.Div(children=['I am div 4!'])
        return html.Div(children=['I am div 4!'])
        return html.Div(children=['I am div 4!'])


if __name__ == '__main__':
    app.run_server(debug=True)
