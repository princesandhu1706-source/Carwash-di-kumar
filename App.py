import streamlit as st
import pandas as pd
from datetime import datetime
import os

# Configurazione pagina
st.set_page_config(page_title="Gestionale Autolavaggio", layout="wide")

# Nome del file dove verranno salvati i dati
DB_FILE = "registro_lavaggi.csv"

# Funzione per caricare i dati
def load_data():
    if os.path.exists(DB_FILE):
        return pd.read_csv(DB_FILE)
    return pd.DataFrame(columns=["Data e Ora", "Marca", "Tipo Lavaggio", "Importo", "Pagamento"])

# Caricamento iniziale
df = load_data()

st.title("Sistema Monitoraggio Autolavaggio 🚗")

# --- SEZIONE INSERIMENTO ---
st.sidebar.header("Nuovo Lavaggio")

with st.sidebar.form("form_lavaggio", clear_on_submit=True):
    # 1. Marca Auto (Menu a tendina)
    marche = ["Fiat", "Ford", "BMW", "Audi", "Mercedes", "Volkswagen", "Toyota", "Renault", "Peugeot", "Altro"]
    marca = st.selectbox("Marca Auto", marche)
    
    # 2. Tipo Lavaggio (Menu a tendina)
    tipo_lavaggio = st.selectbox("Tipo Lavaggio", ["Solo dentro", "Solo fuori", "Dentro fuori", "Lavaggio sedili"])
    
    # 3. Importo (Menu a tendina)
    importi_base = ["8", "10", "15", "17", "18", "20", "25", "30", "80", "90", "Altro"]
    importo_scelto = st.selectbox("Importo (€)", importi_base)
    
    # Gestione "Altro" importo
    importo_finale = importo_scelto
    if importo_scelto == "Altro":
        importo_finale = st.number_input("Inserisci importo personalizzato", min_value=0, value=0)
    
    # 4. Metodo di Pagamento
    pagamento = st.selectbox("Metodo Pagamento", ["Contanti", "Satispay", "Carta di Credito"])
    
    submit = st.form_submit_button("Registra Lavaggio")

if submit:
    # Genera data e ora correnti
    ora_attuale = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    
    # Crea nuova riga
    nuova_riga = {
        "Data e Ora": ora_attuale,
        "Marca": marca,
        "Tipo Lavaggio": tipo_lavaggio,
        "Importo": float(importo_finale),
        "Pagamento": pagamento
    }
    
    # Salva su file CSV
    df = pd.concat([df, pd.DataFrame([nuova_riga])], ignore_index=True)
    df.to_csv(DB_FILE, index=False)
    st.success(f"Registrato alle {ora_attuale}!")

# --- SEZIONE MONITORAGGIO ---
st.header("Monitoraggio Lavaggi")

# Filtri veloci
col1, col2 = st.columns(2)
totale_incasso = df["Importo"].astype(float).sum()
numero_lavaggi = len(df)

col1.metric("Totale Incassato", f"{totale_incasso} €")
col2.metric("Totale Auto Lavate", numero_lavaggi)

# Tabella riassuntiva
st.subheader("Registro Completo")
st.dataframe(df.sort_index(ascending=False), use_container_width=True)

# Esportazione
st.download_button(
    label="Scarica Registro in Excel/CSV",
    data=df.to_csv(index=False).encode('utf-8'),
    file_name=f"lavaggi_{datetime.now().strftime('%m_%Y')}.csv",
    mime='text/csv',
)
