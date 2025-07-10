# -*- coding: utf-8 -*-

import streamlit as st
from bs4 import BeautifulSoup
import re
import pandas as pd
import io

def pobierz_dane_krs(krs):
    url = f"https://api-krs.ms.gov.pl/api/krs/OdpisAktualny/{krs}?rejestr=P&format=json"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            dane = data.get("odpis", {}).get("dane", {}).get("dzial1", {}).get("danePodmiotu", {})
            adres = data.get("odpis", {}).get("dane", {}).get("dzial1", {}).get("siedzibaIAdres", {}).get("adres", {})
            return {
                "krs": krs,
                "nazwa": dane.get("nazwa"),
                "forma_prawna": dane.get("formaPrawna"),
                "nip": dane.get("identyfikatory", {}).get("nip"),
                "regon": dane.get("identyfikatory", {}).get("regon"),
                "ulica": adres.get("ulica"),
                "nr_domu": adres.get("nrDomu"),
                "kod_pocztowy": adres.get("kodPocztowy"),
                "miejscowosc": adres.get("miejscowosc"),
            }
        else:
            return {"krs": krs, "status": f"Błąd {response.status_code}"}
    except Exception as e:
        return {"krs": krs, "status": f"Błąd: {str(e)}"}

st.set_page_config(page_title="Pobieranie danych z KRS", layout="wide")

st.title("KRS MINER - aplikacja do pobierania danych z KRS")

st.subheader("W razie problemów/errorów na stronach:")

st.markdown("[Skontaktuj się na Slacku](https://grupaecdf.slack.com/team/U08FLMFN60Y)")
st.markdown(
    'Skontaktuj się mailowo: <span style="color:purple">f.gorski@ecdf.pl</span>',
    unsafe_allow_html=True
st.markdown("UWAGA: Strona jest w trakcie testów, mogą pojawiać się błędy przy łączeniu z serwerem")
    
st.markdown("### Instrukcja:")
st.markdown("""
**1. Sprawdź czy masz excela ze strony [KRS PULLER](https://krspuller-bymuj54nsxiddtelnvu2kf.streamlit.app/)** (arkusz koniecznie musi mieć pierwszy wiersz "krs" i dalej numery ciągiem
2. wrzuć excela poniżej, zaczną się pobierać dane z KRSu. Wydajność to około 50 podmiotów na minutę, wynika to z ograniczeń serwera rządowego
3. Pobierz excela który wygeneruje się na dole - to twoja baza kontaktów 🤠
"""
    
    
uploaded_file = st.file_uploader("Wgraj plik Excel z kolumną 'krs'", type=["xlsx"])
if uploaded_file:
    df = pd.read_excel(uploaded_file)
    
    if "krs" not in df.columns:
        st.error("Brakuje kolumny 'krs' w pliku Excel.")
    else:
        st.success(f"Znaleziono {len(df)} rekordów do przetworzenia.")

        if st.button(" Rozpocznij pobieranie danych"):
            wyniki = []
            for i, row in df.iterrows():
                krs = str(row["krs"]).zfill(10)
                wynik = pobierz_dane_krs(krs)
                wyniki.append(wynik)
                st.write(f"[{i+1}] Przetworzono KRS: {krs}")

            df_wynik = pd.DataFrame(wyniki)
            st.success(" Pobieranie zakończone.")

            st.dataframe(df_wynik)

            # Dodaj przycisk do pobrania Excela
            st.download_button(
                " Pobierz wynik jako Excel",
                df_wynik.to_excel(index=False, engine="openpyxl"),
                file_name="dane_z_krs.xlsx"
            )
