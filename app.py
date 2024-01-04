import yfinance as yf
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
from bs4 import BeautifulSoup
import requests
import datetime as dt
import dash_bootstrap_components as dbc
import sqlite3

acoes = ['WEGE3.SA', 'PETR4.SA', 'CEAB3.SA']

ticker_mapping = {
    'WEGE3.SA': 'weg',
    'PETR4.SA': 'petrobras',
    'CEAB3.SA': 'c%26a'
}

inicio = '2023-01-01'
fim = dt.datetime.now()

def download_stock_data(ticker, start, end):
    try:
        data = yf.download(ticker, start=start, end=end)
        return data
    except Exception as e:
        print(f"Erro ao baixar dados para {ticker}: {e}")
        return None

dados_acoes = {acao: download_stock_data(acao, inicio, fim) for acao in acoes}

conn = sqlite3.connect('dados_acoes.db')

for acao, dados in dados_acoes.items():
    dados.to_sql(acao, conn, if_exists='replace')

conn.close()

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div(style={'backgroundColor': 'white', 'color': 'black', 'height': '100vh'}, children=[
    dcc.Location(id='url', refresh=False),
    dbc.Container([
        dbc.Row([
            dbc.Col([
                dcc.Dropdown(
                    id='dropdown-acao',
                    options=[{'label': acao, 'value': acao} for acao in acoes],
                    value='WEGE3.SA',
                    multi=False,
                    className="mb-3",
                    style={'background-color': 'white', 'color': 'black'}
                ),
                dcc.Graph(
                    id='graph-dados-historicos',
                    style={'width': '100%', 'height': '70vh', 'margin-bottom': '20px'}
                ),
            ], width=6),

            dbc.Col([
                dbc.Row([
                    dbc.Col([
                        html.H2("Notícias", className="mb-3", style={'font-weight': 'bold', 'text-align': 'center', 'color': 'black'}),
                    ], width=12),
                    dbc.Col([
                        html.Div(id='news-content', style={'text-align': 'left', 'margin-top': '20px', 'margin-bottom': '40px'  }),
                    ], width=12),
                ]),
            ], width=6),
        ], className='mt-5'),  

        dbc.Row([
            dbc.Col([
                html.Div(style={'height': '50px'}),
            ]),
        ]),
    ]),
    html.Nav("Gustavo Candido - Varos", style={'color': 'black', 'text-align': 'center', 'padding': '10px'})
])

@app.callback(
    [Output('graph-dados-historicos', 'figure'),
     Output('news-content', 'children')],
    [Input('dropdown-acao', 'value')]
)
def update_graph_and_news(selected_acao):
    fig = go.Figure(data=[go.Candlestick(x=dados_acoes[selected_acao].index,
                                         open=dados_acoes[selected_acao]['Open'],
                                         high=dados_acoes[selected_acao]['High'],
                                         low=dados_acoes[selected_acao]['Low'],
                                         close=dados_acoes[selected_acao]['Close'])])

    fig.update_layout(title=f'Gráfico de Velas - {selected_acao}',
                      xaxis_title='Data',
                      yaxis_title='Preço',
                      xaxis_rangeslider_visible=False,
                      plot_bgcolor='white',  
                      paper_bgcolor='white',  
                      font=dict(color='black')) 

    search_term = ticker_mapping[selected_acao]
    search_url = f'https://braziljournal.com/?s={search_term}'
    response = requests.get(search_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    news_items = soup.select('ul#allnews > li')

    news_links = []
    news_titles = []
    news_descriptions = []

    for i, news_item in enumerate(news_items):
        if i >= 3:
            break

        link = news_item.select_one('h2 a')['href']
        title = news_item.select_one('.boxarticle-infos-title a').text
        description = news_item.select_one('.boxarticle-infos-text').text.strip()

        news_links.append(link)
        news_titles.append(title)
        news_descriptions.append(description)

    return fig, [html.Div([
        html.H3(html.A(title, href=link, target='_blank', style={'color': 'black', 'text-decoration': 'none'})),
        html.P(description, style={'color': 'black', 'margin-bottom': '30px'}),
    ]) for title, description, link in zip(news_titles, news_descriptions, news_links)]

@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/':
        return index_page
    else:
        return '404'

if __name__ == '__main__':
    app.run_server(debug=True)
