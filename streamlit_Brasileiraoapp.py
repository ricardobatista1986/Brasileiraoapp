import streamlit as st
import pandas as pd
import base64
from pygwalker.api.streamlit import StreamlitRenderer, init_streamlit_comm
from pygwalker import GlobalVarManager


#GlobalVarManager.set_kanaries_api_key(st.secrets["api_key"])

st.set_page_config(layout="wide")
st.title('Brasileirão Série A - Estatísticas')

st.markdown("""
Este app realiza web scraping dos dados estatísticos das equipes do Brasileirão Série A e possibilita a visualização utilizando o PygWalker!
* **Fonte:** FBref.com
""")

# Establish communication between pygwalker and streamlit
init_streamlit_comm()

#sidebar for user input features
st.sidebar.header('User Input Features')
selected_year = st.sidebar.selectbox('Ano', list(reversed(range(2014,2024))))

# Dict for type of stats 
league_data = {
    0: "Classificação",
    2: "Estatísticas da Equipe",
    4: "Estatísticas do Goleiro",
    6: "Estatísticas do Goleiro (Avançadas)",
    8: "Estatísticas de Chutes",
    10: "Estatísticas de Passes",
    12: "Estatísticas de Tipos de Passes",
    14: "Estatísticas de Gols e Criação de Chances de Gol",
    16: "Estatísticas Defensivas",
    18: "Estatísticas de Posse de Bola",
    20: "Estatísticas de Tempo de Jogo",
    22: "Estatísticas Diversas",
}

values_list = [value for value in league_data.values()]

selected_stat = st.sidebar.selectbox('Selecionar Estatística', [value for value in league_data.values()])


def get_keys_by_value(dictionary, target_value):
    return [key for key, value in dictionary.items() if value == target_value]


target_value = selected_stat
ass_key = get_keys_by_value(league_data, target_value)



# Web scraping of EPL Team stats
# https://fbref.com/en/comps/9/Premier-League-Stats
def load_data(year):
    url = "https://fbref.com/en/comps/24/" + str(year) + "-" + str(year+1)
 
############################################################################################################
############################################################################################################  
    if selected_stat == "Classificação":
        html = pd.read_html(url, header=0)
        df = html[0]  # Obtendo o DataFrame de classificação da liga
        # Renomear colunas e selecionar apenas as desejadas
        
        df = df.rename(columns={"Rk": "Cl",
                                "Squad": "Equipe",
                                "MP": "P",
                                "W": "V",
                                "D": "E",
                                "L": "D",
                                "GF": "G",
                                "Pts": "Pts",
                                "Pts/MP": "Pts/90",
                                "Top Team Scorer": "Artilheiro"})

        df[["xG", "xGA", "xGD"]] = df[["xG", "xGA", "xGD"]].astype(float)
        
        df["xPts"] = (df["P"] * 3 * ((df["xG"]**1.536) / ((df["xG"]**1.536) + (df["xGA"]**1.536))))
        df[["xPts"]] = df[["xPts"]].round(1)
        
        df["Pts-xPts"] = df["Pts"] - df["xPts"]
        df[["Pts-xPts"]] = df[["Pts-xPts"]].round(1)
        
        df["xG"] = df["xG"].round(1)
        df["xGA"] = df["xGA"].round(1)
        df["xGD"] = df["xGD"].round(1)

        df = df[["Cl", "Equipe", "P", "V", "E", "D", "G", "GA", "GD", "Pts", "Pts/90", "xG", "xGA", "xGD",
                 "xPts", "Pts-xPts", "Artilheiro"]]  # Selecionar as colunas desejadas

        # Configurações de estilo para congelar a primeira coluna
        frozen_columns = {"Equipe": {"sticky": True}}
        
        return df  # Mover esta linha para fora do bloco if

