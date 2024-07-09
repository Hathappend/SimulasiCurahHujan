import streamlit as st
import importlib
import pages.requirements_step as requirements_step
import pages.random_number_generator as rng

if 'reload_done' not in st.session_state:
    st.session_state.reload_done = False

def main():

    st.sidebar.title("Model Dan Simulasi")
    selected_tab = st.sidebar.radio("Menu", ["Tahap Persiapan","Generator Bilangan Acak","Simulasi"])

    if selected_tab == "Tahap Persiapan":
        importlib.reload(requirements_step)
        requirements_step.main()
    elif selected_tab == "Generator Bilangan Acak":
        if not st.session_state.reload_done:
            importlib.reload(rng)
            st.session_state.reload_done = True
        rng.main()


if __name__ == "__main__":
    main()
