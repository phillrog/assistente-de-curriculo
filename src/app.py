import streamlit as st
import re
from pypdf import PdfReader
from datetime import datetime
from services.assistente_curriculo_service import AssitenteCurriculo 
from utils.formatadores import extrair_secao, limpar_estilo
from utils.pdf_utils import gerar_relatorio_pdf
from utils.logger import StreamlitLogger
from components.ui_elements import renderizar_cabecalho, renderizar_gauge, exibir_manual

# 1. Configuração da página
st.set_page_config(
    page_title="Mentor de Carreira IA", 
    layout="wide", 
    page_icon="🤝",
    initial_sidebar_state="expanded"
)

def limpar_sessao():
    st.session_state.messages = []
    st.session_state.cv_content = ""
    st.session_state.logs = []
    st.session_state.ultimo_prompt = ""

# 2. Inicialização do Estado (Session State)
if "messages" not in st.session_state: st.session_state.messages = []
if "cv_content" not in st.session_state: st.session_state.cv_content = ""
if "tom_estilo" not in st.session_state: st.session_state.tom_estilo = "Seja encorajador, empático e amigável. Foque no potencial e no crescimento."
if "logs" not in st.session_state: st.session_state.logs = []
if "ultimo_prompt" not in st.session_state: st.session_state.ultimo_prompt = ""

def adicionar_log(mensagem):
    hora = datetime.now().strftime("%H:%M:%S")
    st.session_state.logs.append(f"[{hora}] {mensagem}")
    

# Instanciamos o logger global do app aqui
logger_visual = StreamlitLogger(adicionar_log)

def resolve_assistente(api_key, temp):
    """
    Esta função atua como container de DI. 
    Ela resolve as dependências e injeta o logger no assistente.
    """
    
    # 2. Injetamos as dependências no serviço
    return AssitenteCurriculo(
        api_key=api_key, 
        logger=logger_visual, 
        temperature=temp
    )    

# 3. Interface Visual Fixa
renderizar_cabecalho()

main_placeholder = st.empty()