############################################################################################################
############################################################################################################
    elif selected_stat == "Estatísticas da Equipe":
        html = pd.read_html(url, header=1)
        df = html[2]  # Obtendo o DataFrame de estatísticas
        df = df.rename(columns={"Squad": "Equipe",
                                "# Pl": "#Jogadores",
                                "Age": "Idade Med.",
                                "Poss": "Posse de Bola",
                                "MP": "P",
                                "Min": "Min.",
                                "Gls": "G",
                                "Ast": "A",
                                "G+A": "G+A",
                                "G-PK": "G-PK",
                                "PK": "PK G",
                                "PKatt": "PK",
                                "CrdY": "Amarelos",
                                "CrdR": "Vermelhos",
                                "xG": "xG",
                                "npxG": "npxG",
                                "xAG": "xA",
                                "npxG+xAG": "npxG+xA",
                                "PrgC": "Carregadas Prog.",
                                "PrgP": "Passes Prog.",
                                "Gls.1": "G/90",
                                "Ast.1": "A/90",
                                "G+A.1": "G+A/90",
                                "G-PK.1": "G-PK/90",
                                "G+A-PK": "G+A-PK/90",
                                "xG.1": "xG/90",
                                "xAG.1": "xA/90",
                                "xG+xAG": "xG+xA/90",
                                "npxG.1": "npxG/90",
                                "npxG+xAG.1": "npxG+xA/90"})
        
        df["G/90"] = df["G/90"].round(1)
        df["A/90"] = df["A/90"].round(1)
        df["G+A/90"] = df["G+A/90"].round(1)
        df["G-PK/90"] = df["G-PK/90"].round(1)
        df["G+A-PK/90"] = df["G+A-PK/90"].round(1)
        df["xG/90"] = df["xG/90"].round(1)
        df["xA/90"] = df["xA/90"].round(1)
        df["xG+xA/90"] = df["xG+xA/90"].round(1)
        df["npxG/90"] = df["npxG/90"].round(1)
        df["npxG+xA/90"] = df["npxG+xA/90"].round(1)
        
        
        df = df[["Equipe", "#Jogadores", "Idade Med.", "Posse de Bola", "P", "Min.", "G", "A", "G+A", "G-PK",
                 "PK","PK G", "Amarelos", "Vermelhos", "xG", "npxG", "xA", "npxG+xA", "Carregadas Prog.",
                 "Passes Prog.","G/90", "A/90", "G+A/90", "G-PK/90", "G+A-PK/90", "xG/90", "xA/90",
                 "xG+xA/90", "npxG/90", "npxG+xA/90"]]# Selecionar as colunas desejadas

        # Configurações de estilo para congelar a segunda coluna
        #frozen_columns = {"Equipe": {"sticky": True}}
        
        return df  # Adicione esta linha para retornar o dataframe após as manipulações

############################################################################################################
############################################################################################################
    elif selected_stat == "Estatísticas do Goleiro":
        html = pd.read_html(url, header=1)
        df = html[4]  # Obtendo o DataFrame de estatísticas
        df = df.rename(columns={"Squad": "Equipe",
                                "# Pl": "#Goleiros",
                                "MP": "P",
                                "Min": "Min.",
                                "GA": "GA",
                                "GA90": "GA/90",
                                "SoTA": "SoTA",
                                "Saves": "Defesas",
                                "Save%": "%Defesas",
                                "W": "V",
                                "D": "E",
                                "L": "D",
                                "CS": "Clean Sheet",
                                "CS%": "%Clean Sheet",
                                "PKatt": "PKA",
                                "PKA": "GPKA",
                                "PKsv": "PKA Defendidos",
                                "PKm": "PKA Fora",
                                "Save%.1": "%PKA Defendidos"})
        
        df["GA/90"] = df["GA/90"].round(1)
        
        df = df[["Equipe", "#Goleiros", "P", "Min.", "GA", "GA/90", "SoTA", "Defesas", "%Defesas", "V", "E", "D",
                 "Clean Sheet", "%Clean Sheet", "PKA", "GPKA", "PKA Defendidos", "PKA Fora", "%PKA Defendidos"]]  # Selecionar as colunas desejadas

        # Configurações de estilo para congelar a terceira coluna
        #frozen_columns = {"Equipe": {"sticky": True}}
        
        return df  # Adicione esta linha para retornar o dataframe após as manipulações
        
