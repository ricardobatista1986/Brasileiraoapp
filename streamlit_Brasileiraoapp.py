import streamlit as st
import pandas as pd
import base64
from pygwalker.api.streamlit import StreamlitRenderer, init_streamlit_comm
from pygwalker import GlobalVarManager

#GlobalVarManager.set_kanaries_api_key(st.secrets["api_key"])

st.set_page_config(layout="wide")
st.title('Brasileirão Série A - Estatísticas')

st.markdown("""
Este app realiza web scraping dos dados estatísticos das equipes do Brasileirão Série A e possibilita a visualização utilizando o PygWalker.
* **Fonte:** fBref.com
""")

# Establish communication between pygwalker and streamlit
init_streamlit_comm()

#sidebar for user input features
st.sidebar.header('User Input Features')
selected_year = st.sidebar.selectbox('Ano', list(reversed(range(2014,2024))))

# Dict for type of stats 
league_data = {
    0: "League Standings",
    2: "Squad Stats",
    4: "GK Stats",
    6: "Squad Advanced Stats",
    8: "Shooting Stats",
    10: "Passing Stats",
    12: "Pass Types Stats",
    14: "Goals and Shot Creation Stats",
    16: "Defensive Stats",
    18: "Possesion Stats",
    20: "Game Time Stats",
    22: "Miscellanius Stats",
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
    if selected_stat == "League Standings":
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
                                "Pts/MP": "Pts/90",
                                "Top Team Scorer": "Artilheiro"})

        df["xPts"] = (df["P"] * 3 * ((df["xG"]**1.536) / ((df["xG"]**1.536) + (df["xGA"]**1.536))))
        df[["xPts"]] = df[["xPts"]].round(1)

        df['Pts-xPts'] = df['Pts'] - df['xPts']
        df['Pts-xPts'] = df['Pts-xPts'].round(1)

        df = df[["Cl", "Equipe", "P", "V", "E", "D", "G", "GA", "GD", "Pts", "Pts/90", "xG", "xGA", "xGD",
                 "xPts", "Pts-xPts", "Artilheiro"]]  # Selecionar as colunas desejadas

        # Configurações de estilo para congelar a primeira coluna
        frozen_columns = {"Equipe": {"sticky": True}}
        return df  # Adiciona esta linha para retornar o DataFrame

    else:
        html = pd.read_html(url, header=1)
        df = html[ass_key[0]]
        raw = df.reset_index(drop=True)
        raw = raw.fillna(0)
        playerstats = raw
        return playerstats
        playerstats = load_data(selected_year)


# Sidebar - Team selection
sorted_unique_team = sorted(playerstats.Squad.unique())
selected_team = st.sidebar.multiselect('Equipe', sorted_unique_team, sorted_unique_team)

# # Filtering data
df_selected_team = playerstats[(playerstats.Squad.isin(selected_team))]

st.markdown(f"* **Ano:** {selected_year} ")
st.markdown(f"* **Estatística:** {selected_stat} ")
st.write(df_selected_team)

@st.cache_resource
def get_pyg_renderer() -> "StreamlitRenderer":
    df = df_selected_team
    return StreamlitRenderer(df, spec="./gw_config.json", debug=False)

if st.button("Criar Visualização com esses dados"):
    renderer = get_pyg_renderer()
    renderer.render_explore(width=None)
