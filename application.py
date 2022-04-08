import streamlit as st
from recommender import show_rec_page
from visual_data import visual_data


def main():
    st.set_page_config(page_title='Board Gameporium', page_icon=':game_die:')

    show_rec_page()
    visual_data()


if __name__ == '__main__':
    main()

