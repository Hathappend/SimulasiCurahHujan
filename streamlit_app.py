import pandas as pd
import streamlit as st
import numpy as np

# Tentukan nama kolom
nama_kolom_data = ['Index', 'Curah Hujan', 'Lama Hujan (Bulanan)']
nama_kolom_bil_acak = ['Index','Zi-1', 'Zi','Ui']

# Baca file Excel dan beri nama kolom
df_bilangan_acak1 = pd.read_excel('Input.xlsx', header=None, names=nama_kolom_bil_acak,sheet_name='AcakCurah')
df_bilangan_acak2 = pd.read_excel('Input.xlsx', header=None, names=nama_kolom_bil_acak,sheet_name='AcakLama')
df = pd.read_excel('Input.xlsx', header=None, names=nama_kolom_data,sheet_name='Data')

# Konversi kolom 'Curah Hujan' ke tipe integers
df['Curah Hujan'] = df['Curah Hujan'].astype(int)

# Konversi kolom 'Lama Hujan Bulanan' ke tipe integer
df['Lama Hujan (Bulanan)'] = df['Lama Hujan (Bulanan)'].astype(int)


# Data untuk probabilitas Curah Hujan
DataCurahHujan = {
    'Curah Hujan Tahunan': [1300, 1700, 2500, 2800, 3000],
    'Jumlah Frekuensi': [35, 18, 10, 6, 1]
}

#Data untuk probabilitas Lama Hujan (Bulanan)
DataLamaHujan = {
    'Data Lama Hujan': [1,2,3,4,5,6,7,8],
    'Jumlah Frekuensi': [25,16,6,5,5,6,4,3]
}

df_bilangan_acak_curah = pd.DataFrame(df_bilangan_acak1)
df_bilangan_acak_lama = pd.DataFrame(df_bilangan_acak2)

def SimulasiProgram(df_bilangan_acak1,df_bilangan_acak2):
    df_bilangan_acak_curah = pd.DataFrame(df_bilangan_acak1)
    df_bilangan_acak_lama = pd.DataFrame(df_bilangan_acak2)
    Tahun = df_bilangan_acak_curah['Index'] + 2023
    df_bilangan_acak_curah['Tahun'] = Tahun
    df_bilangan_acak_curah['Curah Hujan'] = round(df_bilangan_acak_curah['Ui'] * 100).astype(int)
    df_bilangan_acak_lama['Lama Hujan (Bulanan)'] = round(df_bilangan_acak_lama['Ui'] * 100).astype(int)
    
     # Buat kondisi dan pilihan untuk Curah Hujan
    conditions = [
        (df_bilangan_acak_curah['Curah Hujan'] >= 1) & (df_bilangan_acak_curah['Curah Hujan'] <= 50),
        (df_bilangan_acak_curah['Curah Hujan'] >= 51) & (df_bilangan_acak_curah['Curah Hujan'] <= 76),
        (df_bilangan_acak_curah['Curah Hujan'] >= 77) & (df_bilangan_acak_curah['Curah Hujan'] <= 90),
        (df_bilangan_acak_curah['Curah Hujan'] >= 91) & (df_bilangan_acak_curah['Curah Hujan'] <= 99),
        (df_bilangan_acak_curah['Curah Hujan'] == 100)
    ]
    condition1 = [
        (df_bilangan_acak_lama['Lama Hujan (Bulanan)'] >= 1)  & (df_bilangan_acak_lama['Lama Hujan (Bulanan)'] <= 36),
        (df_bilangan_acak_lama['Lama Hujan (Bulanan)'] >= 37) & (df_bilangan_acak_lama['Lama Hujan (Bulanan)'] <= 59),
        (df_bilangan_acak_lama['Lama Hujan (Bulanan)'] >= 60) & (df_bilangan_acak_lama['Lama Hujan (Bulanan)'] <= 67),
        (df_bilangan_acak_lama['Lama Hujan (Bulanan)'] >= 68) & (df_bilangan_acak_lama['Lama Hujan (Bulanan)'] <= 74),
        (df_bilangan_acak_lama['Lama Hujan (Bulanan)'] >= 75) & (df_bilangan_acak_lama['Lama Hujan (Bulanan)'] <= 81),
        (df_bilangan_acak_lama['Lama Hujan (Bulanan)'] >= 82) & (df_bilangan_acak_lama['Lama Hujan (Bulanan)'] <= 90),
        (df_bilangan_acak_lama['Lama Hujan (Bulanan)'] >= 91) & (df_bilangan_acak_lama['Lama Hujan (Bulanan)'] <= 96),
        (df_bilangan_acak_lama['Lama Hujan (Bulanan)'] >= 97) & (df_bilangan_acak_lama['Lama Hujan (Bulanan)'] <= 100)
    ]
    
    choices = [
        1300,
        1700,  
        2500,
        2800,
        3000   
    ]
    choices1 = [
        1,
        2,  
        3,
        4,
        5,
        6,
        7,
        8
    ]
    df_bilangan_acak_curah['Curah Hujan (mm)'] = np.select(conditions, choices, default=0).astype(int)
    df_bilangan_acak_lama ['Lama Hujan (Bln)'] = np.select(condition1, choices1, default=0).astype(int)
    
    
    # Gabungkan kedua DataFrame berdasarkan index
    df_bilangan_acak_curah['Lama Hujan (Bulanan)'] = df_bilangan_acak_lama['Lama Hujan (Bulanan)']
    df_bilangan_acak_curah['Lama Hujan (Bln)'] = df_bilangan_acak_lama['Lama Hujan (Bln)']
    df_bilangan_acak_curah['Intensitas Hujan'] = df_bilangan_acak_curah['Curah Hujan (mm)'] / df_bilangan_acak_lama['Lama Hujan (Bln)']
    condition2 = [
        (df_bilangan_acak_curah['Intensitas Hujan'] < 100),
        (df_bilangan_acak_curah['Intensitas Hujan'] >= 100) & (df_bilangan_acak_curah['Intensitas Hujan']<=300),
        (df_bilangan_acak_curah['Intensitas Hujan'] >= 301) & (df_bilangan_acak_curah['Intensitas Hujan']<=500),
        (df_bilangan_acak_curah['Intensitas Hujan'] > 500) 
    ]
    choices2 = [
        'Hujan Ringan',
        'Hujan Sedang',
        'Hujan Lebat',
        'Hujan Sangat Lebat'
    ]
    df_bilangan_acak_curah['Status Cuaca'] = np.select(condition2,choices2,default=0)
    df_fix = df_bilangan_acak_curah[['Tahun', 'Curah Hujan', 'Lama Hujan (Bulanan)', 'Curah Hujan (mm)','Lama Hujan (Bln)','Intensitas Hujan','Status Cuaca']]
    
    return df_fix
    




