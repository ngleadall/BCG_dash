# -*- coding: utf-8 -*-
# Importing Modules
import os
import pandas as pd
import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_table
import plotly.graph_objs as go
from dash.dependencies import Input, Output, State

# App setup + stylesheets
external_stylesheets = [dbc.themes.BOOTSTRAP]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = 'BGC Accreditation Dashboard'
#######################################
# Data inputting
#######################################


def import_main_data():
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

    # Check if failing
    # Check if Data returned
    df['failed'] = df['sample_status'].apply(
        lambda x: 1 if x == "Fail" else 0)

    def sex_check(submitted, inferred):

        submitted = str(submitted)
        inferred = str(inferred)

        accepted_sex = ["Male", "Female"]
        if submitted not in accepted_sex or inferred not in accepted_sex:
            return("NaN")
        if submitted == inferred:
            return("Pass")
        else:
            return("Fail")

    # sex check
    df['sex_check'] = df.apply(
        lambda x: sex_check(x.Submitted_sex, x.Inferred_sex), axis=1)
    df['sample_status'] = df['sex_check'].apply(
        lambda x: "Fail" if x != "Pass" else x)

    return(df)


df = import_main_data()


def import_targets():
    '''
    imports targets for each partner
    '''
    df = pd.read_excel('./static/data/target_numbers.data.xlsx', sheet_name=0)

    return(df)


targets_df = import_targets()


def import_antigen_counts():
    '''
    imports data for antigen counts
    '''
    df = pd.read_csv('./static/data/Antigen_data_counts.csv')
    df = df.rename(columns={"Unnamed: 0": "posneg"})
    df = df.set_index('posneg').T.reset_index()

    return(df)


antigen_counts = import_antigen_counts()

#######################################
# Functions
#######################################


def generate_header():
    '''
    makes the page header
    '''
    LOGO = "/static/img/BGC_logo_only.50px.png"

    return dbc.Navbar(
        [
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        dbc.Col(html.Img(src=LOGO, height="50px")),
                        dbc.Col(dbc.NavbarBrand(
                            "Accreditation Dashboard", className="ml-2", style={'padding-top': '10px'})),
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

 # SAMPLE SUMMARY


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
        ], fluid=True)
    ], style={'padding-top': '15px',
              'padding-bottom': '15px',
              'text-align': 'center',
              }
    )
#####################
# SAMPLE PANEL
#####################


def sample_status_plot():
    '''
    Generates the sample status plot
    '''

    current_status = df[['cohort', 'DNA_extracted', 'genotyped',
                         'data_returned', 'failed']].groupby('cohort', as_index=False).sum()

    return dcc.Graph(id='sample_status_plot',
                     figure={
                         'data': [{
                             'x': current_status['cohort'],
                             'y': current_status['DNA_extracted'],
                             'type': 'bar',
                             'name': u'DNA extracted'
                         },
                             {
                             'x': current_status['cohort'],
                             'y': current_status['genotyped'],
                             'type': 'bar',
                             'name': u'Sent for genotyping'
                         }, {
                             'x': current_status['cohort'],
                             'y': current_status['data_returned'],
                             'type': 'bar',
                             'name': u'Data returned'
                         }, {
                             'x': current_status['cohort'],
                             'y': current_status['failed'],
                             'type': 'bar',
                             'name': u'Failed samples'
                         }],
                         'layout': dict(
                             title={'text': 'Sample Status Summary'},
                             xaxis={'title': 'Partner'},
                             yaxis={'title': 'Sample count'},
                             legend=dict(orientation='v', y=0.5),
                             hovermode='closest'
                         )
                     })


def sample_target_plot():

    counts = df['cohort'].value_counts().rename_axis(
        'Partner').reset_index(name='counts')

    return dcc.Graph(id='sample_target_plot',
                     figure={
                         'data': [{
                             'x': targets_df['Partner'],
                             'y': targets_df['Target'],
                             'type':'bar',
                             'name':'Collection target'
                         }, {
                             'x': counts['Partner'],
                             'y': counts['counts'],
                             'type':'bar',
                             'name':'Collected'
                         }],
                         'layout': dict(
                             title={'text': 'Collection status'},
                             xaxis={'title': 'Partner'},
                             yaxis={'title': 'Sample count'},
                             legend=dict(orientation='v', y=0.5),
                             hovermode='closest'
                         )
                     }
                     )


def antigen_target_plot():

    counts = antigen_counts

    return dcc.Graph(id='antigen_count_plot',
                     figure={
                         'data': [{
                             'x': counts['index'],
                             'y': counts['+'],
                             'type':'bar',
                             'name':'+ive'
                         }, {
                             'x': counts['index'],
                             'y': counts['-'],
                             'type':'bar',
                             'name':'-ive',
                         }],
                         'layout': dict(
                             title={'text': 'Antigen Collection Status'},
                             xaxis={'title': 'Antigen'},
                             yaxis={'title': 'Sample count'},
                             legend=dict(orientation='v', y=0.5),
                             hovermode='closest'

                         )
                     }
                     )


def generate_sample_panel_tab():
    '''
    generates the content for tab 1. Sample panels
    '''

    return html.Div([
        dbc.Container([
            dbc.Row([
                dbc.Col(sample_target_plot()),
                dbc.Col(sample_status_plot())
            ], align="center"),
        ], fluid=True),
        dbc.Container([
            antigen_target_plot()
        ], fluid=True)
    ])

###########################
# QC tab
###########################


