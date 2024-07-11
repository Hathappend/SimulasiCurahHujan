import streamlit as st
import pandas as pd

def init():
    if 'guest' not in st.session_state:
        st.session_state['guest'] = {}
    if 'frequency_tables' not in st.session_state:
        st.session_state['frequency_tables'] = {}

#fungsi untunk generate angka acak metode mixed
def generate_mixed(a, n, z0, c, m, jumlah_iterasi):

    #initialisasi
    random_number = {}
    increment = []
    zi_min_1 = []
    zi = []
    ui = []
    
    #perhitungan angka acak
    for i in range(1, jumlah_iterasi+1):
        increment.append(i)
        random_number['i'] = increment
        if i == 1:
            zi_min_1.append(z0) 
        else:
            zi_min_1.append(zi[i-2]) 
        random_number['Zi-1'] = zi_min_1
        zi.append(((a**n * zi_min_1[i-1]) + ((a**n - 1)/(a - 1)) * c) % m)
        random_number['Zi'] = zi
        ui.append(zi[i-1]/m)
        random_number['Ui'] = ui

    return random_number

def main():

    #inisialsisasi
    init()

    st.title("Random Number Generator")
    st.caption('_Note:_ Untuk keperluan simulasi wajib pilih kolom')

    #mengambil data tabel frekuensi
    frequency_table = st.session_state['frequency_tables']

    selected_column = None
    if frequency_table:
        
        #validasi jika angka acak sudah di siapkan
        ready = False
        for key in list(frequency_table.keys()):
            session_key = f'{key}_random_numbers'
            if session_key in st.session_state and st.session_state[session_key]:
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
    
    #menginisialisasi parameter angka acak
    df = pd.DataFrame(
            [
                {"a": 300, "n": 2, "Z0": 10122004, "c": 2024, "m": 2221, "Jumlah Iterasi": 300}
            ]
        )

    edited_df = st.data_editor(df, hide_index=True)

    #proses generate angka acak
    if st.button("Generate"):
        st.success("Random number berhasil disimpan")
        a = edited_df.at[0, 'a']
        n = edited_df.at[0, 'n']
        z0 = edited_df.at[0, 'Z0']
        c = edited_df.at[0, 'c']
        m = edited_df.at[0, 'm']
        jumlah_iterasi = edited_df.at[0, 'Jumlah Iterasi']

        # generate angka acak
        random_number = generate_mixed(a, n, z0, c, m, jumlah_iterasi)

        # save parameter
        key_param = f"{selected_column}_random_numbers_params"
        st.session_state[key_param] = edited_df

        # save randon number ke session
        key = f"{selected_column}_random_numbers"
        st.session_state[key] = random_number

        # Pilihan jika hanya ingin generate angka acak saja tanpa simulasi
        st.session_state["guest_random_numbers"] = random_number

    # Menampilkan angka acak hasil generate berdasarkan select box
    st.write("Hasil Generate:")
    if selected_column:
        key = f"{selected_column}_random_numbers"
        if key in st.session_state:
            st.dataframe(pd.DataFrame(st.session_state[key]), width=700)

if __name__ == "__main__":
    main()