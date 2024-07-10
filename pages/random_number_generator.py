from streamlit_cookies_controller import CookieController
from streamlit_local_storage import LocalStorage
import streamlit as st
import pandas as pd
import numpy as np

# Initialize CookieController and LocalStorage early
if 'cookies' not in st.session_state:
    st.session_state['cookies'] = {}

if 'guest' not in st.session_state:
    st.session_state.guest = {}

# Inisialisasi CookieController
controller = CookieController()
localS = LocalStorage()

def generate_mixed(a, n, z0, c, m, jumlah_iterasi):
    random_number = {}
    increment = []
    zi_min_1 = []
    zi = []
    ui = []
    for i in range(1, jumlah_iterasi):
        increment.append(i)
        random_number['i'] = increment
        if i == 1:
            zi_min_1.append(z0)  # Konversi z0 ke int
        else:
            zi_min_1.append(zi[i-2])  # Konversi zi[i-2] ke int
        random_number['Zi-1'] = zi_min_1
        zi.append(((a**n * zi_min_1[i-1]) + ((a**n - 1)/(a - 1)) * c) % m)
        random_number['Zi'] = zi
        ui.append(zi[i-1]/m)
        random_number['Ui'] = ui

    return random_number

def save_to_local_storage(cookie_name, random_number):
    
    # Konversi semua nilai dalam dictionary ke tipe data Python standar
    def convert_values(obj):
        if isinstance(obj, dict):
            return {k: convert_values(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [convert_values(i) for i in obj]
        elif isinstance(obj, pd.Series):
            return obj.tolist()
        elif isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        else:
            return obj

    random_number = convert_values(random_number)
    localS.setItem(cookie_name, random_number)

def save_parameter_rng(cookie_name, params):
    
    controller.set(cookie_name, params)

def main():
    st.title("Random Number Generator")
    st.caption('_Note:_ Untuk keperluan simulasi wajib pilih kolom')

    frequency_table = controller.get('Frequency Table')

    selected_column = None
    if frequency_table:

        ready = False
        for key in list(frequency_table.keys()):
            print(key)
            if controller.get(key):
                ready = True
            else:
                ready = False
                break
        
        if ready:        
            st.info("Angka acak sudah di siapkan")

        st.subheader("Generate berdasarkan: ")
        
        # Pilihan kolom dalam select box
        selected_column = st.selectbox("Pilih Kolom:", list(frequency_table.keys()))

    else:
        st.warning("Data di tahap persiapan, belum di siapkan. Silahkan isi terlebih dahulu data persiapan untuk kebutuhan simulasi. Jika tidak abaikan..")
    

    df = pd.DataFrame(
            [
                {"a": 300, "n": 2, "Z0": 10122004, "c": 2024, "m": 2221, "Jumlah Iterasi": 300}
            ]
        )

    edited_df = st.data_editor(df, hide_index=True)

    if st.button("Generate"):
        st.success("Random number berhasil disimpan")
        a = edited_df.at[0, 'a']
        n = edited_df.at[0, 'n']
        z0 = edited_df.at[0, 'Z0']
        c = edited_df.at[0, 'c']
        m = edited_df.at[0, 'm']
        jumlah_iterasi = edited_df.at[0, 'Jumlah Iterasi']
        random_number = generate_mixed(a, n, z0, c, m, jumlah_iterasi)

        save_parameter_rng(selected_column, edited_df.to_dict())
        save_to_local_storage(selected_column, random_number)

        #pilihan jika hanya ingin generate angka acak saja tanpa simulasi
        st.session_state["guest"] = random_number

    st.write("Hasil Generate:")
    if selected_column:
        get_random_number_saved = localS.getItem(selected_column)
        get_rng_params = controller.get(selected_column)
        if get_rng_params:
            st.dataframe(get_rng_params, hide_index=True)
        if get_random_number_saved:
            st.dataframe(get_random_number_saved, width=700, hide_index=True)
            df = pd.DataFrame(get_random_number_saved)
            duplikat_kolom = df[df.duplicated('Ui', keep=False)]
            if not duplikat_kolom.empty:
                st.error("Duplikat data")
    else:
        st.dataframe(st.session_state["guest"], width=700)
    
            
                
    
    # if st.button("Refresh"):
    #     st.markdown(
    #     """<button onclick="window.location.reload();">Refresh</button>""",
    #     unsafe_allow_html=True
    # )

if __name__ == "__main__":
    main()

