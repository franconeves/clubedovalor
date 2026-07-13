import pandas as pd
import yfinance as yf
from datetime import datetime

print("🔄 Iniciando varredura com a Fórmula Mágica Adaptada (B3)...")

# Lista estruturada de empresas da B3
tickers_b3 = [
    'VALE3', 'PETR4', 'PETR3', 'ITUB4', 'BBDC4', 'BBAS3', 'ITSA4', 'WEGE3', 'B3SA3', 'RENT3',
    'GGBR4', 'SUZB3', 'ELET3', 'EQTL3', 'LREN3', 'RADL3', 'PRIO3', 'RDOR3', 'RAIL3', 'CMIG4',
    'VIVT3', 'SBSP3', 'VBBR3', 'JBSS3', 'CCRO3', 'CPLE6', 'BRFS3', 'HYPE3', 'GOAU4', 'CSAN3',
    'CPFE3', 'CYRE3', 'EMBR3', 'STBP3', 'MRVE3', 'MULT3', 'EGIE3', 'YDUQ3', 'CRFB3', 'TAEE11',
    'UGPA3', 'USIM5', 'CSNA3', 'MRFG3', 'BEEF3', 'SAPR11', 'KLBN11', 'TRPL4', 'ALOS3', 'ALUP11',
    'ARZZ3', 'ASAI3', 'AZUL4', 'BPAC11', 'BRAP4', 'BRKM5', 'CASH3', 'CIEL3', 'COGN3', 'CSMG3',
    'DXCO3', 'ECOR3', 'ENEV3', 'ENGI11', 'EZTC3', 'FLRY3', 'GMAT3', 'INTB3', 'IRBR3', 'JHSF3',
    'KEPL3', 'LWSA3', 'MATD3', 'MGLU3', 'MOVI3', 'NEOE3', 'NTCO3', 'ODPV3', 'ONCO3', 'ORVR3',
    'PSSA3', 'QUAL3', 'RAPT4', 'RAIZ4', 'RCSL4', 'SANB11', 'SIMH3', 'SLCE3', 'SMTO3', 'TASA4',
    'TEND3', 'TIMS3', 'TOTS3', 'TRIS3', 'UNIP6', 'VAMO3', 'VIVA3', 'WIZC3', 'ZAMP3', 'AGRO3',
    'ANIM3', 'CAML3', 'CEAB3', 'DIRR3', 'EVEN3', 'GUAR3', 'LEVE3', 'LIGT3', 'MDIA3', 'MYPK3',
    'RECV3', 'FRAS3', 'TUPY3', 'VLID3', 'POMO4', 'POSI3', 'RANI3', 'ROMI3', 'PLPL3'
]

tickers = [f"{t}.SA" for t in tickers_b3]
dados_acoes = []

for t in tickers:
    try:
        ticker_object = yf.Ticker(t)
        info = ticker_object.info
        nome_papel = t.replace('.SA', '')

        preco_atual = info.get('currentPrice') or info.get('regularMarketPrice')
        volume_diario = info.get('averageVolume') or info.get('regularMarketVolume')

        if not preco_atual:
            continue

        # 1. Ajuste do Dividend Yield
        dy = info.get('dividendYield', 0)
        dy_ajustado = (dy if dy > 1 else dy * 100) if dy else 0

        # 2. Captura do Múltiplo de Preço (EV/EBITDA ou similar)
        ev_ebit = info.get('enterpriseValueToEbitda') or info.get('enterpriseToEbitda') or info.get('trailingPE')

        # 3. Métrica de Qualidade Resiliente (Garante que sempre haverá um indicador de retorno)
        roic = info.get('returnOnInvestment') or info.get('returnOnAssets') or info.get('returnOnEquity')

        # Backup caso as chaves tradicionais de retorno venham vazias do Yahoo
        if not roic:
            margem_op = info.get('operatingMargins', 0)
            roic = margem_op if margem_op else 0

        roic_ajustado = roic * 100 if roic else 0

        # Filtro de Segurança Dinâmico (flexível para não travar a execução)
        if ev_ebit and ev_ebit > 0:
            dados_acoes.append({
                'Papel': nome_papel,
                'Preco_Atual': preco_atual,
                'EV_EBIT': round(ev_ebit, 2),
                'ROIC_%': round(roic_ajustado, 2),
                'Dividend_Yield_%': round(dy_ajustado, 2),
                'Volume_Medio_Diario': volume_diario if volume_diario else 0
            })
            print(f"✓ {nome_papel} processada com sucesso.")
    except Exception as e:
        continue

if len(dados_acoes) == 0:
    print("\n⚠️ Erro: Não foi possível obter dados da API do Yahoo Finance no momento. Verifique sua conexão.")
else:
    df = pd.DataFrame(dados_acoes)

    # Filtro A: Eliminar ações sem liquidez de mercado relevante (volume mínimo ajustado para proteção)
    df = df[df['Volume_Medio_Diario'] > 10000]

    # Filtro B: Evitar duplicidade de classes de ações (ex: PETR3 e PETR4)
    df['Empresa'] = df['Papel'].str[:4]
    df = df.sort_values(by='Volume_Medio_Diario', ascending=False)
    df = df.drop_duplicates(subset='Empresa', keep='first').drop(columns=['Empresa'])

    # =====================================================================
    # PASSO 4: APLICANDO A MATEMÁTICA DA FÓRMULA MÁGICA
    # =====================================================================
    # Rank de Barateamento: menor EV/EBIT ganha melhor posição (1 é o melhor)
    df['Rank_EV_EBIT'] = df['EV_EBIT'].rank(ascending=True)

    # Rank de Qualidade: maior ROIC ganha melhor posição (1 é o melhor)
    df['Rank_ROIC'] = df['ROIC_%'].rank(ascending=False)

    # Pontuação final (Soma dos Ranks)
    df['Pontuacao_Formula'] = df['Rank_EV_EBIT'] + df['Rank_ROIC']

    # Ordena o DataFrame pela pontuação mágica final
    df_ranking = df.sort_values(by='Pontuacao_Formula', ascending=True).reset_index(drop=True)
    df_ranking.index = df_ranking.index + 1
    df_ranking.index.name = 'Posicao_Formula'

    # Preparando visualização final limpa
    df_final = df_ranking[['Papel', 'Preco_Atual', 'EV_EBIT', 'ROIC_%', 'Dividend_Yield_%']]

    # Exportando arquivo Excel
    data_hoje = datetime.now().strftime('%Y-%m-%d')
    nome_excel = f"exports/Formula_Magica_B3_{data_hoje}.xlsx"
    df_ranking.to_excel(nome_excel)

    print("\n" + "="*65)
    print("🏆 TOP 10 - FÓRMULA MÁGICA (AÇÕES BARATAS + ALTA QUALIDADE):")
    print(df_final.head(10))
    print("="*65)
    print(f"✨ SUCESSO! Relatório atualizado gerado em: {nome_excel}")