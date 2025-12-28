# [![Build - Assistente de Currículo](https://github.com/phillrog/assistente-de-curriculo/actions/workflows/build-com-conda.yml/badge.svg)](https://github.com/phillrog/assistente-de-curriculo/actions/workflows/build-com-conda.yml) - [![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://ai-assistente-de-curriculo.streamlit.app)

# 🤖 Assistente de Currículo IA



Este projeto é um **assistente inteligente** desenvolvido para ajudar candidatos a otimizarem seus currículos para vagas específicas, utilizando o poder da IA (Gemini 2.0 Flash e Gemini 3 Flash (Preview)).

<img width="1908" height="1007" alt="image" src="https://github.com/user-attachments/assets/e1534d72-adb3-4c02-a847-84b5743d32d8" />



## 🌟 O que a aplicação faz?
A aplicação analisa a compatibilidade entre um **currículo (PDF)** e uma **descrição de vaga**, fornecendo:
* **Match Score:** Uma porcentagem visual de aderência técnica. 📊
* **Análise Geral:** Um resumo estratégico do perfil do candidato. 📝
* **Diferenciais:** Sugestões de pontos fortes que devem ser destacados. 💪
* **Gaps Técnicos:** Identificação de lacunas e como compensá-las. ⚠️
* **Plano de Ação:** Sugestões práticas de palavras-chave e reescrita de experiências (Método STAR). 💡
* **Relatório PDF:** Geração de um documento profissional com todas as sugestões. 📄
* **Inspeção:** Você pode ver o log e o prompt executado. 🔥
* **Storytelling:** Ajuda com narrativas de resolução de problemas e evolução profissional.🔥

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
### 5\. ⚙️ Estrutura e Engenharia de Prompt

A inteligência do sistema baseia-se em um prompt estruturado que utiliza técnicas avançadas de **Few-Shot Prompting** e **Delimitadores XML** para garantir precisão e segurança. A estrutura foi desenhada para separar claramente as instruções do sistema dos dados sensíveis do usuário.

**Principais pilares da estrutura:**

