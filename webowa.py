# -*- coding: utf-8 -*-


import streamlit as st
from bs4 import BeautifulSoup
import re
import pandas as pd
import io

st.title("KRS PULLER - pobieranie numer贸w KRS z Rejestru.io")

st.subheader("馃摡 W razie problem贸w/error贸w na stronach:")

st.markdown("[Skontaktuj si臋 na Slacku](https://grupaecdf.slack.com/team/U08FLMFN60Y)")
st.markdown(
    'Skontaktuj si臋 mailowo: <span style="color:purple">f.gorski@ecdf.pl</span>',
    unsafe_allow_html=True
)


st.markdown("### Instrukcja:")
st.markdown("""
1. Wejd藕 na [Rejestr.io](https://rejestr.io) i wybierz interesuj膮ce ci臋 filtry np. bran偶a budowlana, lubuskie, zysk > 1 mln z艂 itp.  
2. Rozwi艅 list臋 wynik贸w w rejestrze, tak aby pokaza艂y si臋 wszystkie podmioty, kt贸re chcesz wyszuka膰  
3. Kliknij prawym przyciskiem na stron臋 i zapisz j膮 jako stron臋 internetow膮 (format .html)  
4. Wrzu膰 zapisan膮 stron臋 w polu poni偶ej  
5. Wygeneruje si臋 Excel na dole strony 鈥?pobierz go i sprawd藕, czy liczba numer贸w KRS zgadza si臋 z oczekiwanymi po wyszukaniu w rejestrze
6. Przejd藕 do strony **KRS MINER** i wrzu膰 pobranego Excela  
""")

uploaded_file = st.file_uploader("Zapisz stron臋 z Rejestru.io jako HTML i wgraj tutaj", type="html")

if uploaded_file:
    html = uploaded_file.read().decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")
    text = soup.get_text()

    # Wyszukiwanie 10-cyfrowych numer贸w KRS
    krs_numbers = re.findall(r'\b\d{10}\b', text)

    # Usuni臋cie duplikat贸w i sortowanie
    unique_krs = sorted(set(krs_numbers))

    if unique_krs:
        st.success(f"Znaleziono {len(unique_krs)} unikalnych numer贸w KRS:")
        for krs in unique_krs:
            st.write(f"鈥?{krs}")

        # Tworzenie DataFrame
        df = pd.DataFrame({'krs': unique_krs}, dtype=str)

        # Zapis do Excela w pami臋ci
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
        st.warning("Nie znaleziono 偶adnych numer贸w KRS w pliku.")