############################################################################################################
############################################################################################################        
    elif selected_stat == "Estatísticas do Goleiro (Avançadas)":
        html = pd.read_html(url, header=1)
        df = html[6]  # Obtendo o DataFrame de estatísticas
        df = df.rename(columns={"Squad": "Equipe",
                                "90s": "P",
                                "GA": "GA",
                                "PKA": "GPKA",
                                "FK": "GA Falta",
                                "CK": "GA Escanteio",
                                "OG": "OG",
                                "PSxG": "PSxG",
                                "PSxG/SoT": "PSxG/SoTA",
                                "PSxG+/-": "PSxG-GA",
                                "/90": "PSxG-GA/90",
                                "Cmp": "Passes Longos Completos",
                                "Att": "Passes Longos",
                                "Cmp%": "%Passes Longos Completos",
                                "Att (GK)": "Passes Curtos",
                                "Thr": "Passes com Mãos",
                                "Launch%": "%Passes Longos",
                                "AvgLen": "Dist. Média dos Passes",
                                "Att.1": "Tiros de Meta",
                                "Launch%.1": "%Tiros de Meta Longos",
                                "AvgLen.1": "Dist. Média dos Tiros de Meta",
                                "Opp": "Cruzamentos A",
                                "Stp": "Cruzamentos A Bloqueados",
                                "Stp%": "%Cruzamentos A Bloqueados",
                                "#OPA": "Ações Def. Fora Peq. Área",
                                "#OPA/90": "Ações Def. Fora Peq. Área/90",
                                "AvgDist": "Dist. Média Ações Def. Fora Peq. Área"})
            
        df["Ações Def. Fora Peq. Área/90"] = df["Ações Def. Fora Peq. Área/90"].round(1)
            
        df = df[["Equipe", "P", "GA", "GPKA", "GA Falta", "GA Escanteio", "OG", "PSxG", "PSxG/SoTA", "PSxG-GA",
                 "PSxG-GA/90", "Passes Longos", "Passes Longos Completos", "%Passes Longos Completos",
                 "Passes Curtos", "Passes com Mãos", "%Passes Longos", "Dist. Média dos Passes", "Tiros de Meta",
                 "%Tiros de Meta Longos", "Dist. Média dos Tiros de Meta", "Cruzamentos A",
                 "Cruzamentos A Bloqueados", "%Cruzamentos A Bloqueados", "Ações Def. Fora Peq. Área", 
                 "Ações Def. Fora Peq. Área/90", "Dist. Média Ações Def. Fora Peq. Área"]]  # Selecionar as colunas desejadas

        # Configurações de estilo para congelar a terceira coluna
        #frozen_columns = {"Equipe": {"sticky": True}}
            
        return df  # Adicione esta linha para retornar o dataframe após as manipulações
            
############################################################################################################
############################################################################################################           
    elif selected_stat == "Estatísticas de Chutes":
        html = pd.read_html(url, header=1)
        df = html[8]  # Obtendo o DataFrame de estatísticas
        df = df.rename(columns={"Squad": "Equipe",
                                "90s": "P",
                                "Gls": "G",
                                "Sh": "Chutes",
                                "SoT": "SoT",
                                "SoT%": "%SoT",
                                "Sh/90": "Chutes/90",
                                "SoT/90": "SoT/90",
                                "G/Sh": "G/Chutes",
                                "G/SoT": "G/SoT",
                                "Dist": "Dist. Média Finalizações",
                                "FK": "Chutes Falta",
                                "PK": "PK G",
                                "PKatt": "PK",
                                "xG": "xG",
                                "npxG": "npxG",
                                "npxG/Sh": "npxG/Chute",
                                "G-xG": "G-xG"})
            
        df["Chutes/90"] = df["Chutes/90"].round(1)
        df["SoT/90"] = df["SoT/90"].round(1)            
            
        df = df[["Equipe", "P", "G", "Chutes", "SoT", "%SoT", "Chutes/90", "SoT/90", "G/Chutes", "G/SoT", 
                 "Dist. Média Finalizações", "Chutes Falta", "PK","PK G", "xG", "npxG", "npxG/Chute", 
                 "G-xG"]]  # Selecionar as colunas desejadas

        # Configurações de estilo para congelar a terceira coluna
        #frozen_columns = {"Equipe": {"sticky": True}}   
            
        return df  # Adicione esta linha para retornar o dataframe após as manipulações
                  
