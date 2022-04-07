import streamlit as st
import pickle
import pandas as pd
import numpy as np
import sklearn
from sklearn.decomposition import TruncatedSVD
from sklearn.neighbors import NearestNeighbors


def load_corr_matrix():
    with open('correlation_matrix.pkl', 'rb') as file:
        corrmat = pickle.load(file)
        return corrmat


corrmat_model = load_corr_matrix()


def load_df():
    game_dataframe = pd.read_csv('game_data_clean.csv', index_col=0)
    return game_dataframe


game_data = load_df()


def show_rec_page():
    game_names = game_data.Name.to_list()
    game_ids = pd.Index(data=game_data.BGGId, copy=True)
    game_ids = game_ids.drop_duplicates(keep='first')

    st.title("Boardgame Recommender")
    st.write("""### Search for a game name that you like and then choose features of the game you're looking for. """)

    input_game = st.selectbox('Type to search for a game you like and select it from the drop down list.', game_names)
    st.subheader('Choose the game features you want to find.')
    game_complexity = st.slider("Game Complexity/Difficulty", min_value=0.0, max_value=5.0, value=0.0, step=0.5)
    max_players = st.slider("Max Number Of Players (1-12 or 13+)", min_value=1, max_value=13, value=1)
    mfg_playtime = st.slider("Average Playtime In Minutes", min_value=10, max_value=120, value=10, step=10)
    mfg_age = st.slider("Recommended Minimum Age", min_value=0, max_value=18, value=0, step=2)

    button_click = st.button("Recommend Game")
    if button_click:
        input_game_index = game_data[game_data['Name'] == input_game].index
        input_features = [game_complexity, max_players, mfg_playtime, mfg_age]

        # Get all correlation values of games based on user chosen game.
        calc_rec = corrmat_model[input_game_index]
        calc_rec = calc_rec[0]
        # Get a dataframe of all games that have a correlation score less than 1 (which is the user selected game)
        # and above .8 (roughly a B rating).
        possible_games = game_data[game_data['BGGId'].isin(list(game_ids[(calc_rec < .999999) & (calc_rec > 0.8)]))]
        #print(possible_games)
        # Calculate nearest neighbor values from the possible games list.
        X = possible_games.iloc[:, [7, 10, 11, 12]].values
        nbrs = NearestNeighbors(n_neighbors=3).fit(X)
        nbrs_tuple = nbrs.kneighbors([input_features])
        # Grab game indices from tuple.
        rec_game_indices = list(nbrs_tuple[1][0])
        # Filter out recommended games from dataframe
        games_to_recommend = possible_games.iloc[rec_game_indices]

        # create display columns and values
        col1, col2, col3 = st.columns(3)

        with col1:
            st.subheader(games_to_recommend.Name.iloc[0])
            st.image(games_to_recommend.ImagePath.iloc[0])
            st.text(f'Game Complexity: {games_to_recommend.GameWeight.iloc[0]}')
            st.text(f'Max Players: {games_to_recommend.MaxPlayers.iloc[0]}')
            st.text(f'Avg Playtime: {games_to_recommend.MfgPlaytime.iloc[0]}')
            st.text(f'Minimum Age: {games_to_recommend.MfgAgeRec.iloc[0]}')

        with col2:
            st.subheader(games_to_recommend.Name.iloc[1])
            st.image(games_to_recommend.ImagePath.iloc[1])
            st.text(f'Game Complexity: {games_to_recommend.GameWeight.iloc[1]}')
            st.text(f'Max Players: {games_to_recommend.MaxPlayers.iloc[1]}')
            st.text(f'Avg Playtime: {games_to_recommend.MfgPlaytime.iloc[1]}')
            st.text(f'Minimum Age: {games_to_recommend.MfgAgeRec.iloc[1]}')

        with col3:
            st.subheader(games_to_recommend.Name.iloc[2])
            st.image(games_to_recommend.ImagePath.iloc[2])
            st.text(f'Game Complexity: {games_to_recommend.GameWeight.iloc[2]}')
            st.text(f'Max Players: {games_to_recommend.MaxPlayers.iloc[2]}')
            st.text(f'Avg Playtime: {games_to_recommend.MfgPlaytime.iloc[2]}')
            st.text(f'Minimum Age: {games_to_recommend.MfgAgeRec.iloc[2]}')

