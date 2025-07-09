import streamlit as st
from bs4 import BeautifulSoup
import re

st.title("Ekstraktor numerów KRS z pliku HTML")

uploaded_file = st.file_uploader("Zapisz stronę z rejestru io jako html i wgraj tutaj", type="html")

if uploaded_file:
    html = uploaded_file.read().decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")
    text = soup.get_text()

    # Szukamy numerów KRS (np. 0000123456)
    krs_numbers = re.findall(r'\b\d{10}\b', text)

    if krs_numbers:
        st.success(f"Znaleziono {len(krs_numbers)} numerów KRS:")
        for krs in krs_numbers:
            st.write(f"• {krs}")
    else:
        st.warning("Nie znaleziono numerów KRS w pliku.")
