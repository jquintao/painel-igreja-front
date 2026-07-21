import streamlit as st
import requests
from datetime import date

# O st.set_page_config foi removido daqui para não conflitar com o Inicio.py

API_URL = "https://api-igreja-o5t6.onrender.com/membros/"

st.title("👤 Cadastro de Membros")
st.markdown("Preencha os dados abaixo para registrar um novo membro oficial.")
st.divider()

# Formulário
with st.form("form_membro", clear_on_submit=True):
    nome = st.text_input("Nome Completo *")
    
    col1, col2 = st.columns(2)
    with col1:
        idade = st.number_input("Idade", min_value=0, max_value=120, step=1)
    with col2:
        sexo = st.selectbox("Sexo", ["Masculino", "Feminino", "Não Informar"])
        
    profissao = st.text_input("Profissão")
    data_nasc = st.date_input("Data de Nascimento", min_value=date(1920, 1, 1), max_value=date.today())
    
    st.subheader("Contato")
    col3, col4 = st.columns(2)
    with col3:
        telefone = st.text_input("Telefone / WhatsApp")
    with col4:
        rede_social = st.text_input("Instagram / Facebook")
        
    st.divider()
    submit_button = st.form_submit_button(label="Salvar Membro", use_container_width=True)

# Lógica de Envio
if submit_button:
    if not nome.strip():
        st.warning("⚠️ O campo 'Nome Completo' é obrigatório!")
    else:
        # Empacotando os dados conforme a API exige
        payload = {
            "nome": nome,
            "idade": idade,
            "sexo": sexo,
            "profissao": profissao,
            "data_nasc": str(data_nasc),
            "telefone": telefone,
            "rede_social": rede_social,
            "foto": "string", 
            "id_celula": None, 
            "create_by": 1 
        }
        
        with st.spinner("Salvando no banco de dados..."):
            try:
                response = requests.post(API_URL, json=payload)
                
                if response.status_code in [200, 201]:
                    dados_retorno = response.json()
                    st.success(f"✅ Sucesso! Membro **{nome}** cadastrado com o ID: {dados_retorno.get('id')}")
                    st.balloons()
                else:
                    st.error(f"❌ Erro ao salvar: O servidor retornou o código {response.status_code}.")
                    st.json(response.json())
                    
            except requests.exceptions.RequestException:
                st.error("🔌 Erro de conexão com a API no Render.")
