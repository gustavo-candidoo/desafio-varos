import yfinance as yf
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objects as go

# Lista de símbolos das ações
acoes = ['WEGE3.SA', 'PETR4.SA', 'CEAB3.SA']

# Período desejado (2023-01-01 a 2023-12-31)
inicio = '2023-01-01'
fim = '2023-12-31'

# Dados históricos para cada ação
dados_acoes = {acao: yf.download(acao, start=inicio, end=fim) for acao in acoes}

# Inicialização do aplicativo Dash
app = dash.Dash(__name__)

# Layout do dashboard
app.layout = html.Div([
    html.H1("Dashboard de Dados Históricos de Ações"),
    
    dcc.Dropdown(
        id='dropdown-acao',
        options=[{'label': acao, 'value': acao} for acao in acoes],
        value='WEGE3.SA',
        multi=False
    ),
    
    dcc.Graph(
        id='graph-dados-historicos'
    )
])

# Callback para atualizar o gráfico com base na seleção do usuário
@app.callback(
    Output('graph-dados-historicos', 'figure'),
    [Input('dropdown-acao', 'value')]
)
def update_graph(selected_acao):
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
    
    return fig

# Execução do aplicativo
if __name__ == '__main__':
    app.run_server(debug=True)
import yfinance as yf
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objects as go

# Lista de símbolos das ações
acoes = ['WEGE3.SA', 'PETR4.SA', 'CEAB3.SA']

# Período desejado (2023-01-01 a 2023-12-31)
inicio = '2023-01-01'
fim = '2023-12-31'

# Dados históricos para cada ação
dados_acoes = {acao: yf.download(acao, start=inicio, end=fim) for acao in acoes}

# Inicialização do aplicativo Dash
app = dash.Dash(__name__)

# Layout do dashboard
app.layout = html.Div([
    html.H1("Dashboard de Dados Históricos de Ações"),
    
    dcc.Dropdown(
        id='dropdown-acao',
        options=[{'label': acao, 'value': acao} for acao in acoes],
        value='WEGE3.SA',
        multi=False
    ),
    
    dcc.Graph(
        id='graph-dados-historicos'
    )
])

# Callback para atualizar o gráfico com base na seleção do usuário
@app.callback(
    Output('graph-dados-historicos', 'figure'),
    [Input('dropdown-acao', 'value')]
)
def update_graph(selected_acao):
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
    
    return fig

# Execução do aplicativo
if __name__ == '__main__':
    app.run_server(debug=True)