# 5. SIDEBAR
with st.sidebar:
    st.title("Configurações")
    
    api_key = st.text_input("Google API Key", type="password")

    # SELETOR DE TOM EDITÁVEL
    st.write("---")
    st.subheader("🎭 Personalidade da IA")
    
    toms_predefinidos = {
        "Amigável": "Seja encorajador, empático e amigável. Foque no potencial e no crescimento.",
        "Realista": "Seja direto, sincero e realista. Aponte falhas críticas como um recrutador rigoroso faria.",
        "Personalizado": st.session_state.tom_estilo if "Seja" not in st.session_state.tom_estilo else ""
    }
    
    opcao_tom = st.selectbox("Escolha um estilo base:", list(toms_predefinidos.keys()))
    
    # Campo visível para edição do prompt do Tom
    st.session_state.tom_estilo = st.text_area(
        "Prompt do Tom (Edite se desejar):", 
        value=toms_predefinidos[opcao_tom],
        height=100
    )

    # AJUSTE DE TEMPERATURA
    st.write("---")
    st.subheader("⚙️ Temperatura")
    temp_value = st.slider("Nível de Criatividade", 0.0, 1.0, 0.2, 0.1)
    
    if temp_value <= 0.2:
        st.caption("💡 **Dica:** Temperaturas baixas tornam as respostas mais assertivas e as notas mais consistentes.")
    else:
        st.caption("🎨 **Dica:** Temperaturas altas aumentam a criatividade, mas as notas podem variar entre análises.")
    
    st.write("---")
    job_desc = st.text_area("🎯 Vaga dos seus Sonhos", height=150)
    uploaded_file = st.file_uploader("📂 Seu Currículo Atual (PDF)", type="pdf")
    
    st.write("---")
    
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        btn_iniciar = st.button("🚀 ANALISAR")
    with col_btn2:
        btn_limpar = st.button("🗑️ LIMPAR")

    if btn_iniciar:
        if api_key and job_desc and uploaded_file:
            logger_visual.info("Iniciando processo de análise...")
            with main_placeholder.container():
                st.markdown(f"""
                    <div class="loader-overlay">
                        <div class="loader-circle"></div>
                        <h2 style='color: #4A90E2; font-family: sans-serif;'>🔮 Analisando...</h2>
                        <p style='color: #666; font-family: sans-serif;'>Aguarde um momento enquanto preparo sua avaliação.</p>
                    </div>
                """, unsafe_allow_html=True)

                try:
                    logger_visual.info("Lendo arquivo PDF...")
                    reader = PdfReader(uploaded_file)
                    st.session_state.cv_content = "".join([p.extract_text() for p in reader.pages])
                    logger_visual.info(f"PDF lido: {len(st.session_state.cv_content)} caracteres extraídos.")
                    
                    logger_visual.info("Conectando ao Gemini 2.0 Flash via LangChain...")
                    analyzer = resolve_assistente(api_key, temp_value)
                                        
                    logger_visual.info("Enviando prompt de análise estratégica...")
                    res = analyzer.chat(
                        st.session_state.cv_content, 
                        job_desc, 
                        "", 
                        "Analise meu currículo agora seguindo o formato de tags [RESUMO], [PONTOS_FORTES], [GAPS], [SUGESTOES], [DICAS_OURO] e [NOTA].",
                        st.session_state.tom_estilo
                    )
                    
                    # Pega o prompt que acabou de ser gerado e salva na sessão
                    st.session_state.ultimo_prompt = analyzer.ultimo_prompt_renderizado
                    
                    logger_visual.info("Análise recebida com sucesso!")
                    st.session_state.messages = [{"role": "assistant", "content": res}] 
                    
                    st.components.v1.html("""<script>var b = window.parent.document.querySelector('button[data-testid="stSidebarCollapseButton"]'); if(b) b.click();</script>""", height=0)
                    st.rerun()
                except Exception as e:
                    logger_visual.error(f"ERRO: {str(e)}")
                    main_placeholder.empty()
                    st.error(f"Erro: {e}")
        else:
            st.warning("Preencha todos os campos para continuar.")

    if btn_limpar:
        logger_visual.info("Limpando histórico e sessão.")
        limpar_sessao()
        st.rerun()
        
    st.markdown("---")
    
    
    st.caption("""
        ⚠️ **Nota de Transparência:** Este assistente oferece sugestões baseadas em processamento de dados. 
        As recomendações não garantem aprovação em processos seletivos e devem ser validadas por você. 
        Como uma tecnologia experimental (Gemini 2.0 Flash), as análises podem conter imprecisões.
        """)
    
    st.markdown(
        "<div style='text-align: center; color: #999; font-size: 12px;'>"
        "Desenvolvido por <b>Phillipe</b> | Assistente de Currículo IA v1.0"
        "</div>", 
        unsafe_allow_html=True
    )
    
    # --- LOG VISUAL (NOVA SEÇÃO) ---
    st.write("---")
    with st.expander("🛠️ Inspecionar Logs e Prompt", expanded=False):
        tab1, tab2 = st.tabs(["Logs", "Último Prompt"])
        with tab1:
            if st.session_state.logs:
                logs_para_download = "\n".join(st.session_state.logs)
                
                # Exibição visual na tela
                for log in reversed(st.session_state.logs):
                    st.caption(log)
                    
                st.write("---")
        
                # Botão de exportação do log
                st.download_button(
                    label="📄 Baixar Histórico de Logs",
                    data=logs_para_download,
                    file_name=f"logs_sessao_{datetime.now().strftime('%H%M%S')}.txt",
                    mime="text/plain",
                    key="btn_download_logs"
                )
            else:
                st.caption("Aguardando atividades...")
        with tab2:
            if st.session_state.ultimo_prompt:
                st.code(st.session_state.ultimo_prompt, language="markdown")
                st.write("---")
                # Botão dedicado para baixar o prompt como arquivo .txt
                st.download_button(
                    label="📄 Baixar Prompt Estruturado",
                    data=st.session_state.ultimo_prompt,
                    file_name="prompt_enviado.txt",
                    mime="text/plain"
                )
            else:
                st.caption("Nenhum prompt executado ainda.")
    
# 6. CONTEÚDO DINÂMICO
if not st.session_state.messages:
    with main_placeholder.container():
        st.info("### Bem-vindo ao seu Assistente de Currículo! 🌟")
        # --- AVISO SOBRE IA ---
        st.warning("""
        ⚠️ **Nota de Transparência:** Este assistente oferece sugestões baseadas em processamento de dados. 
        As recomendações não garantem aprovação em processos seletivos e devem ser validadas por você. 
        Como uma tecnologia experimental (Gemini 2.0 Flash), as análises podem conter imprecisões.
        """)

        st.markdown("---")
        st.markdown("### 🛠️ Como usar em 4 etapas:")
        
        # Criando colunas para as etapas
        step1, step2, step3, step4 = st.columns(4)
        
        with step1:
            st.markdown("#### 1. API Key\nInsira sua chave do Google Gemini na barra lateral.")
        with step2:
            st.markdown("#### 2. A Vaga\nCole a descrição da vaga que você deseja aplicar.")
        with step3:
            st.markdown("#### 3. O Currículo\nSuba o seu currículo atual no formato PDF.")
        with step4:
            st.markdown("#### 4. Analisar\nClique em 'Analisar' e receba seu feedback completo!")

        st.markdown("---")
        st.markdown("### ⚙️ Por trás do código:")
        st.write("Configura a análise na barra lateral para começarmos a trabalhar no seu sucesso.")
        c1, c2, c3 = st.columns(3)
        c1.markdown("#### 💎 Valorização\nIdentificamos o que você tem de melhor.")
        c2.markdown("#### 🎯 Precisão\nAjustamos seu currículo para o que a vaga pede.")
        c3.markdown("#### 💬 Mentoria\nPeça cartas, dicas e simulações de entrevista.")