def ProbabilitasLamaHujan(DataLamaHujan, add_row=True):
    df_LamaHujan = pd.DataFrame(DataLamaHujan)
    total_frekuensi = df_LamaHujan['Jumlah Frekuensi'].sum()
    df_LamaHujan['Probabilitas'] = df_LamaHujan['Jumlah Frekuensi'] / total_frekuensi
    df_LamaHujan['Probabilitas Kumulatif'] = np.ceil(df_LamaHujan['Probabilitas'].cumsum() * 100)
   
    return df_LamaHujan
def KemunculanAngkaAcakLamaHujan(DataLamaHujan, add_row=True):
    df_LamaHujan = pd.DataFrame(DataLamaHujan)
    total_frekuensi = df_LamaHujan['Jumlah Frekuensi'].sum()
    df_LamaHujan['Probabilitas'] = df_LamaHujan['Jumlah Frekuensi'] / total_frekuensi
    df_LamaHujan['Probabilitas Kumulatif'] = np.ceil(df_LamaHujan['Probabilitas'].cumsum() * 100)
   
    # Menghitung interval angka acak dimulai dari 1-100
    interval_awal = df_LamaHujan['Probabilitas Kumulatif'].shift(fill_value=0).astype(int) + 1
    interval_akhir = df_LamaHujan['Probabilitas Kumulatif'].astype(int)
    interval_akhir.iloc[-1] = 100  # Pastikan batas atas terakhir adalah 100
    df_LamaHujan['Interval Angka Acak'] = np.where(interval_awal == interval_akhir,
                                                     interval_awal.astype(str),
                                                     interval_awal.astype(str) + "-" + interval_akhir.astype(str))
    return df_LamaHujan

def ProbabilitasCurahHujan(DataCurahHujan, add_row=True):
    df_CurahHujan = pd.DataFrame(DataCurahHujan)
    total_frekuensi = df_CurahHujan['Jumlah Frekuensi'].sum()
    df_CurahHujan['Probabilitas'] = df_CurahHujan['Jumlah Frekuensi'] / total_frekuensi
    df_CurahHujan['Probabilitas Kumulatif'] = np.ceil(df_CurahHujan['Probabilitas'].cumsum() * 100)
   
    return df_CurahHujan
def KemunculanAngkaAcakCurahHujan(DataCurahHujan, add_row=True):
    df_CurahHujan = pd.DataFrame(DataCurahHujan)
    total_frekuensi = df_CurahHujan['Jumlah Frekuensi'].sum()
    df_CurahHujan['Probabilitas Kumulatif'] = np.ceil((df_CurahHujan['Jumlah Frekuensi'] / total_frekuensi).cumsum() * 100)
    
    # Menghitung interval angka acak dimulai dari 1-100
    interval_awal = df_CurahHujan['Probabilitas Kumulatif'].shift(fill_value=0).astype(int) + 1
    interval_akhir = df_CurahHujan['Probabilitas Kumulatif'].astype(int)
    interval_akhir.iloc[-1] = 100  # Pastikan batas atas terakhir adalah 100
    df_CurahHujan['Interval Angka Acak'] = np.where(interval_awal == interval_akhir,
                                                     interval_awal.astype(str),
                                                     interval_awal.astype(str) + "-" + interval_akhir.astype(str))
    return df_CurahHujan

