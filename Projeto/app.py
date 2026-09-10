import os
import streamlit as st
from groq import Groq
from dotenv import load_dotenv

# Carrega chave do arquivo .env se existir
load_dotenv()

# 1. Configuração da página
st.set_page_config(
    page_title="Agente IA - Groq",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 Agente Inteligente com Groq & Streamlit")

# 2. Barra Lateral - Configurações
st.sidebar.header("⚙️ Configurações do Agente")

api_key_input = st.sidebar.text_input(
    "Groq API Key", 
    type="password", 
    value=os.getenv("GROQ_API_KEY", "")
)

if not api_key_input:
    st.info("Insira sua chave API na barra lateral ou no arquivo `.env` para iniciar.", icon="🔑")
    st.stop()

# Inicializa cliente da API
client = Groq(api_key=api_key_input)

# Instruções para o comportamento do Agente
system_prompt = st.sidebar.text_area(
    "Instruções do Sistema (System Prompt):",
    value="Você é um assistente virtual prestativo, preciso e direto ao ponto.",
    height=120
)

# Parâmetros do modelo
modelo_selecionado = st.sidebar.selectbox(
    "Modelo:",
    ["openai/gpt-oss-120b"],
    index=0
)

temperatura = st.sidebar.slider("Criatividade (Temperatura):", 0.0, 1.0, 0.7, 0.1)

# Botão para reiniciar conversa
if st.sidebar.button("🧹 Limpar Conversa", use_container_width=True):
    st.session_state.messages = []
    st.rerun()

# 3. Gerenciamento de Estado das Mensagens
if "messages" not in st.session_state:
    st.session_state.messages = []

# Exibe histórico de mensagens na tela
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. Processamento da Pergunta do Usuário
if pergunta := st.chat_input("Digite sua pergunta..."):
    # Registra e mostra a mensagem do usuário
    st.session_state.messages.append({"role": "user", "content": pergunta})
    with st.chat_message("user"):
        st.markdown(pergunta)

    # Processa e exibe a resposta via Streaming
    with st.chat_message("assistant"):
        try:
            # Constrói o histórico enviando primeiro o System Prompt
            mensagens_payload = [{"role": "system", "content": system_prompt}]
            mensagens_payload.extend([
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ])

            # Chamada Streaming para a API da Groq
            stream = client.chat.completions.create(
                messages=mensagens_payload,
                model=modelo_selecionado,
                temperature=temperatura,
                stream=True,
            )

            # Exibe o texto enquanto é gerado
            resposta = st.write_stream(
                chunk.choices[0].delta.content or "" for chunk in stream
            )

            # Salva no histórico do Streamlit
            st.session_state.messages.append({"role": "assistant", "content": resposta})

        except Exception as e:
            st.error(f"Erro ao conectar com a API: {e}")