############################################################################################################
############################################################################################################            
    elif selected_stat == "Estatísticas de Passes":
        html = pd.read_html(url, header=1)
        df = html[10]  # Obtendo o DataFrame de estatísticas
        df = df.rename(columns={"Squad": "Equipe",
                                "90s": "P",
                                "Cmp": "Passes Completos",
                                "Att": "Passes",
                                "Cmp%": "%Passes Completos",
                                "TotDist": "Dist. Total Passes",
                                "PrgDist": "Dist. Total Passes Progressivos",
                                "Cmp.1": "Passes Curtos Completos",
                                "Att.1": "Passes Curtos",
                                "Cmp%.1": "%Passes Curtos Completos",
                                "Cmp.2": "Passes Médios Completos",
                                "Att.2": "Passes Médios",
                                "Cmp%.2": "%Passes Médios Completos",
                                "Cmp.3": "Passes Longos Completos",
                                "Att.3": "Passes Longos",
                                "Cmp%.3": "%Passes Longos Completos",
                                "Ast": "A",
                                "xAG": "xAG",
                                "xA": "xA",
                                "A-xAG": "A-xAG",
                                "KP": "Passes Importantes",
                                "1/3": "Passes Terço Final",
                                "PPA": "Passes Área Adv.",
                                "CrsPA": "Cruzamentos",
                                "PrgP": "Passes Progressivos"})
            
                        
        df = df[["Equipe", "P", "Passes", "Passes Completos", "%Passes Completos", "Dist. Total Passes",
                 "Dist. Total Passes Prog.", "Passes Curtos", "Passes Curtos Completos",
                 "%Passes Curtos Completos", "Passes Médios", "Passes Médios Completos",
                 "%Passes Médios Completos", "Passes Longos", "Passes Longos Completos",
                 "%Passes Longos Completos", "A", "xAG", "xA", "A-xAG", "Passes Importantes",
                 "Passes Terço Final", "Passes Área Adv.", "Cruzamentos", "Passes Progressivos"]]  # Selecionar as colunas desejadas

        # Configurações de estilo para congelar a terceira coluna
        #frozen_columns = {"Equipe": {"sticky": True}}        
            
        return df  # Adicione esta linha para retornar o dataframe após as manipulações

############################################################################################################
############################################################################################################
    elif selected_stat == "Estatísticas de Tipos de Passes":
        html = pd.read_html(url, header=1)
        df = html[12]  # Obtendo o DataFrame de estatísticas
        df = df.rename(columns={"Squad": "Equipe",
                                "90s": "P",
                                "Att": "Passes",
                                "Live": "Passes em Jogo",
                                "Dead": "Passes Bola Parada",
                                "FK": "Passes Faltas",
                                "TB": "Passes Enfiados",
                                "Sw": "Inversões de Jogo",
                                "Crs": "Cruzamento",
                                "TI": "Laterais",
                                "CK": "Escanteios",
                                "In": "Escanteios Curva Dentro",
                                "Out": "Escanteios Curva Fora",
                                "Str": "Escanteios Reto",
                                "Cmp": "Passes Completos",
                                "Off": "Passes Impedimento",
                                "Blocks": "Passes Bloqueados"})
            
                        
        df = df[["Equipe", "P", "Passes", "Passes em Jogo", "Passes Bola Parada", "Passes Faltas",
                 "Passes Enfiados", "Inversões de Jogo", "Cruzamento", "Laterais", "Escanteios", 
                 "Escanteios Curva Dentro", "Escanteios Curva Fora", "Escanteios Reto", "Passes Completos", 
                 "Passes Impedimento", "Passes Bloqueados"]]  # Selecionar as colunas desejadas

        # Configurações de estilo para congelar a terceira coluna
        #frozen_columns = {"Equipe": {"sticky": True}}      
            
        return df  # Adicione esta linha para retornar o dataframe após as manipulações

