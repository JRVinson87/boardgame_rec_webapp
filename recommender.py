import streamlit as st
import pickle
import numpy as np
import sklearn
from sklearn.decomposition import TruncatedSVD
from sklearn.neighbors import NearestNeighbors


def load_corr_matrix():
    with open('correlation_matrix.pkl', 'rb') as file:
        corrmat = pickle.load(file)
        return corrmat


corrmat_model = load_corr_matrix()


def load_nbrs_model():
    with open('nbrs_model.pkl', 'rb') as file:
        nbrs_pkl = pickle.load(file)
        return nbrs_pkl


nbrs_model = load_nbrs_model()


def show_rec_page():
    st.title("Boardgame Recommender")
    st.write("""### Enter a game you love. """)
    #input_game = st.selectbox('Enter your favorite game.', )
