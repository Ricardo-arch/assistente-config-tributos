import streamlit as st
import streamlit_authenticator as stauth
import openai

# CONFIGURAÇÃO DO ASSISTENTE
openai.api_key = st.secrets["OPENAI_API_KEY"] 
# Substitua pela sua chave da OpenAI

# Lista de usuários autorizados
names = ['Ricardo Artiq']
usernames = ['ricardo.santana@artiq.com.br']
passwords = ['1*Sigauser*alfa']  # Senha provisória (pode ser alterada depois)

hashed_passwords = stauth.Hasher(passwords).generate()

authenticator = stauth.Authenticate(
    names, usernames, hashed_passwords,
    "config_tributos_app", "abcdef", cookie_expiry_days=1
)

name, authentication_status, username = authenticator.login("Login", "main")

if authentication_status:
    st.title("🤖 Assistente de Configuração de Tributos - Protheus TOTVS")
    st.success(f"Bem-vindo, {name}!")

    user_input = st.text_area("Digite sua dúvida sobre o Configurador de Tributos:")

    if st.button("Perguntar"):
        if user_input:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": (
                        "Você é um assistente especialista no novo Configurador de Tributos do sistema Protheus da TOTVS. "
                        "Seu papel é ajudar o usuário a entender a nova rotina do sistema com clareza e paciência. "
                        "Explique conceitos, regras fiscais, exceções, parametrizações e testes de forma acessível e com exemplos práticos. "
                        "Evite jargões sem explicação, destaque erros comuns, e incentive boas práticas. "
                        "Se o usuário não for claro, faça perguntas para entender melhor. "
                        "Considere sempre o contexto fiscal e contábil do Brasil atual."
                    )},
                    {"role": "user", "content": user_input}
                ]
            )
            st.markdown("### Resposta:")
            st.write(response['choices'][0]['message']['content'])
        else:
            st.warning("Por favor, digite uma pergunta antes de clicar em 'Perguntar'.")

elif authentication_status is False:
    st.error("Usuário ou senha incorretos.")
elif authentication_status is None:
    st.warning("Por favor, insira suas credenciais.")
