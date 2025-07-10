# -*- coding: utf-8 -*-


import streamlit as st
from bs4 import BeautifulSoup
import re
import pandas as pd
import io

st.title("KRS PULLER - pobieranie numerów KRS z Rejestru.io")

st.subheader("W razie problemów/errorów na stronach:")

st.markdown("[Skontaktuj się na Slacku](https://grupaecdf.slack.com/team/U08FLMFN60Y)")
st.markdown(
    'Skontaktuj się mailowo: <span style="color:purple">f.gorski@ecdf.pl</span>',
    unsafe_allow_html=True
)


st.markdown("### Instrukcja:")
st.markdown("""
1. Wejdź na [Rejestr.io](https://rejestr.io) i wybierz interesujące Cię filtry np. branża budowlana, lubuskie, zysk > 1 mln zł itp.  
2. Rozwiń listę wyników w rejestrze **do końca**, tak aby pokazały si wszystkie podmioty, które chcesz wyszukać 
3. Kliknij prawym przyciskiem na stronę i zapisz ją jako strona internetowa (format .html)  
4. Wrzuć zapisaną stronę w polu poniżej  
5. Wygeneruje się Excel na dole strony - pobierz go i sprawdź, czy liczba numerów KRS zgadza się z oczekiwanymi po wyszukaniu w rejestrze
6. Przejdź do strony **KRS MINER** i wrzuć pobranego Excela  
""")

uploaded_file = st.file_uploader("Zapisz stronę z Rejestru.io jako HTML i wgraj tutaj", type="html")

if uploaded_file:
    html = uploaded_file.read().decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")
    text = soup.get_text()

    # Wyszukiwanie 10-cyfrowych numerów KRS
    krs_numbers = re.findall(r'\b\d{10}\b', text)

    # Usunięcie duplikatów i sortowanie
    unique_krs = sorted(set(krs_numbers))

    if unique_krs:
        st.success(f"Znaleziono {len(unique_krs)} unikalnych numerów KRS:")
        for krs in unique_krs:
            st.write(f"{krs}")

        # Tworzenie DataFrame
        df = pd.DataFrame({'krs': unique_krs}, dtype=str)

        # Zapis do Excela w pamięci
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False)
        output.seek(0)

        # Przycisk pobierania
        st.download_button(
            label=" Pobierz jako Excel",
            data=output,
            file_name="numery_krs.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    else:
        st.warning("Nie znaleziono żadnych numerów KRS w pliku.")
