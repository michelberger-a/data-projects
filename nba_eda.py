import streamlit as st
import pandas as pd
import base64
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from datetime import date

title_year = date.today().year + 1
st.title(f'NBA Player Stats Explorer 2000-{title_year}')

st.markdown("""
Will perform web-scraping of NBA Player Stats over multiple seasons!
* **Data Source:** [Basketball-reference.com](https://www.basketball-reference.com/)            
""")

st.sidebar.header('Input Features')

# select year for data to investigate
# this is unique select
current_year = date.today().year + 2
selected_year = st.sidebar.selectbox('Year',
                                     list(reversed(range(2000, current_year)))) # reverse shows most recent years first

# web scrape the data stats
@st.cache_data
def load_data(year):
    url = "https://www.basketball-reference.com/leagues/NBA_" + (f"{year}") + "_per_game.html"
    html = pd.read_html(url, header = 0)
    df = html[0]
    raw = df.drop(df[df.Age == "Age"].index) # delete repeating
    raw = raw.fillna(0)
    playerstats = raw.drop(['Rk'], axis=1)
    return playerstats
playerstats = load_data(selected_year)

# back to sidebar to select the team
sorted_unique_team = playerstats.Team.unique().tolist()
sorted_unique_team.remove(0)
sorted_unique_team.sort()
selected_team = st.sidebar.multiselect('Team', sorted_unique_team, sorted_unique_team)

# select position on sidebar
unique_pos = ['C', "PF", "SF", "PG", "SG"]
selected_pos = st.sidebar.multiselect("Position", unique_pos, unique_pos)

# filter data
df_selected_team = playerstats[(playerstats.Team.isin(selected_team)) & (playerstats.Pos.isin(selected_pos))]
df_selected_team = df_selected_team.sort_values('Player')

st.header("Show Player Stats of Selected Team(s) and Position(s)")
st.write("Data Dimension: " + str(df_selected_team.shape[0]) + " rows and " + str(df_selected_team.shape[1]) + " columns.")
# prints out the actual dataframe of players and stats
st.dataframe(df_selected_team)


# download the nba player stats data
def filedownload(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode() # string to byte conversion
    href = f'<a href="data:file/csv;base64,{b64}" download="playerstats.csv">Download CSV File</a>'
    return href

st.markdown(filedownload(df_selected_team), unsafe_allow_html=True)


# next steps: add an awards winner 
with st.expander('Player Awards', icon = "🏆"):

    mvp10 = playerstats[playerstats.Awards.str.contains('MVP-10', case=False, regex=True).fillna(False)].index
    mvp = playerstats.drop(mvp10)
    mvp = mvp[mvp.Awards.str.contains("mvp-1", case=False, regex=True).fillna(False)]["Player"]

    dpoy10 = playerstats[playerstats.Awards.str.contains('DPOY-10', case=False, regex=True).fillna(False)].index
    dpoy = playerstats.drop(dpoy10)
    dpoy = dpoy[dpoy.Awards.str.contains("dpoy-1", case=False, regex=True).fillna(False)]["Player"]

    roy10 = playerstats[playerstats.Awards.str.contains('ROY-10', case=False, regex=True).fillna(False)].index
    roy = playerstats.drop(roy10)
    roy = roy[roy.Awards.str.contains("roy-1", case=False, regex=True).fillna(False)]["Player"]

    mip10 = playerstats[playerstats.Awards.str.contains('MIP-10', case=False, regex=True).fillna(False)].index
    mip = playerstats.drop(mip10)
    mip = mip[mip.Awards.str.contains("mip-1", case=False, regex=True).fillna(False)]["Player"]
    

    st.markdown("**MVP:** " + mvp.values[0])
    st.markdown("**DPOY:** " + dpoy.values[0])
    st.markdown("**ROY:** " + roy.values[0])
    st.markdown("**MIP:** " + mip.values[0])


# create the heat map
# need to export and re-import because cannot print a seaborn map right to streamlit
if st.button("Intercorrelation Heatmap"):
    st.header("Intercorrelation Matrix Heatmap")
    df_selected_team.to_csv('output.csv',index=False)
    df = pd.read_csv('output.csv')

    df = df.iloc[:, 4:-1]

    corr = df.corr()
    mask = np.zeros_like(corr)
    mask[np.triu_indices_from(mask)] = True
    with sns.axes_style("white"):
        fig, ax = plt.subplots(figsize=(7, 5))
        ax = sns.heatmap(corr, mask = mask, vmax=1, square=True)
    st.pyplot(fig)