def HitungCurahHujan():
    curah_hujan_segments = list(df['Curah Hujan'])
    rekap_curah_hujan_segments = {}
    for data in curah_hujan_segments:
        if data in rekap_curah_hujan_segments:
            rekap_curah_hujan_segments[data] += 1
        else:
            rekap_curah_hujan_segments[data] = 1
    return rekap_curah_hujan_segments

def HitungLamaHujan():
    lama_hujan_segments = list(df['Lama Hujan (Bulanan)'])
    rekap_lama_hujan_segments = {}
    for data in lama_hujan_segments:
        if data in rekap_lama_hujan_segments:
            rekap_lama_hujan_segments[data] += 1
        else:
            rekap_lama_hujan_segments[data] = 1
    rekap_lama_hujan_segments_sorted = dict(sorted(rekap_lama_hujan_segments.items()))
    return rekap_lama_hujan_segments_sorted

# Menghitung data
rekap_curah_hujan = HitungCurahHujan()
rekap_lama_hujan = HitungLamaHujan()

# Membuat DataFrame
CurahHujan = pd.DataFrame(list(rekap_curah_hujan.items()), columns=['Curah Hujan', 'Frekuensi'])
LamaHujan = pd.DataFrame(list(rekap_lama_hujan.items()), columns=['Lama Hujan', 'Frekuensi'])

# Menghitung Probabilitas dan Interval Angka Acak
dfProbabilitasCurahHujan = ProbabilitasCurahHujan(DataCurahHujan, add_row=True)
dfIntervalAngkaAcakCurahHujan = KemunculanAngkaAcakCurahHujan(DataCurahHujan, add_row=True)
dfProbabilitasAngkaAcakLamaHujan = ProbabilitasLamaHujan(DataLamaHujan, add_row=True)
dfIntervalAngkaAcakLamaHujan = KemunculanAngkaAcakLamaHujan(DataLamaHujan, add_row=True)
dfSimulasi = SimulasiProgram(df_bilangan_acak1,df_bilangan_acak2)



# Convert DataFrame to HTML without index
CurahHujanTabel = CurahHujan.to_html(index=False)
LamaHujanTabel = LamaHujan.to_html(index=False)
CurahHujanTabelProbabilitas = dfProbabilitasCurahHujan.to_html(index=False)
CurahHujanTabelInterval = dfIntervalAngkaAcakCurahHujan.to_html(index=False)
LamaHujanTabelProbabilitas = dfProbabilitasAngkaAcakLamaHujan.to_html(index=False)
LamaHujanTabelInterval = dfIntervalAngkaAcakLamaHujan.to_html(index=False)
TabelBilanganAcakCurahHujan = df_bilangan_acak_curah.to_html(index=False)
TabelBilanganAcakLamaHujan = df_bilangan_acak_lama.to_html(index=False)
TabelSimulasi = dfSimulasi.to_html(index=False)



# Tampilan dengan Streamlit
# Main function
def main():
    st.sidebar.title("Model Dan Simulasi")
    selected_tab = st.sidebar.radio("Menu", ["Tabel Frekuensi, Probabilitas, dan Interval Angka Acak","Tabel Bilangan Acak","Simulasi"])

    
    if selected_tab == "Tabel Frekuensi, Probabilitas, dan Interval Angka Acak":
        st.title("Tabel Frekuensi, Probabilitas, dan Interval Angka Acak")

        st.subheader("Rekapitulasi Curah Hujan:")
        st.write(CurahHujanTabel, unsafe_allow_html=True)

        st.write("")

        st.subheader("Rekapitulasi Lama Hujan:")
        st.write(LamaHujanTabel, unsafe_allow_html=True)

        st.write("")

        st.subheader("Probabilitas Curah Hujan Tahunan:")
        st.write(CurahHujanTabelProbabilitas, unsafe_allow_html=True)

        st.write("")

        st.subheader("Interval Angka Acak Curah Hujan Tahunan:")
        st.write(CurahHujanTabelInterval, unsafe_allow_html=True)

        st.write("")

        st.subheader("Probabilitas Lama Hujan (Bulanan):")
        st.write(LamaHujanTabelProbabilitas, unsafe_allow_html=True)

        st.write("")

        st.subheader("Interval Angka Acak Lama Hujan (Bulanan):")
        st.write(LamaHujanTabelInterval, unsafe_allow_html=True)
    elif selected_tab == "Tabel Bilangan Acak":
        st.title("Tabel Bilangan Acak")
        st.write("")

        st.subheader("Bilangan Acak Curah Hujan:")
        st.write(TabelBilanganAcakCurahHujan, unsafe_allow_html=True)


        st.write("")

        st.subheader("Bilangan Lama Hujan (Bulanan):")
        st.write(TabelBilanganAcakLamaHujan, unsafe_allow_html=True)
    elif selected_tab == "Simulasi":
        st.title("Simulasi")
        st.write("")
        st.subheader("Simulasi Curah Hujan Tahunan:")
        st.write(TabelSimulasi, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
