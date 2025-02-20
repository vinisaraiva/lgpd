import streamlit as st
import requests
import os
from openai import OpenAI

# Configurar a API da OpenAI (substitua pela sua chave)
# OPENAI_API_KEY = "SUA_CHAVE_API_AQUI"

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

# Configuração inicial da página
st.set_page_config(page_title=("Análise aviso LGPD"), page_icon=":bar_chart:", layout="wide")



def get_text_from_url(url):
    """Tenta obter o conteúdo da política de privacidade de um site"""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        return f"Erro ao acessar a URL: {e}"

def analyze_text_with_gpt(text):
    """Envia o texto para o GPT e recebe uma análise sobre conformidade com a LGPD"""
    prompt = f"""
    Analise a seguinte Política de Privacidade e verifique se está em conformidade com a LGPD. 
    Gere um relatório com tópicos claros, indicando se está adequada ou se há algo faltando.
    Caso falte algo, detalhe os pontos ausentes.

    Texto da Política de Privacidade:
    {text}

    Responda de forma organizada e objetiva, usando tópicos como:
    - Conformidade geral
    - Consentimento do usuário
    - Direitos do usuário
    - Transparência na coleta de dados
    - Segurança e armazenamento
    - Compartilhamento de dados
    - Recomendações de melhoria
    """

    try:
        response = client.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "system", "content": "Você é um especialista em conformidade com a LGPD."},
                      {"role": "user", "content": prompt}],
            api_key=OPENAI_API_KEY
        )
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Erro na análise: {e}"

# Interface Streamlit
st.title("Analisador de Conformidade LGPD")
st.write("Copie o link da política de privacidade de um site ou cole o texto diretamente para análise.")

# Campo para inserir URL ou texto manualmente
url = st.text_input("Insira o link da Política de Privacidade do site (opcional):")
texto_manual = st.text_area("Ou cole o texto da Política de Privacidade aqui:")

# Botão para Analisar
if st.button("Analisar"):
    if url:
        texto = get_text_from_url(url)
    elif texto_manual:
        texto = texto_manual
    else:
        st.error("Por favor, insira um link válido ou cole um texto.")
        texto = None
    
    if texto:
        with st.spinner("Analisando o texto..."):
            resultado = analyze_text_with_gpt(texto)
        st.subheader("Relatório de Conformidade LGPD")
        st.write(resultado)
