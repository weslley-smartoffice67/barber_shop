import streamlit as st
from datetime import datetime
import pandas as pd
from io import BytesIO

# Usuários de exemplo
USERS = {
    "admin": "1234",
    "evaristo": "barber"
}

def login():
    st.title("Evaristo Barber Shop - Login")
    username = st.text_input("Usuário")
    password = st.text_input("Senha", type="password")
    if st.button("Entrar"):
        if username in USERS and USERS[username] == password:
            st.session_state['logged_in'] = True
            st.session_state['username'] = username
        else:
            st.error("Usuário ou senha inválidos")

def registro_receita():
    st.success(f"Bem-vindo, {st.session_state['username']}! 🧔✂️")
    st.header("Registro de Entradas Diárias")
    with st.form("form_receita"):
        data = st.date_input("Data", value=datetime.now())
        servico = st.text_input("Serviço")
        quantidade = st.number_input("Quantidade", min_value=1, step=1, value=1)
        valor = st.number_input("Valor (R$)", min_value=0.0, step=0.01, value=0.0, format="%.2f")
        submitted = st.form_submit_button("Salvar Registro")
        if submitted:
            if "registros" not in st.session_state:
                st.session_state['registros'] = []
            st.session_state['registros'].append({
                "Data": data.strftime("%d/%m/%Y"),    # Formato dd,mm,aaaa
                "Serviço": servico,
                "Quantidade": quantidade,
                "Valor": valor
            })
            st.success("Registro salvo com sucesso!")

    # Tabela formatada
    if "registros" in st.session_state and st.session_state['registros']:
        df = pd.DataFrame(st.session_state['registros'])
        df["Valor"] = df["Valor"].apply(lambda x: f"R$ {x:,.2f}".replace('.', ','))
        st.subheader("Histórico do Dia")
        st.table(df)

        # Exporta para Excel
        output = BytesIO()
        df_excel = pd.DataFrame(st.session_state['registros'])
        df_excel.to_excel(output, index=False, sheet_name='Controle Diário')
        st.download_button(
            label="Exportar para Excel",
            data=output.getvalue(),
            file_name="Controle_Diario_Barbearia.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

if "logged_in" not in st.session_state:
    st.session_state['logged_in'] = False

if st.session_state['logged_in']:
    registro_receita()
else:
    login()
