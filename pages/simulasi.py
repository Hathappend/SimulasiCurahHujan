import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

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

# fungsi untuk membandingkan angka acak ke interval
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

    #inisialisasi
    init()

    st.title("Simulasi Curah Hujan")

    #mengambil data frekuensi tabel
    frequency_tables = st.session_state['frequency_tables']

    #validasi bahwa angka acak sudah di generate atau belum
    find = False
    for key in list(frequency_tables.keys()):
        session_key = f'{key}_random_numbers'
        if session_key in st.session_state and st.session_state[session_key]:
            find = True
        else: 
            find = False
            break
    
    #proses simulasi
    if find:
        st.info("Semua data persiapan sudah siap. Simulasikan sekarang")

        if st.button("Simulasikan"):
            
            # Menghitung angka acak * 100
            combine_random_number = {}
            colomn_variable = list(frequency_tables.keys())
            for key in colomn_variable:
                session_key = f'{key}_random_numbers'
                if session_key in st.session_state:
                    random_number = st.session_state[session_key]['Ui'] # ekstrak data angka acak ke kolom Ui
                    combine_random_number[key] = random_number
            
            # Simpan angka acak ke dalam session
            df_random_number = pd.DataFrame(combine_random_number).mul(100).round().astype(int)
            st.session_state['random_number'] = df_random_number

            df = pd.DataFrame(combine_random_number).mul(100).round().astype(int)

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
        st.warning("Persiapan data belum di siapkan. Silahkan siapkan terlebih dahulu")

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

        # 
        # Visualisasi Data
        #

        col1, col2, col3 = st.columns(3)

        #
        # Visualiasasi data jumlah frekuensi setiap curah hujan
        #

        status_counts = st.session_state['status'].value_counts()
        status_counts = status_counts.reset_index()
        status_counts.columns = ['status curah hujan', 'frekuensi']

        # Membuat Bar Chart
        plt.figure(figsize=(8, 6))
        plt.bar(status_counts['status curah hujan'], status_counts['frekuensi'], color='skyblue')
        plt.title(f"Frekuensi Curah Hujan selama {st.session_state['status'].shape[0]} tahun")
        plt.xlabel('Status Curah Hujan')
        plt.ylabel('Frekuensi')

        # Menampilkan di Streamlit
        if st.session_state['status'].to_dict():
            col1.pyplot(plt)

        #
        # Visualiasasi data persentase curah hujan
        #

        status_counts = st.session_state['status'].value_counts(normalize=True) * 100
        status_counts = status_counts.reset_index()
        status_counts.columns = ['status curah hujan', 'persentase']

        # Membuat Pie Chart
        fig, ax = plt.subplots()
        ax.pie(status_counts['persentase'], labels=status_counts['status curah hujan'], autopct='%1.1f%%', startangle=90)
        ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        plt.title(f"Persentase Curah Hujan Selama {st.session_state['status'].shape[0]} tahun")        

        # Menampilkan di Streamlit
        if st.session_state['status'].to_dict():
            col2.pyplot(fig)

        #
        # Visualiasasi data jumlah rata-rata setiap curah hujan
        #

        if st.session_state['status'].to_dict():
            df = pd.concat(
                [
                    st.session_state['intensity'],
                    st.session_state['status']
                ], axis=1
            )

            df.columns = ['intensity', 'status']
            avg_intensity = df.groupby('status')['intensity'].mean().reset_index().sort_values(by='intensity', ascending=False)

            # Membuat Bar Chart
            plt.figure(figsize=(8, 6))
            bars = plt.bar(avg_intensity['status'], avg_intensity['intensity'], color='skyblue')
            plt.title(f"Rata-Rata Intensitas Hujan selama {st.session_state['status'].shape[0]} tahun")
            plt.xlabel('Status Curah Hujan')

            #Menambahkan label nilai rata-rata di atas setiap bar
            for bar in bars:
                yval = bar.get_height()
                plt.text(bar.get_x() + bar.get_width()/2, yval, f'{round(yval, 2)} mm', ha='center', va='bottom')

            # Menampilkan di Streamlit
            col3.pyplot(plt)

        

        #
        # Menampilakn tabel angka acak dan simulasi
        #

        col1, col2 = st.columns([1.8, 2.2])

        randomNumberContainer = col1.container(border=True)
        randomNumberContainer.subheader("Angka Acak")

        df_random = pd.concat(
            [
                st.session_state['years'].astype(str), 
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