def generate_dqc_CR_plot(data_frame):
    '''
    Generates dqc vs callrate plot
    '''
    return dcc.Graph(id='dqc_v_cr_plot',
                     figure={
                         'data': [
                             dict(
                                 x=data_frame[data_frame['sample_status']
                                              == i]['dQC'],
                                 y=data_frame[data_frame['sample_status']
                                              == i]['Cluster_CR'],
                                 text=data_frame[data_frame['sample_status']
                                                 == i]['ID'],
                                 mode='markers',
                                 name=i
                             ) for i in data_frame.sample_status.unique()
                         ],
                         'layout': dict(
                             title={'text': 'Cluster call rate vs. Dish QC'},
                             xaxis={'title': 'Dish QC'},
                             yaxis={'title': 'Cluster call rate (%)'},
                             legend=dict(orientation='v', y=0.5),
                             hovermode='closest',
                             width=500,
                             height=500,
                             autosize=True
                         )
                     })


def generate_cr_het_plot(data_frame):
    '''
    plots cr vs het rate
    '''

    return dcc.Graph(id='cr_v_het_plot',
                     figure={
                         'data': [
                             dict(
                                 x=data_frame[data_frame['sample_status']
                                              == i]['het_rate'],
                                 y=data_frame[data_frame['sample_status']
                                              == i]['Cluster_CR'],
                                 text=data_frame[data_frame['sample_status']
                                                 == i]['ID'],
                                 mode='markers',
                                 name=i
                             ) for i in data_frame.sample_status.unique()
                         ],
                         'layout': dict(
                             title={
                                 'text': 'Cluster call rate vs. Heterozygosity'},
                             xaxis={'title': 'Heterozygosity (%)'},
                             yaxis={'title': 'Cluster call rate (%)'},
                             legend=dict(orientation='v', y=0.5),
                             hovermode='closest',
                             autosize=True,
                             width=500,
                             height=500
                         )
                     })


def generate_failed_samples_table():
    '''
    Generates table of failed samples
    '''

    columns = [
        "Sample ID",
        "Cohort",
        "Pico green",
        "CV%",
        "Heterozygosity rate",
        "dish QC",
        "Sex check",
        "Cluster CR",
        "BP failure mode",
        "Sample status"
    ]

    d = df[[
        "ID",
        "cohort",
        "pico_green",
        "CV%",
        "het_rate",
        "dQC",
        "Cluster_CR",
        "Failure_Mode",
        "sex_check",
        "sample_status",
    ]]

    d = d.rename(columns={
        "ID": "Sample ID",
        "cohort": "Cohort",
        "pico_green": "Pico green",
        "CV%": "CV%",
        "dQC": "dish QC",
        "het_rate": "Heterozygosity rate",
        "Cluster_CR": "Cluster CR",
        "sex_check": "Sex check",
        "Failure_Mode": "BP failure mode",
        "sample_status": "Sample status"})

    return dash_table.DataTable(
        id='table',
        columns=[{"name": i, "id": i} for i in columns],
        data=d.sort_values(
            by=['Cohort']).to_dict('records'),
        style_cell={
            'padding': '5px',
            'textAlign': 'center',
            'border': '1px solid black'
        },
        style_header={
            'backgroundColor': 'rgb(230, 230, 230)',
            'fontWeight': 'bold',
            'border': '1px solid black'
        },
        style_data_conditional=[
            {'if': {
                'column_id': 'Sex check',
                'filter_query': '{Sex check} eq "Fail"'
            },
                'backgroundColor': '#ff9b9e',
                'fontWeight': 'bold'},
            {
                'if': {
                    'column_id': 'dish QC',
                    'filter_query': '{dish QC} < 0.82'
                },
                'backgroundColor': '#ff9b9e',
                'fontWeight': 'bold'
            },
            {
                'if': {
                    'column_id': 'Cluster CR',
                    'filter_query': '{Cluster CR} < 97.0'
                },
                'backgroundColor': '#ff9b9e',
                'fontWeight': 'bold'
            },

        ],
        editable=True,
        filter_action='native',
        filter_query='{Sample status} eq "Fail"',
        sort_action="native",
        sort_mode="single",
        column_selectable="multi",
        selected_columns=[],
        selected_rows=[],
        page_action="native",
        page_current=0,
        page_size=30
    )


def generate_qc_panel_tab():
    '''
    generates the content for tab 2. Sample QC
    '''

    return html.Div([
        dbc.Container([
            dbc.Row([
                dbc.Col(generate_dqc_CR_plot(df)),
                dbc.Col(generate_cr_het_plot(df))
            ])
        ])
    ]), html.Div([
        html.H4(children='Table browser'),
        dbc.Container([
            generate_failed_samples_table()
        ], fluid=True)
    ], style={'padding-top': '15px',
              'padding-bottom': '15px',
              'padding-right': '30px',
              'padding-left': '30px'
              },
    ), html.Div(
        id='datatable-interactivity-container')

####################################
# Main App
####################################


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
        dcc.Tab(label='Sample QC', value='tab-2'),
    ]),
    html.Div(id='tabs-content')

])

app.config.suppress_callback_exceptions = True
# Callbacks
@app.callback(Output('tabs-content', 'children'),
              [Input('tabs', 'value')])
def render_content(tab):
    if tab == 'tab-1':
        return generate_sample_panel_tab()
    if tab == 'tab-2':
        return generate_qc_panel_tab()



if __name__ == '__main__':
    # print("I am working!")
    app.run_server(debug=True)
