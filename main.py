import streamlit as st
import importlib
import pages.requirements_step as requirements_step
import pages.random_number_generator as rng

if 'reload_rng' not in st.session_state:
    st.session_state.reload_rng = False
# if 'requirements_step' not in st.session_state:
#     st.session_state.reload_requirements_step = False

def main():

    st.sidebar.title("Model Dan Simulasi")
    selected_tab = st.sidebar.radio("Menu", ["Tahap Persiapan","Generator Bilangan Acak","Simulasi"])

    if selected_tab == "Tahap Persiapan":
        importlib.reload(rng)
        requirements_step.main()
    elif selected_tab == "Generator Bilangan Acak":
        if not st.session_state.reload_rng:
            importlib.reload(rng)
            st.session_state.reload_rng = True
        rng.main()


if __name__ == "__main__":
    main()
