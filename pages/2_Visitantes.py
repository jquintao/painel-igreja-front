import streamlit as st
import requests
from datetime import date

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Cadastro de Visitantes", page_icon="👋")

API_URL = "https://api-igreja-o5t6.onrender.com/visitantes/"

st.title("👋 Cadastro de Visitantes")
st.markdown("Preencha os dados abaixo para registrar a visita.")
st.divider()

# --- FORMULÁRIO ---
with st.form("form_visitante", clear_on_submit=True):
    st.subheader("Dados Pessoais")
    nome = st.text_input("Nome Completo *")
    
    col1, col2 = st.columns(2)
    with col1:
        idade = st.number_input("Idade", min_value=0, max_value=120, step=1)
    with col2:
        sexo = st.selectbox("Sexo", ["Masculino", "Feminino", "Não Informar"])
        
    profissao = st.text_input("Profissão")
    
    col3, col4 = st.columns(2)
    with col3:
        data_nasc = st.date_input("Data de Nascimento", min_value=date(1920, 1, 1), max_value=date.today())
    with col4:
        data_visita = st.date_input("Data da Visita", max_value=date.today())
        
    st.subheader("Contato e Endereço")
    telefone = st.text_input("Telefone / WhatsApp")
    endereco = st.text_input("Endereço Completo")
        
    st.divider()
    submit_button = st.form_submit_button(label="Salvar Visitante", use_container_width=True)

# --- LÓGICA DE ENVIO ---
if submit_button:
    if not nome.strip():
        st.warning("⚠️ O campo 'Nome Completo' é obrigatório!")
    else:
        # Empacotando os dados conforme a nossa tabela real de visitantes
        payload = {
            "nome": nome,
            "idade": idade,
            "sexo": sexo,
            "profissao": profissao,
            "data_nasc": str(data_nasc),
            "telefone": telefone,
            "endereco": endereco,
            "data_visita": str(data_visita),
            "create_by": 1 # Acionando nosso campo de auditoria
        }
        
        with st.spinner("Salvando no banco de dados..."):
            try:
                response = requests.post(API_URL, json=payload)
                
                if response.status_code in [200, 201]:
                    dados_retorno = response.json()
                    st.success(f"✅ Sucesso! Visitante **{nome}** cadastrado com o ID: {dados_retorno.get('id')}")
                    st.balloons()
                else:
                    st.error(f"❌ Erro ao salvar: O servidor retornou o código {response.status_code}.")
                    st.json(response.json())
                    
            except requests.exceptions.RequestException:
                st.error("🔌 Erro de conexão com a API no Render.")