############################################################################################################
############################################################################################################
    elif selected_stat == "Estatísticas de Gols e Criação de Chances de Gol":
        html = pd.read_html(url, header=1)
        df = html[14]  # Obtendo o DataFrame de estatísticas
        df = df.rename(columns={"Squad": "Equipe",
                                "90s": "P",
                                "SCA": "Ações Criação Chutes",
                                "SCA90": "Ações Criação Chutes/90",
                                "PassLive": "Passes em Jogo para Chutes",
                                "PassDead": "Passes Bola Parada para Chutes",
                                "TO": "Dribles para Chutes",
                                "Sh": "Chutes para Chutes",
                                "Fld": "Faltas para Chutes",
                                "Def": "Ações Defensivas para Chutes",
                                "GCA": "Ações Criação Gols",
                                "GCA90": "Ações Criação Gols/90",
                                "PassLive": "Passes em Jogo para Gols",
                                "PassDead": "Passes Bola Parada para Gols",
                                "TO": "Dribles para Gols",
                                "Sh": "Chutes para Chutes para Gols",
                                "Fld": "Faltas para Gols",
                                "Def": "Ações Defensivas para Gols"})
            
        df["Ações Criação Chutes/90"] = df["Ações Criação Chutes/90"].round(1)
        df["Ações Criação Gols/90"] = df["Ações Criação Gols/90"].round(1)
            
        df = df[["Equipe", "P", "Ações Criação Chutes", "Ações Criação Chutes/90", "Passes em Jogo para Chutes", 
                 "Passes Bola Parada para Chutes", "Dribles para Chutes", "Chutes para Chutes", 
                 "Faltas para Chutes", "Ações Defensivas para Chutes", "Ações Criação Gols", 
                 "Ações Criação Gols/90", "Passes em Jogo para Gols", "Passes Bola Parada para Gols", 
                 "Dribles para Gols", "Chutes para Chutes para Gols", "Faltas para Gols", 
                 "Ações Defensivas para Gols"]]  # Selecionar as colunas desejadas

        # Configurações de estilo para congelar a terceira coluna
        #frozen_columns = {"Equipe": {"sticky": True}}
            
        return df  # Adicione esta linha para retornar o dataframe após as manipulações

############################################################################################################
############################################################################################################
    elif selected_stat == "Estatísticas Defensivas":
        html = pd.read_html(url, header=1)
        df = html[16]  # Obtendo o DataFrame de estatísticas
        df = df.rename(columns={"Squad": "Equipe",
                                "90s": "P",
                                "Tkl": "Desarmes",
                                "TklW": "Desarmes Ganhos",
                                "Def 3rd": "Desarmes Terço Def.",
                                "Mid 3rd": "Desarmes Terço Central",
                                "Att 3rd": "Desarmes Terço Final",
                                "Tkl": "Dribles A Desarmados",
                                "Att": "Dribles A",
                                "Tkl%": "%Dribles A Desarmados",
                                "Lost": "Dribles A Sofridos",
                                "Blocks": "Bloqueios",
                                "Sh": "Chutes Bloqueados",
                                "Pass": "Passes Bloqueados",
                                "Int": "Cortes",
                                "Tkl+Int": "Cortes + Desarmes",
                                "Clr": "Rebatida",
                                "Err": "Erros Defensivos"})
            
                        
        df = df[["Equipe", "P", "Desarmes", "Desarmes Ganhos", "Desarmes Terço Def.", "Desarmes Terço Central", 
                 "Desarmes Terço Final", "Dribles A", "Dribles A Desarmados", "Dribles A Sofridos", 
                 "%Dribles A Desarmados", "Bloqueios", "Chutes Bloqueados", "Passes Bloqueados", "Cortes", 
                 "Cortes + Desarmes", "Rebatida", "Erros Defensivos"]]  # Selecionar as colunas desejadas

        # Configurações de estilo para congelar a terceira coluna
        #frozen_columns = {"Equipe": {"sticky": True}}
            
        return df  # Adicione esta linha para retornar o dataframe após as manipulações