-   **Persona Profile:** Define a IA como um especialista em recrutamento e psicologia. Esta técnica de atribuição de papel aumenta a precisão do modelo para domínios específicos.

    -   *Fonte:* [Google Cloud - Role Prompting Strategy](https://www.google.com/search?q=https://cloud.google.com/vertex-ai/docs/generative-ai/learn/introduction-prompt-design%23assign-role)

-   **XML Tagging:** Utiliza tags como `<vaga>` e `<curriculo>` para delimitar contextos, uma técnica recomendada para evitar "instrução de injeção" (Prompt Injection) e melhorar o parsing de dados.

    -   *Fonte:* [Anthropic - Use XML Tags for clear separation](https://www.google.com/search?q=https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/use-xml-tags)

-   **Format Constraints:** Garante que a saída seja sempre padronizada em tags (`[RESUMO]`, `[NOTA]`, etc.). O uso de restrições de formato é essencial para integração com interfaces de usuário (UI).

    -   *Fonte:* [OpenAI - Structured Outputs Guide](https://platform.openai.com/docs/guides/structured-outputs)

-   **Tactical Guidelines:** Aplica metodologias reais de mercado:

    -   **Método STAR:** Padrão ouro para descrição de conquistas profissionais.

        -   *Referência:* [MIT Career Advising - STAR Method](https://www.google.com/search?q=https://capd.mit.edu/resources/star-method-for-resumes-and-interviews/)

    -   **Otimização para ATS:** Técnicas para alinhar o currículo aos algoritmos de triagem automática.

        -   *Referência:* [Harvard Business Review - How to Design a Resume for ATS](https://www.google.com/search?q=https://hbr.org/2022/01/how-to-design-a-resume-for-applicant-tracking-systems)

-   **Análise de Narrativa (Career Storytelling):** Esta técnica vai além da análise estática de palavras-chave. Ela foca na **coerência da trajetória** do candidato, transformando descrições passivas de cargos em narrativas de resolução de problemas e evolução profissional.

    -   *Referência:* [HBR - The Art of Career Storytelling](https://www.google.com/search?q=https://hbr.org/2016/01/the-art-of-career-storytelling) | [Forbes - Why Storytelling Is The Future Of Resumes](https://www.google.com/search?q=https://www.forbes.com/sites/forbeshumanresourcescouncil/2021/04/14/why-storytelling-is-the-future-of-the-resume/)

-   **Curadoria de Estudos (Upskilling & Gap Bridging):** Implementa o conceito de **"Recolocação Orientada ao Aprendizado"**, transformando cada falha técnica identificada em um plano de ação prático por meio de links diretos para recursos educativos.

    -   *Referência:* [Roadmap.sh - Learning Paths](https://roadmap.sh/) | [World Economic Forum - Reskilling Revolution](https://www.weforum.org/agenda/2020/01/reskilling-revolution-jobs-future-skills/)

**Exemplo do Prompt Renderizado:**

```

--- PROMPT ENVIADO AO GEMINI ---

SUA MISSÃO: Transformar o currículo de um CANDIDATO desempregado em um documento de ALTO IMPACTO que vença os robôs (ATS) e encante recrutadores humanos.

VOCÊ É: Um Especialista em Recrutamento Tech e Psicologia de Contratação.

### REGRAS DE OURO (Siga rigorosamente):
1. A [NOTA] deve ser baseada ESTREITAMENTE em critérios técnicos (Match de competências). Ela deve ser IDÊNTICA independentemente do tom escolhido (Amigável ou Realista ou Outro).
2. No campo [DICAS_OURO], use obrigatoriamente '**' para negrito nos títulos e '-' para listas.

### ESTILO DE RESPOSTA
** Tom da resposta
Seja encorajador, empático e amigável. Foque no potencial e no crescimento.

### CONTEXTO DE ENTRADA
Abaixo estão os dados que você deve processar. Considere apenas o conteúdo dentro das tags:

<vaga>
** Aqui dados da vaga
</vaga>

<curriculo>
** Aqui dados do currículo
</curriculo>

<historico_da_conversa>
** Caso quiser montar um histórico interativo
</historico_da_conversa>

### SOLICITAÇÃO ATUAL DO USUÁRIO
<comando>
Analise meu currículo agora seguindo o formato de tags [RESUMO], [PONTOS_FORTES], [GAPS], [SUGESTOES], [DICAS_OURO] e [NOTA].
</comando>

---
DIRETRIZES TÁTICAS PARA O ALTO IMPACTO:
1. FOCO EM ATS: Identifique as 5 palavras-chave essenciais da vaga que NÃO estão no currículo. Liste-as nas sugestões.
2. MÉTODO STAR: Escolha a experiência mais relevante do currículo e sugira uma reescrita rápida: (S)ituação, (T)arefa, (A)ção e (R)esultado quantificável.
3. MITIGAÇÃO DE GAPS: Para cada falha técnica, dê uma "saída estratégica". Como o candidato pode compensar esse gap?
4. FONTES E LINKS: Sempre que sugerir o estudo de uma tecnologia ou ferramenta (ex: Python, AWS, Scrum), procure fornecer um link de fonte confiável (Documentação oficial, Coursera, Udemy ou Microsoft Learn) para o candidato se aprofundar.
5. ANÁLISE DE NARRATIVA (STORYTELLING): Avalie se o currículo conta uma história de progressão clara. Se o currículo parecer uma "lista de tarefas", sugira como transformar essas tarefas em conquistas que demonstrem liderança ou autonomia, alinhadas à cultura de empresas tech modernas.
6. CURADORIA DE ESTUDOS (LINKS): Para cada GAP técnico identificado, você deve obrigatoriamente fornecer um link direto para aprendizado. Priorize:
- Documentações Oficiais (ex: react.dev, docs.python.org);
- Cursos Gratuitos (Microsoft Learn, Google Cloud Skills Boost, Coursera);
- Roadmap.sh para visualização de carreira.
- Formato: [Nome do Recurso](URL).

[RESUMO] -> (Análise direta baseada no TOM: Seja encorajador, empático e amigável. Foque no potencial e no crescimento.)
[PONTOS_FORTES] -> (Destaque o que torna este candidato ideal)
[GAPS] -> (O que falta? Seja honesto e dê a saída estratégica)
[SUGESTOES] -> 
- 🔑 **5 Palavras-chave:** (Liste-as aqui)
- 🚀 **Método STAR:** (Exemplo de reescrita)
- 💡 **Storytelling:** (Insight de narrativa)
- 📚 **CURADORIA DE LINKS:** (Para cada GAP técnico citado acima, forneça obrigatoriamente um link [Nome](URL) seguindo a Diretriz 6)
[DICAS_OURO] -> (Gere 3 dicas PERSONALIZADAS e acionáveis para quem busca recolocação).
[NOTA] -> (Número de 0 a 100 baseado em match técnico real)

---
REGRA DE ENGAJAMENTO:
Sempre termine sua resposta com uma "PERGUNTA DE MENTOR" desafiadora para o usuário.
Exemplo: "Quer que eu simule uma pergunta difícil desta vaga para você treinar?" ou
"Gostaria que eu escrevesse uma mensagem de abordagem para você enviar ao recrutador no LinkedIn?"


### FORMATO OBRIGATÓRIO DE RESPOSTA:
Gere o relatório técnico usando EXATAMENTE estas tags:
[RESUMO], [PONTOS_FORTES], [GAPS], [SUGESTOES], [DICAS_OURO], [NOTA].

```

---

### 6. 📂 Estrutura de Pastas
services/: Contém a lógica central da aplicação, como a comunicação com a API do Gemini e o processamento de IA. 🧠

utils/: Reúne funções utilitárias e auxiliares, como formatadores de texto e ferramentas para geração de arquivos PDF. 🛠️

components/: Foca nos elementos da interface visual (UI) do Streamlit, garantindo que o design esteja separado da lógica. 🎨

### 7.🔐 Guia de API Key (Google AI Studio)

A aplicação utiliza o modelo **Gemini 2.0 Flash** e **Gemini 3 Flash (Preview)**. Para obter sua chave gratuita, siga estes passos:

1.  Acesse o [Google AI Studio](https://aistudio.google.com/).

2.  Faça login com sua conta Google.

3.  No menu lateral, clique em **"Get API key"**.

4.  Clique no botão **"Create API key in new project"**.

5.  Copie a chave gerada e cole-a no campo correspondente na barra lateral da aplicação.
Obs: Cuidado com os limites

### 8 Versões utilizadas
<img width="1067" height="162" alt="image" src="https://github.com/user-attachments/assets/5e5334b0-4b91-4801-aedc-b5dd1ce2e509" />



# Resultado

![assistente-cv](https://github.com/user-attachments/assets/f9513fe4-01fd-4f1e-a9d3-472ffad31d7d)


