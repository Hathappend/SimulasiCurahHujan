import streamlit as st
import importlib
import pages.requirements_step as requirements_step
import pages.random_number_generator as rng
import pages.simulasi as simulasi

st.set_page_config(layout="wide")

def main():

    if "frequency_tables" not in st.session_state:
        st.session_state['frequency_tables'] = {}
        
    # for key in st.session_state['frequency_tables'].keys():
    #     st.session_state[f'{key}_random_numbers'] = {}

    #initialisasi session
    if 'guest' not in st.session_state:
        st.session_state.guest = {}

    st.sidebar.title("Model Dan Simulasi")
    selected_tab = st.sidebar.radio("Menu", ["Tahap Persiapan","Generator Bilangan Acak","Simulasi"])

    if selected_tab == "Tahap Persiapan":
        requirements_step.main()
    elif selected_tab == "Generator Bilangan Acak":
        rng.main()
    elif selected_tab == "Simulasi" :
        simulasi.main()


if __name__ == "__main__":
    main()
