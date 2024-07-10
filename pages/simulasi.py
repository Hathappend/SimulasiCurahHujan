import streamlit as st
import pandas as pd

def init():

    #Inisialisasi session
    if 'frequency_tables' not in st.session_state:
        st.session_state['frequency_tables'] = {}

    #Inisialisasi session
    if 'years' not in st.session_state:
        st.session_state['years'] = pd.DataFrame()
    if 'status' not in st.session_state:
        st.session_state['status'] = pd.DataFrame()
    if 'intensity' not in st.session_state:
        st.session_state['intensity'] = pd.DataFrame()
    if 'interval_random_number' not in st.session_state:
        st.session_state['interval_random_number'] = pd.DataFrame()
    if 'random_number' not in st.session_state:
        st.session_state['random_number'] = pd.DataFrame()


def compare_to_interval(value, column):
    if column == "Curah Hujan Tahunan (Satuan mm)":
        if value >=0 and value <= 50:
            return 1300
        elif value >=51 and value <= 76:
            return 1700
        elif value >=77 and value <= 90:
            return 2500
        elif value >=91 and value <= 99:
            return 2800
        else:
            return 3000
    elif column == "Lama Hujan Tahunan (Satuan Bulan)":
        if value >=0 and value <= 36:
            return 1
        elif value >=37 and value <= 59:
            return 2
        elif value >=60 and value <= 67:
            return 3
        elif value >=68 and value <= 74:
            return 4
        elif value >=75 and value <= 81:
            return 5
        elif value >=82 and value <= 90:
            return 6
        elif value >=91 and value <= 96:
            return 7
        else:
            return 8
    elif column == "intensitas":
        if value < 100:
            return "Hujan Ringan"
        elif value >=100 and value <= 300:
            return "Hujan Sedang"
        elif value >=301 and value <= 500:
            return "Hujan Lebat"
        else :
            return "Hujan Sangat Lebat"

def main():

    init()

    st.title("Simulasi Curah Hujan")

    frequency_tables = st.session_state['frequency_tables']
    find = False
    for key in list(frequency_tables.keys()):
        session_key = f'{key}_random_numbers'
        if session_key in st.session_state and st.session_state[session_key]:
            find = True
        else: 
            find = False
            break
    
    if find:
        st.info("Semua data persiapan sudah siap. Simulasikan sekarang")

        if st.button("Simulasikan"):
            
            # Menghitung angka acak * 100
            combine_random_number = {}
            colomn_variable = list(frequency_tables.keys())
            for key in colomn_variable:
                session_key = f'{key}_random_numbers'
                if session_key in st.session_state:
                    random_number = st.session_state[session_key]['Ui']
                    combine_random_number[key] = random_number
            
            df_random_number = pd.DataFrame(combine_random_number).mul(100).round().astype(int)
            df = pd.DataFrame(combine_random_number).mul(100).round().astype(int)

            # Simpan angka acak
            st.session_state['random_number'] = df_random_number

            # Menghitung interval dan intensitas curah hujan
            combine_interval_random_number = pd.DataFrame()
            for key in colomn_variable:
                df[key] = df[key].apply(compare_to_interval, column=key)
                combine_interval_random_number[key] = df[key]

            df["intensitas"] = round(df[colomn_variable[0]] / df[colomn_variable[1]])
            df["Status Curah Hujan"] = df["intensitas"].apply(compare_to_interval, column="intensitas")

            # Simpan interval, intensitas, dan status
            st.session_state['interval_random_number'] = combine_interval_random_number
            st.session_state['intensity'] = df["intensitas"]
            st.session_state['status'] = df["Status Curah Hujan"]

            # Hitung tahun
            df["Tahun"] = range(2024, 2024 + len(df))
            
            # Simpan tahun
            st.session_state['years'] = df["Tahun"]
    else:
        st.write("Klik tombol 'Simulasikan' untuk memulai simulasi.")

    # 
    # Tampilkan hasil jika data tersedia
    #

    if (
        "years" in st.session_state and
        "random_number" in st.session_state and
        "interval_random_number" in st.session_state and
        "intensity" in st.session_state and
        "status" in st.session_state
    ):
        col1, col2 = st.columns([1.5, 2.5])

        randomNumberContainer = col1.container(border=True)
        randomNumberContainer.subheader("Angka Acak")

        df_random = pd.concat(
            [
                st.session_state['years'], 
                st.session_state['random_number']
            ],
            axis=1
        )
        
        randomNumberContainer.dataframe(df_random, hide_index=True, use_container_width=True)

        simulationContainer = col2.container(border=True)
        simulationContainer.subheader("Simulasi")

        df_simulation = pd.concat(
            [
                st.session_state['interval_random_number'], 
                st.session_state['intensity'], 
                st.session_state['status']
            ],
            axis=1
        )

        simulationContainer.dataframe(df_simulation, hide_index=True, use_container_width=True)


if __name__ == "__main__":
    main()