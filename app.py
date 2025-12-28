import streamlit as st
import google.generativeai as genai
from datetime import datetime

# ==============================
# 1. CONFIGURAÇÃO DA PÁGINA
# ==============================
st.set_page_config(
    page_title="LEGIA v2.4",
    page_icon="⚖️",
    layout="wide"
)

# ==============================
# 2. ESTILO (CSS)
# ==============================
st.markdown("""
<style>
    html, body, [class*="css"]  {
        font-size: 16px;
    }
    .block-container {
        padding-top: 4rem !important; 
        padding-bottom: 4rem !important;
        max-width: 95% !important; 
    }        
    .stTextArea textarea {
        font-size: 16px !important;
        font-family: 'Courier New', Courier, monospace;
        line-height: 1.2;
    }
    .stButton button {
        font-size: 18px !important;
        font-weight: bold !important;
    }
</style>
""", unsafe_allow_html=True)

# ==============================
# 3. SEGURANÇA
# ==============================
def check_password():
    if "senha_acesso" not in st.secrets:
        return True
    
    def password_entered():
        if st.session_state["password"] == st.secrets["senha_acesso"]:
            st.session_state["password_correct"] = True
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.text_input("🔑 Senha do Sistema:", type="password", on_change=password_entered, key="password")
        return False
    elif not st.session_state["password_correct"]:
        st.error("Senha incorreta.")
        st.text_input("Tente novamente:", type="password", on_change=password_entered, key="password")
        return False
    else:
        return True

if not check_password():
    st.stop()

# ==============================
# 4. AVISOS
# ==============================
with st.container():
    st.warning(
        """
        ⚠️ **AVISO:** Sistema em fase BETA. O conteúdo é gerado por IA e **deve ser revisado** juridicamente. 
        """
    )

# ==============================
# 5. BACKEND (AUTO-DISCOVERY DO GOOGLE)
# ==============================
model_name_used = "Desconhecido"

try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    
    available_models = []
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            available_models.append(m.name)
            
    preferencias = ['models/gemini-1.5-flash', 'models/gemini-1.5-pro', 'models/gemini-1.0-pro', 'models/gemini-pro']
    
    chosen_model = None
    for pref in preferencias:
        if pref in available_models:
            chosen_model = pref
            break
            
    if not chosen_model and available_models:
        chosen_model = available_models[0]
        
    if not chosen_model:
        st.error("Erro Crítico: Nenhum modelo de texto disponível na sua conta Google.")
        st.stop()
        
    model = genai.GenerativeModel(chosen_model)
    model_name_used = chosen_model
    
except Exception as e:
    st.error(f"Erro de Conexão com Google: {e}")
    st.stop()

# ==============================
# 6. PROMPTS
# ==============================
PROMPTS = {
    "Projeto de Lei": """
    Atue como Procurador Legislativo. Redija MINUTA DE PROJETO DE LEI.
    REGRAS DE FORMATAÇÃO:
    - Use NEGRITO (**texto**) nos títulos de artigos (ex: **Art. 1º**).
    - Use CAIXA ALTA e NEGRITO na Ementa.
    - Evite vício de iniciativa.
    ESTRUTURA: Ementa, Artigos, Cláusulas, Justificativa no final.
    """,
    "Indicação": """
    Atue como Assessor. Redija INDICAÇÃO.
    REGRAS: Use NEGRITO nos nomes e títulos.
    ESTRUTURA: Vocativo, Solicitação, Justificativa no final.
    """,
    "Pedido de Providência": """
    Atue como Assessor. Redija PEDIDO DE PROVIDÊNCIA.
    REGRAS: Destaque o local e o problema em NEGRITO. Justificativa no final
    """,
    "Pedido de Informação": """
    Atue como Fiscal. Redija PEDIDO DE INFORMAÇÃO.
    REGRAS: Use lista numerada. Destaque os prazos em NEGRITO. Justificativa no final
    """,
    "Moção": """
    Atue como Assessor. Redija MOÇÃO.
    REGRAS: Linguagem solene. Destaque o homenageado em NEGRITO. Justificativa no final
    """,
    "Ofício de Gabinete": """
    Atue como Chefe de Gabinete. Redija OFÍCIO.
    REGRAS: Assunto, Cabeçalho formal, Texto Formal, Respeitoso, Texto Rico.
    """
}

# ==============================
# 7. INTERFACE
# ==============================
st.title("⚖️ LEGIA")
st.caption(f"Desenvolvido por Daniel Colvero, 2025-2026. (Motor: {model_name_used})")
st.markdown("---")

col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("Parâmetros")
    tipo = st.selectbox("Documento:", list(PROMPTS.keys()))
    autor = st.text_input("Parlamentar:", placeholder="Ex: Ver. Daniel Oliveira")
    partido = st.text_input("Partido:", placeholder="Ex: MDB")
    cidade = st.text_input("Município:", value="Espumoso - RS")

with col2:
    st.subheader("Dados da Matéria")
    assunto = st.text_area(
        "Instruções:",
        height=200,
        placeholder="Descreva o que você precisa com o maior detalhamento possível. Pedidos genéricos geram textos genéricos."
    )

# ==============================
# 8. LÓGICA DE MEMÓRIA (SESSION STATE)
# ==============================

# Inicializa a memória se ela não existir
if "texto_final" not in st.session_state:
    st.session_state["texto_final"] = ""

# Botão de Geração
if st.button("⚡ Executar LEGIA", type="primary", use_container_width=True):
    if not assunto.strip():
        st.warning("⚠️ Escreva algo no campo de instruções.")
    else:
        with st.spinner(f"Redigindo minuta usando {model_name_used}..."):
            prompt_final = f"""
            {PROMPTS[tipo]}
            --- DADOS ---
            CIDADE: {cidade} | AUTOR: {autor} | PARTIDO: {partido} | DATA: {datetime.now().strftime("%d/%m/%Y")}
            --- PEDIDO ---
            {assunto}
            --- REGRA FINAL ---
            Capriche no português culto e formal. Use Markdown para formatar títulos em negrito.
            """

            try:
                response = model.generate_content(prompt_final)
                # AQUI ESTÁ O SEGREDINHO: Salvamos na memória da sessão
                st.session_state["texto_final"] = response.text
                st.success("Gerado com sucesso!")
            except Exception as e:
                st.error(f"Erro na geração: {e}")

# ==============================
# 9. EXIBIÇÃO PERSISTENTE
# ==============================
# Só mostra a área de resultado se tiver algo na memória
if st.session_state["texto_final"]:
    st.markdown("---")
    st.subheader("Resultado")
    
    tab1, tab2 = st.tabs(["📝 Leitura Formatada", "📝 Copiar Texto"])
    
    with tab1:
        st.markdown("### Visualização Prévia")
        st.markdown(st.session_state["texto_final"])
        
    with tab2:
        st.text_area("Copie daqui:", value=st.session_state["texto_final"], height=600)
    
    # Agora o botão de download usa a memória. Mesmo se recarregar, a memória mantém o texto na tela.
    nome_arquivo = f"LEGIA_{tipo.replace(' ', '')}_{datetime.now().strftime('%Y%m%d')}.txt"
    st.download_button(
        label="💾 Baixar Texto (.txt)", 
        data=st.session_state["texto_final"], 
        file_name=nome_arquivo
    )

# ==============================
# 10. RODAPÉ
# ==============================
st.markdown("---")
st.markdown("<div style='text-align: center; color: grey;'>LEGIA v2.4 • Daniel Colvero • 2026</div>", unsafe_allow_html=True)