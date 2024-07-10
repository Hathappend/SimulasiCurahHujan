import streamlit as st
import pandas as pd
import numpy as np
from streamlit_cookies_controller import CookieController
from streamlit_local_storage import LocalStorage

# Inisialisasi CookieController
controller = CookieController()
localS = LocalStorage()

# Fungsi untuk menghitung tabel frekuensi
def calculate_frequency_table(data, column_names):
    frequency_tables = {}
    for column in column_names:
        frequency_table = data[column].value_counts().reset_index()
        frequency_table.columns = [column, 'Frekuensi']
        frequency_tables[column] = frequency_table
    return frequency_tables

def probabilitas(dataFrekuensi):
    df_frekuensi = pd.DataFrame(dataFrekuensi)
    total_frekuensi = df_frekuensi['Frekuensi'].sum()
    df_frekuensi['Probabilitas'] = df_frekuensi['Frekuensi'] / total_frekuensi
    df_frekuensi['Probabilitas Kumulatif'] = np.ceil(df_frekuensi['Probabilitas'].cumsum() * 100)
   
    return df_frekuensi

def kemunculanAngkaAcak(dataFrekuensi):
    df_frekuensi = pd.DataFrame(dataFrekuensi)
    total_frekuensi = df_frekuensi['Frekuensi'].sum()
    df_frekuensi['Probabilitas Kumulatif'] = np.ceil((df_frekuensi['Frekuensi'] / total_frekuensi).cumsum() * 100)
    
    # Menghitung interval angka acak dimulai dari 1-100
    interval_awal = df_frekuensi['Probabilitas Kumulatif'].shift(fill_value=0).astype(int) + 1
    interval_akhir = df_frekuensi['Probabilitas Kumulatif'].astype(int)
    interval_akhir.iloc[-1] = 100  # Pastikan batas atas terakhir adalah 100
    df_frekuensi['Interval Angka Acak'] = np.where(interval_awal == interval_akhir,
                                                     interval_awal.astype(str),
                                                     interval_awal.astype(str) + "-" + interval_akhir.astype(str))
    return df_frekuensi

# Fungsi untuk upload file
def uploaded_file(uploadedFile):
    data = None

    if uploadedFile is not None:
        # Baca file yang diupload
        if uploadedFile.name.endswith(".csv"):
            data = pd.read_csv(uploadedFile)
        elif uploadedFile.name.endswith(".xlsx"):
            data = pd.read_excel(uploadedFile)
        
    return data 

# Fungsi untuk save data
def save(frequency_tables):
    saved_frequency_tables = {}
    for column, frequency_table in frequency_tables.items():
        saved_frequency_tables[column] = frequency_table.to_dict()
    controller.set('Frequency Table', saved_frequency_tables)

# Fungsi untuk mengambil data
def getData(cookie_name):
    get = controller.get(cookie_name)
    if get:
        return get
    return None

def show(data, show_type):
    columns = st.columns(2)
    for i, (column, frequency_table) in enumerate(data.items()):
        if show_type == "frequency":
            with columns[i % 2]:
                st.dataframe(frequency_table, hide_index=True)
        elif show_type == "probability":
            st.dataframe(probabilitas(frequency_table), hide_index=True)
        elif show_type == "interval":
            st.dataframe(kemunculanAngkaAcak(frequency_table), hide_index=True)
        elif show_type == "rng":
            st.write(f'Tabel Angka Acak untuk {column} dengan parameter:')
            st.dataframe(controller.get(column))
            st.dataframe(localS.getItem(column), width=700)

def main():

    st.title("File Upload dan Tabel Frekuensi")

    # Upload file
    uploadedFile = None

    # Menampilkan data (Tabel Frekuensi) yang disimpan dalam cookie jika ada
    saved_frequency_tables = getData("Frequency Table")
    if saved_frequency_tables:
        st.file_uploader("Upload file CSV atau Excel", type=["csv", "xlsx"], accept_multiple_files=False, disabled=True)
        st.write("Data telah di siapkan")
        with st.expander("Tabel Frekuensi"):
            show(saved_frequency_tables, "frequency")
        with st.expander("Tabel Probabilitas"):
            show(saved_frequency_tables, "probability")
        with st.expander("Tabel Interval Angka Acak"):
            show(saved_frequency_tables, "interval")
        with st.expander("Tabel Angka Acak"):
            find = False
            for key in list(saved_frequency_tables.keys()):
                if controller.get(key):
                    find = True
                else:
                    find = False
                    st.warning(f'Angka acak belum lengkap, dibutuhkan angka acak "{key}" ')
                    break

            if find:    
                show(saved_frequency_tables, "rng")
            
    else:
        uploadedFile = st.file_uploader("Upload file CSV atau Excel", type=["csv", "xlsx"], accept_multiple_files=False)
            
        

    data = uploaded_file(uploadedFile)
    if data is not None:
        st.write("Data yang diupload:")
        st.write(data)

        # Pilih kolom untuk perhitungan tabel frekuensi
        column_names = st.multiselect("Pilih kolom untuk perhitungan tabel frekuensi", data.columns)

        if column_names:
            frequency_tables = calculate_frequency_table(data, column_names)
            show(frequency_tables, "frequency")

            # Tombol untuk menyimpan data ke dalam cookie
            if st.button("Save"):
                save(frequency_tables)
                st.success("Data berhasil di simpan")

                if st.button("Refresh"):
                    st.markdown(
                    """<button onclick="window.location.reload();">Refresh</button>""",
                    unsafe_allow_html=True
                )

if __name__ == "__main__":
    main()


