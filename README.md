# [![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://ai-assistente-de-curriculo.streamlit.app)

# 🤖 Assistente de Currículo IA



Este projeto é um **assistente inteligente** desenvolvido para ajudar candidatos a otimizarem seus currículos para vagas específicas, utilizando o poder da IA (Gemini 2.0 Flash).

<img width="1918" height="962" alt="image" src="https://github.com/user-attachments/assets/76cff744-605d-40c2-8608-8e999af134c1" />


## 🌟 O que a aplicação faz?
A aplicação analisa a compatibilidade entre um **currículo (PDF)** e uma **descrição de vaga**, fornecendo:
* **Match Score:** Uma porcentagem visual de aderência técnica. 📊
* **Análise Geral:** Um resumo estratégico do perfil do candidato. 📝
* **Diferenciais:** Sugestões de pontos fortes que devem ser destacados. 💪
* **Gaps Técnicos:** Identificação de lacunas e como compensá-las. ⚠️
* **Plano de Ação:** Sugestões práticas de palavras-chave e reescrita de experiências (Método STAR). 💡
* **Relatório PDF:** Geração de um documento profissional com todas as sugestões. 📄

## 🎯 Intenção
A intenção deste projeto é servir como uma ferramenta de **apoio e mentoria**. O foco não é apenas dar uma nota, mas oferecer **sugestões construtivas** para que o usuário entenda como o mercado (e os sistemas de triagem ATS) podem interpretar seu perfil.

## ⚠️ Disclaimer (Aviso Legal)
Esta é uma ferramenta baseada em Inteligência Artificial Experimental. 
* As análises fornecidas são **sugestões** e não garantem aprovação em processos seletivos.
* Recomenda-se que o usuário valide todas as informações antes de aplicá-las.
* Os dados são processados via API do Google Gemini; verifique as políticas de privacidade do provedor.

## 🚀 Como rodar o projeto

Siga os passos abaixo para configurar o ambiente e executar a aplicação localmente:

### 1. Criar o Ambiente Virtual
Isso garante que as bibliotecas do projeto não conflitem com outras no seu computador.
```bash
python -m venv .venv
```

### 2. Ativar o Ambiente Virtual

No Windows:

```bash
.\.venv\Scripts\activate
```

No Linux/Mac:

```bash
source .venv/bin/activate
```

### 3. Instalar as Dependências
Instale todas as bibliotecas necessárias listadas no arquivo requirements.txt.

```bash
pip install -r requirements.txt
```

### 4. Executar a Aplicação
Inicie o servidor do Streamlit para abrir a interface no seu navegador.

```bash
python -m streamlit run app.py
```

Desenvolvido com ❤️ para impulsionar carreiras.


---

### 5. 📂 Estrutura de Pastas
services/: Contém a lógica central da aplicação, como a comunicação com a API do Gemini e o processamento de IA. 🧠

utils/: Reúne funções utilitárias e auxiliares, como formatadores de texto e ferramentas para geração de arquivos PDF. 🛠️

components/: Foca nos elementos da interface visual (UI) do Streamlit, garantindo que o design esteja separado da lógica. 🎨

### 6.🔐 Guia de API Key (Google AI Studio)

A aplicação utiliza o modelo **Gemini 2.0 Flash**. Para obter sua chave gratuita, siga estes passos:

1.  Acesse o [Google AI Studio](https://aistudio.google.com/).

2.  Faça login com sua conta Google.

3.  No menu lateral, clique em **"Get API key"**.

4.  Clique no botão **"Create API key in new project"**.

5.  Copie a chave gerada e cole-a no campo correspondente na barra lateral da aplicação.
Obs: Cuidado com os limites

<img width="1918" height="972" alt="image" src="https://github.com/user-attachments/assets/99b97803-2770-44ad-a419-c73ee79c9825" />

# Resultado

   