############################################################################################################
############################################################################################################
    elif selected_stat == "Estatísticas de Posse de Bola":
        html = pd.read_html(url, header=1)
        df = html[18]  # Obtendo o DataFrame de estatísticas
        df = df.rename(columns={"Squad": "Equipe",
                                "Poss": "Posse de Bola Média",
                                "90s": "P",
                                "Touches": "Toques na Bola",
                                "Def Pen": "Toques na Área Def.",
                                "Def 3rd": "Toques Terço Def.",
                                "Mid 3rd": "Toques Terço Central",
                                "Att 3rd": "Toques Terço Final",
                                "Att Pen": "Toques na Área Ofe.",
                                "Live": "Toques em Jogo",
                                "Att": "Dribles",
                                "Succ": "Dribles Bem Sucedidos",
                                "Succ%": "%Dribles Bem Sucedidos",
                                "Tkld": "Dribles Desarmados",
                                "Tkld%": "%Dribles Desarmados",
                                "Carries": "Conduções",
                                "TotDist": "Dist. Total Conduções",
                                "PrgDist": "Dist. Total Conduções Progressivas",
                                "PrgC": "Conduções Progressivas",
                                "1/3": "Conduções Terço Final",
                                "CPA": "Conduções Área",
                                "Mis": "Perda de Bola",
                                "Dis": "Desarmes A",
                                "Rec": "Passes Recebidos",
                                "PrgR": "Passes Progressivos Recebidos"})
            
                        
        df = df[["Equipe", "Posse de Bola Média", "P", "Toques na Bola", "Toques na Área Def.", 
                 "Toques Terço Def.", "Toques Terço Central", "Toques Terço Final", "Toques na Área Ofe.", 
                 "Toques em Jogo", "Dribles", "Dribles Bem Sucedidos", "%Dribles Bem Sucedidos", 
                 "Dribles Desarmados", "%Dribles Desarmados", "Conduções", "Dist. Total Conduções", 
                 "Dist. Total Conduções Progressivas", "Conduções Progressivas", "Conduções Terço Final", 
                 "Conduções Área", "Perda de Bola", "Desarmes A", "Passes Recebidos", 
                 "Passes Progressivos Recebidos"]]  # Selecionar as colunas desejadas

        # Configurações de estilo para congelar a terceira coluna
        #frozen_columns = {"Equipe": {"sticky": True}}
            
        return df  # Adicione esta linha para retornar o dataframe após as manipulações

