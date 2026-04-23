import streamlit as st
import pandas as pd

# tampilkan logo
st.image("logo.png", width=150)

# judul
st.title("Aplikasi Perhitungan Emisi Karbon")
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

st.title("ZETriC Dashboard")

# koneksi ke Google Sheets
scope = ["https://spreadsheets.google.com/feeds",
         "https://www.googleapis.com/auth/drive"]

creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)

sheet = client.open("ZETriC Data").sheet1
data = sheet.get_all_records()

df = pd.DataFrame(data)

# hitung emisi sederhana
def hitung(row):
    energi = float(row['Energi']) * 0.85
    jarak = float(row['Jarak'])
    
    if row['Transportasi'] == "Motor":
        transport = jarak * 0.12
    elif row['Transportasi'] == "Mobil":
        transport = jarak * 0.24
    else:
        transport = 0
    
    limbah = float(row['Limbah']) * 0.2
    
    return energi + transport + limbah

df['Total Emisi'] = df.apply(hitung, axis=1)

# tampilkan data
st.dataframe(df)

# grafik
st.bar_chart(df.groupby('Nama')['Total Emisi'].sum())
