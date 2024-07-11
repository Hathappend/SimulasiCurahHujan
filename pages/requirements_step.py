import streamlit as st
import pandas as pd
import numpy as np


def init():

    #Inisialisasi session
    if 'frequency_tables' not in st.session_state:
        st.session_state['frequency_tables'] = {}


# Fungsi untuk menghitung tabel frekuensi
def calculate_frequency_table(data, column_names):
    frequency_tables = {}
    for column in column_names:
        frequency_table = data[column].value_counts().reset_index()
        frequency_table.columns = [column, 'Frekuensi']
        frequency_tables[column] = frequency_table
    return frequency_tables

#mencari probabilitas
def probabilitas(dataFrekuensi):
    df_frekuensi = pd.DataFrame(dataFrekuensi)
    total_frekuensi = df_frekuensi['Frekuensi'].sum()
    df_frekuensi['Probabilitas'] = df_frekuensi['Frekuensi'] / total_frekuensi
    df_frekuensi['Probabilitas Kumulatif'] = np.ceil(df_frekuensi['Probabilitas'].cumsum() * 100)
   
    return df_frekuensi

#mencari interval angka acak
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

# Fungsi untuk save data ke session
def save(frequency_tables):
    saved_frequency = {}
    for column, frequency_table in frequency_tables.items():
        saved_frequency[column] = frequency_table
    st.session_state["frequency_tables"] = saved_frequency

#dungsi untuk menampilkan data
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

            # menampilkan parameter angka acak
            session_key_param = f"{column}_random_numbers_params"
            if session_key_param in st.session_state:
                st.dataframe(st.session_state[session_key_param], hide_index=True)

            # menampilkan angka acak
            session_key = f"{column}_random_numbers"
            if session_key in st.session_state:
                st.dataframe(st.session_state[session_key], width=700, hide_index=True)

def main():

    #inisialisasi
    init()

    st.title("Tahap Persiapan Simulasi Curah Hujan")

    # Upload file
    uploadedFile = None

    # Menampilkan data (Tabel Frekuensi) yang disimpan dalam cookie jika ada
    saved_frequency_tables = st.session_state["frequency_tables"]
    if saved_frequency_tables:
        st.file_uploader("Upload file CSV atau Excel", type=["csv", "xlsx"], accept_multiple_files=False, disabled=True)

        #validasi jika frekuensi tabel telah disimpan atau belum
        find = False
        for key in list(st.session_state['frequency_tables'].keys()):
            session_key = f"{key}_random_numbers"
            if session_key in st.session_state and st.session_state[session_key]:
                find = True
            else:
                find = False
                break
        
        #info jika data angka acak sudah disiapkan atau belum
        if find:
            st.info("Data sudah selesai disiapkan, waktunya simulasi..")
        else:
            st.warning("Data angka acak belum selesai disiapkan")

        with st.expander("Tabel Frekuensi"):
            show(saved_frequency_tables, "frequency")
        with st.expander("Tabel Probabilitas"):
            show(saved_frequency_tables, "probability")
        with st.expander("Tabel Interval Angka Acak"):
            show(saved_frequency_tables, "interval")
        with st.expander("Tabel Angka Acak"):
            
            if find:    
                # Panggil fungsi untuk menampilkan tabel angka acak
                show(st.session_state['frequency_tables'], "rng")
            else:
                st.warning(f'Angka acak belum lengkap, dibutuhkan angka acak "{key}" ')
            
    else:
        uploadedFile = st.file_uploader("Upload file CSV atau Excel", type=["csv", "xlsx"], accept_multiple_files=False)
            
        
    #
    # Menampilakn hasil data
    #

    data = uploaded_file(uploadedFile)
    if data is not None:
        st.write("Data yang diupload:")
        st.write(data)

        # Pilih kolom untuk perhitungan tabel frekuensi
        column_names = st.multiselect("Pilih kolom untuk perhitungan tabel frekuensi", data.columns)

        #menghitung tabel frekuensi
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