import streamlit as st
import requests
import pandas as pd

# Voltamos com o layout="wide" para que a tabela fique espaçosa no computador
st.set_page_config(page_title="Lista de Visitantes", page_icon="📋", layout="wide")

# 1. TRUQUE MÁGICO CORRIGIDO (Mantém o botão do menu lateral)
esconder_menu_rodape = """
    <style>
    #MainMenu {visibility: hidden;} /* Esconde os 3 pontinhos do desenvolvedor */
    footer {visibility: hidden;}    /* Esconde o Made with Streamlit */
    /* Retiramos a linha do header para o botão do menu não sumir! */
    </style>
"""
st.markdown(esconder_menu_rodape, unsafe_allow_html=True)
st.markdown(esconder_menu_rodape, unsafe_allow_html=True)

st.title("📋 Lista de Visitantes")
st.markdown("Filtre por data e escolha como prefere visualizar os dados.")
st.divider()

API_URL = "https://api-igreja-o5t6.onrender.com/visitantes/"

# --- ÁREA DE FILTROS E OPÇÕES ---
col1, col2 = st.columns([1, 1])

with col1:
    data_filtro = st.date_input("📅 Data da Visita", value=None, format="DD/MM/YYYY")

with col2:
    # Chave seletora para o usuário escolher o modo de visualização
    modo_visao = st.radio(
        "Modo de Visualização", 
        ["📱 Celular (Cartões)", "💻 Computador (Tabela)"], 
        horizontal=True
    )

if st.button("🔄 Atualizar Dados", use_container_width=True):
    st.rerun()

st.divider()

# --- BUSCANDO E EXIBINDO OS DADOS ---
with st.spinner("Buscando registros no banco de dados..."):
    try:
        response = requests.get(API_URL)
        
        if response.status_code == 200:
            visitantes = response.json()
            
            if visitantes:
                df = pd.DataFrame(visitantes)
                
                # Aplica o filtro de data, se houver
                if data_filtro:
                    nome_coluna_data = "data_visita" # Ajuste se necessário
                    if nome_coluna_data in df.columns:
                        data_texto = str(data_filtro)
                        df = df[df[nome_coluna_data].astype(str).str.contains(data_texto)]
                
                if df.empty:
                    st.info(f"Nenhum visitante encontrado para a data {data_filtro.strftime('%d/%m/%Y')}.")
                else:
                    st.caption(f"Total de registros encontrados: {len(df)}")
                    
                    # === A MÁGICA DA VISUALIZAÇÃO ACONTECE AQUI ===
                    
                    if "Celular" in modo_visao:
                        # 1. MODO CELULAR (CARDS)
                        lista_filtrada = df.to_dict('records')
                        for visitante in lista_filtrada:
                            nome = visitante.get("nome", "Visitante sem nome")
                            with st.expander(f"👤 {nome}", expanded=False):
                                st.write(f"**Data da Visita:** {visitante.get('data_visita', 'Não informada')}")
                                st.write(f"**Telefone:** {visitante.get('telefone', 'Não informado')}")
                                st.write(f"**Rede Social:** {visitante.get('rede_social', 'Não informada')}")
                                # Adicione mais campos aqui se quiser
                    else:
                        # 2. MODO COMPUTADOR (TABELA GRID)
                        st.dataframe(df, use_container_width=True)
                        
            else:
                st.info("Ainda não há nenhum visitante cadastrado no sistema.")
                
        else:
            st.error(f"❌ Erro ao buscar dados. Código: {response.status_code}")
            
    except requests.exceptions.RequestException:
        st.error("🔌 Erro de conexão com a API no Render.")