for i,msg in enumerate(st.session_state.messages):
    with st.chat_message(msg["role"]):
        if "[RESUMO]" in msg["content"]:
            texto = msg["content"]
            resumo = extrair_secao(texto, "[RESUMO")
            fortes = extrair_secao(texto, "[PONTOS_FORTES")
            gaps = extrair_secao(texto, "[GAPS")
            sugestoes = extrair_secao(texto, "[SUGESTOES")
            dicas_dinamicas = extrair_secao(texto, "[DICAS_OURO") 
            
            nota_raw = extrair_secao(texto, "[NOTA")
            n_match = re.search(r"(\d+\.?\d*)", nota_raw)
            if n_match:
                val = float(n_match.group(1))
                score = int(val * 10) if val <= 10 else int(val)
            else:
                score = 0
            score = min(max(score, 0), 100)

            # --- BOTÃO DE EXPORTAR PDF (DENTRO DO BLOCO DE ANÁLISE) ---
            pdf_bytes = gerar_relatorio_pdf(texto, score)
            st.warning("""
        ⚠️ **Nota de Transparência:** Este assistente oferece sugestões baseadas em processamento de dados. 
        As recomendações não garantem aprovação em processos seletivos e devem ser validadas por você. 
        Como uma tecnologia experimental (Gemini 2.0 Flash), as análises podem conter imprecisões.
        """)
            st.download_button(
                label="📥 Baixar Análise em PDF",
                data=pdf_bytes,
                file_name=f"Analise_Carreira_{datetime.now().strftime('%d%m%Y')}.pdf",
                mime="application/pdf",
                key=f"btn_download_{i}"
            )
            # --------------------------------------------------------

            c_main, c_side = st.columns([3, 1])
            with c_main:
                st.subheader("📝 Avaliação do Assistente")
                st.write(resumo)
            with c_side:
                renderizar_gauge(score)
            
            if dicas_dinamicas:
                st.markdown(f"""
                <div style="background-color: #f0f7ff; padding: 20px; border-left: 5px solid #4A90E2; border-radius: 10px; margin: 15px 0;">
                    <h4 style="margin-top: 0; color: #1e3a8a; font-family: sans-serif;">✨ Dicas de Ouro Personalizadas</h4>
                    <div style="color: #374151; font-size: 14px; line-height: 1.6;">
                """, unsafe_allow_html=True)
                st.markdown(dicas_dinamicas)
                st.markdown("</div></div>", unsafe_allow_html=True)

            st.write("---")
            b1, b2, b3 = st.columns(3)
            with b1: st.info(f"**💪 Seus Diferenciais**\n\n{fortes}")
            with b2: st.warning(f"**⚠️ Onde Melhorar**\n\n{gaps}")
            with b3: st.success(f"**💡 Plano de Ação**\n\n{sugestoes}")
            
            st.markdown(f"**Pontuação de Match Final: {score}/100**")
            
            corpo_extra = re.sub(r"\[.*?\]", "", texto).replace(resumo, "").strip()
            if len(corpo_extra) > 50:
                st.markdown("---")
                st.markdown(corpo_extra)
                
            st.warning("""
        ⚠️ **Nota de Transparência:** Este assistente oferece sugestões baseadas em processamento de dados. 
        As recomendações não garantem aprovação em processos seletivos e devem ser validadas por você. 
        Como uma tecnologia experimental (Gemini 2.0 Flash), as análises podem conter imprecisões.
        """)
        else:
            st.markdown(msg["content"])
        

if prompt := st.chat_input("Pergunte algo ao Assistente..."):
    if not st.session_state.cv_content:
        st.error("Realize a análise inicial primeiro!")
    else:
        logger_visual.info(f"Usuário perguntou: '{prompt}'")
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.rerun()

st.warning("""
        ⚠️ **Nota de Transparência:** Este assistente oferece sugestões baseadas em processamento de dados. 
        As recomendações não garantem aprovação em processos seletivos e devem ser validadas por você. 
        Como uma tecnologia experimental (Gemini 2.0 Flash), as análises podem conter imprecisões.
        """)

if len(st.session_state.messages) > 0 and st.session_state.messages[-1]["role"] == "user":
    with st.chat_message("assistant"):
        with st.spinner("Preparando resposta..."):
            logger_visual.info("Gerando resposta baseada no histórico do chat...")
            analyzer = resolve_assistente(api_key, temp_value)
            analise_contexto = st.session_state.messages[0]["content"]
            hist = f"CONTEXTO DA ANÁLISE:\n{analise_contexto}"
            response = analyzer.chat(st.session_state.cv_content, job_desc, hist, st.session_state.messages[-1]["content"], st.session_state.tom_estilo)
            logger_visual.info("Resposta do chat gerada.")
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})