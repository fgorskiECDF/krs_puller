import streamlit as st
from bs4 import BeautifulSoup
import re

st.title("KRS PULLER - pobieranie numerów krs z Rejestru.io")

st.markdown("### Instrukcja:")

st.markdown("""
1. Wejdź na [Rejestr.io](https://rejestr.io) i wybierz interesujące cię filtry np. branża budowlana, lubuskie, zysk>1mln zł itp.
2. Rozwiń listę wyników w rejestrze, tak aby pokazały się wszystkie podmioty, które chcesz wyszukać
2. Kliknij prawym przyciskiem na stronę i zapisz ją jako strona internetowa (format .html)
3. Wrzuć zapisaną stronę w polu poniżej
4. Wygeneruje Ci się excel na dole strony, pobierz go i sprawdź czy liczba numerów krs zgadza się z porządaną liczbą 
5. Przejdź do strony KRS MINER i wrzuć pobranego excela
""")

uploaded_file = st.file_uploader("Zapisz stronę z Rejestru.io jako html i wgraj tutaj", type="html")
krs_numbers = []

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
import pandas as pd
import io

    # Przygotowanie danych jako DataFrame z jedną kolumną 'krs' (typ tekstowy)
    df = pd.DataFrame({'krs': krs_numbers}, dtype=str)

    # Zapis do Excela w pamięci
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)
    output.seek(0)

    # Przycisk pobierania
    st.download_button(
        label="Pobierz jako Excel",
        data=output,
        file_name="numery_krs.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
