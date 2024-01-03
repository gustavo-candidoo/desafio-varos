import yfinance as yf
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
from bs4 import BeautifulSoup
import requests

# Lista de símbolos das ações
acoes = ['WEGE3.SA', 'PETR4.SA', 'CEAB3.SA']

# Mapeamento de tickers para termos de pesquisa
ticker_mapping = {
    'WEGE3.SA': 'weg',
    'PETR4.SA': 'petrobras',
    'CEAB3.SA': 'c&a'
}

# Período desejado (2023-01-01 a 2023-12-31)
inicio = '2023-01-01'
fim = '2023-12-31'

# Dados históricos para cada ação
dados_acoes = {acao: yf.download(acao, start=inicio, end=fim) for acao in acoes}

# Inicialização do aplicativo Dash
app = dash.Dash(__name__)

# Layout do dashboard
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content', className='container-fluid', style={'backgroundColor': 'black'})  # Adiciona estilo de fundo preto
])

# Página inicial
index_page = html.Div([
    dcc.Markdown('''
    # Dashboard de Dados Históricos de Ações
    '''),
    html.Div([
        # Layout da esquerda (gráfico e dropdown)
        html.Div([
            dcc.Dropdown(
                id='dropdown-acao',
                options=[{'label': acao, 'value': acao} for acao in acoes],
                value='WEGE3.SA',
                multi=False,
                className="mb-3"
            ),
            dcc.Graph(
                id='graph-dados-historicos',
                style={'width': '100%', 'height': '70vh'}  # Ajusta a largura e altura do gráfico
            ),
        ], className="col-md-6"),

        # Layout da direita (notícias)
        html.Div([
            html.H2("Notícias", className="mb-3", style={'color': 'white', 'font-weight': 'bold'}),  # Ajusta o estilo do título
            html.Div(id='news-content')
        ], className="col-md-6"),
    ], className="row"),
])

# Callback para atualizar o gráfico e obter notícias com base na seleção do usuário
@app.callback(
    [Output('graph-dados-historicos', 'figure'),
     Output('news-content', 'children')],
    [Input('dropdown-acao', 'value')]
)
def update_graph_and_news(selected_acao):
    # Criação do gráfico de velas com Plotly
    fig = go.Figure(data=[go.Candlestick(x=dados_acoes[selected_acao].index,
                                         open=dados_acoes[selected_acao]['Open'],
                                         high=dados_acoes[selected_acao]['High'],
                                         low=dados_acoes[selected_acao]['Low'],
                                         close=dados_acoes[selected_acao]['Close'])])

    fig.update_layout(title=f'Gráfico de Velas - {selected_acao}',
                      xaxis_title='Data',
                      yaxis_title='Preço',
                      xaxis_rangeslider_visible=False)

    # Scraping de notícias com base no ticker
    search_term = ticker_mapping[selected_acao]
    search_url = f'https://braziljournal.com/?s={search_term}'
    response = requests.get(search_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Encontrar os elementos <li> dentro da lista
    news_items = soup.select('ul#allnews > li')

    # Inicializar listas para armazenar informações extraídas
    news_links = []
    news_titles = []
    news_descriptions = []

    # Limitar a 3 notícias
    for i, news_item in enumerate(news_items):
        if i >= 3:
            break

        link = news_item.select_one('h2 a')['href']
        title = news_item.select_one('.boxarticle-infos-title a').text
        description = news_item.select_one('.boxarticle-infos-text').text.strip()

        news_links.append(link)
        news_titles.append(title)
        news_descriptions.append(description)

    # Retornar o gráfico de velas e o conteúdo das notícias
    return fig, [html.Div([
        html.H3(html.A(title, href=link, target='_blank')),  # Adiciona o link no título
        html.P(description),
    ]) for title, description, link in zip(news_titles, news_descriptions, news_links)]

# ...

# Atualização do layout baseado na URL
@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/':
        return index_page
    else:
        return '404'

if __name__ == '__main__':
    app.run_server(debug=True)