############################################################################################################
############################################################################################################
    elif selected_stat == "Estatísticas de Tempo de Jogo":
        html = pd.read_html(url, header=1)
        df = html[20]  # Obtendo o DataFrame de estatísticas
        df = df.rename(columns={"Squad": "Equipe",
                                "Age": "Idade Média",
                                "MP": "P",
                                "Mn/Start": "Min./Início",
                                "Subs": "Substituições",
                                "Mn/Sub": "Min./Substituição",
                                "PPM": "P/90",
                                "onG": "G",
                                "onGA": "GA",
                                "+/-": "+/-",
                                "+/-90": "+/-/90",
                                "onxG": "xG",
                                "onxGA": "xGA",
                                "xG+/-": "+/- xG",
                                "xG+/-90": "+/- xG/90"})
            
                        
        df = df[["Equipe", "Idade Média", "P", "Min./Início", "Substituições", "Min./Substituição", "P/90", "G", 
                 "GA", "+/-", "+/-/90", "xG", "xGA", "+/- xG", "+/- xG/90"]]  # Selecionar as colunas desejadas

        # Configurações de estilo para congelar a terceira coluna
        #frozen_columns = {"Equipe": {"sticky": True}}
            
        return df  # Adicione esta linha para retornar o dataframe após as manipulações    

############################################################################################################
############################################################################################################
    elif selected_stat == "Estatísticas Diversas":
        html = pd.read_html(url, header=1)
        df = html[22]  # Obtendo o DataFrame de estatísticas
        df = df.rename(columns={"Squad": "Equipe",
                                "90s": "P",
                                "CrdY": "Amarelos",
                                "CrdR": "Vermelhos",
                                "2CrdY": "2 Amarelos",
                                "Fls": "Faltas Cometidas",
                                "Fld": "Faltas Sofridas",
                                "Off": "Impedimentos",
                                "Crs": "Cruzamentos",
                                "Int": "Cortes",
                                "TklW": "Desarmes Ganhos",
                                "PKwon": "G Penaltis",
                                "PKcon": "G Penaltis A",
                                "OG": "OG",
                                "Recov": "Recuperação",
                                "Won": "Disp. Aéreas Ganhas",
                                "Lost": "Disp. Aéreas Perdidas",
                                "Won%": "%Disp. Aéreas Ganhas"})
            
                        
        df = df[["Equipe", "P", "Amarelos", "Vermelhos", "2 Amarelos", "Faltas Cometidas", "Faltas Sofridas", 
                 "Impedimentos", "Cruzamentos", "Cortes", "Desarmes Ganhos", "G Penaltis", "G Penaltis A", 
                 "OG", "Recuperação", "Disp. Aéreas Ganhas", "Disp. Aéreas Perdidas", "%Disp. Aéreas Ganhas"]]  # Selecionar as colunas desejadas

        # Configurações de estilo para congelar a terceira coluna
        #frozen_columns = {"Equipe": {"sticky": True}}
            
        return df  # Adicione esta linha para retornar o dataframe após as manipulações  

    else:
        html = pd.read_html(url, header=1)
        df = html[ass_key[0]]
        raw = df.reset_index(drop=True)
        raw = raw.fillna(0)
        playerstats = raw
        return playerstats

playerstats = load_data(selected_year)


# Sidebar - Team selection
sorted_unique_team = sorted(playerstats.Equipe.unique())
selected_team = st.sidebar.multiselect('Equipe', sorted_unique_team, sorted_unique_team)

# # Sidebar - Position selection
# unique_pos = ['RB','QB','WR','FB','TE']
# selected_pos = st.sidebar.multiselect('Position', unique_pos, unique_pos)

# # Filtering data
#df_selected_team = playerstats[(playerstats.Equipe.isin(selected_team))] #original
df_selected_team = playerstats[(playerstats.Equipe.isin(selected_team))]

st.markdown(f"* **Ano:** {selected_year} ")

st.markdown(f"* **Estatística:** {selected_stat} ")

if selected_stat == "Classificação":
    st.markdown(f"* **Cálculo xPts:** Partidas * 3 * (xG^1.536) / ((xG^1.536) + (xGA^1.536))")

#st.write(df_selected_team) #original
st.write(df_selected_team)


@st.cache_resource
def get_pyg_renderer() -> "StreamlitRenderer":
    df = df_selected_team
    return StreamlitRenderer(df, spec="./gw_config.json", debug=False)

if st.button("Criar Visualização com esses dados"):
    renderer = get_pyg_renderer()
    renderer.render_explore(width=None)
