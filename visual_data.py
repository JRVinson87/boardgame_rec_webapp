import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import recommender


def hist_plot():
    st.subheader("Average Rating count/distribution.")
    fig = plt.figure(figsize=(6, 6))
    sns.histplot(data=recommender.game_data, x="AvgRating")
    st.pyplot(fig)


def count_plot():
    st.subheader("Counts of Play times, Age Recommendations, Minimum Players, and Max Players.")
    fig, ax = plt.subplots(2, 2, figsize=(12, 12))

    cp0 = sns.countplot(x=recommender.game_data['MfgPlaytime'], ax=ax[0][0]);
    cp0.set_xticklabels(cp0.get_xticklabels(), rotation=65, horizontalalignment='right');

    cp1 = sns.countplot(x=recommender.game_data['MfgAgeRec'], ax=ax[0][1]);
    cp1.set_xticklabels(cp1.get_xticklabels(), rotation=45, horizontalalignment='right');

    cp2 = sns.countplot(x=recommender.game_data['MinPlayers'], ax=ax[1][0]);

    cp3 = sns.countplot(x=recommender.game_data['MaxPlayers'].map(lambda x: min(x, 20)), ax=ax[1][1]);
    cp3.set_xticklabels(cp3.get_xticklabels(), rotation=45, horizontalalignment='right');

    st.pyplot(fig)


def scat_plot():
    st.subheader('Game complexity/difficulty vs Rating')
    fig, ax = plt.subplots(figsize=(6, 6))
    sns.scatterplot(data=recommender.game_data, x='GameWeight', y='AvgRating');
    st.pyplot(fig)


def heat_map():
    st.subheader('Heatmap of feature correlations.')
    df_heatmap = recommender.game_data[['NumOwned', 'YearPublished', 'GameWeight', 'AvgRating',
                            'MinPlayers', 'MaxPlayers', 'MfgPlaytime', 'MfgAgeRec']].copy()
    fig = plt.figure(figsize=(10, 10))
    sns.heatmap(df_heatmap.corr(), annot=True, fmt='.2f', annot_kws={"size": 12});
    st.pyplot(fig)


def visual_data():
    st.title("Visualized Board Game Data")
    st.write("Last update: 04/2022")

    hist_plot()
    count_plot()
    scat_plot()
    heat_map()

