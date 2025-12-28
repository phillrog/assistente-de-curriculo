from langchain_google_genai import GoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from utils.logger import BaseLogger

class AssitenteCurriculo:
    def __init__(self, api_key, logger: BaseLogger, temperature=0.1):
        # Armazena o prompt que será acessada pela App
        self.ultimo_prompt_renderizado = ""
        self.logger = logger
        
        self.logger.info("Inicializando motor de IA (Gemini 2.0 Flash)...")
        
        try:
            self.llm = GoogleGenerativeAI(
                model="gemini-2.0-flash",
                google_api_key=api_key,
                temperature=temperature
            )
            
            self.template = """
            SUA MISSÃO: Transformar o currículo de um CANDIDATO desempregado em um documento de ALTO IMPACTO que vença os robôs (ATS) e encante recrutadores humanos.

            VOCÊ É: Um Especialista em Recrutamento Tech e Psicologia de Contratação.
            
            ### REGRAS DE OURO (Siga rigorosamente):
            1. A [NOTA] deve ser baseada ESTREITAMENTE em critérios técnicos (Match de competências). Ela deve ser IDÊNTICA independentemente do tom escolhido (Amigável ou Realista ou Outro).
            2. No campo [DICAS_OURO], use obrigatoriamente '**' para negrito nos títulos e '-' para listas.
            
            ### ESTILO DE RESPOSTA
            {style_choice}

            ### CONTEXTO DE ENTRADA
            Abaixo estão os dados que você deve processar. Considere apenas o conteúdo dentro das tags:
            
            <vaga>
            {job_description}
            </vaga>

            <curriculo>
            {candidate_cv}
            </curriculo>

            <historico_da_conversa>
            {chat_history}
            </historico_da_conversa>

            ### SOLICITAÇÃO ATUAL DO USUÁRIO
            <comando>
            {user_input}
            </comando>

            ---
            DIRETRIZES TÁTICAS PARA O ALTO IMPACTO:
            1. FOCO EM ATS: Identifique as 5 palavras-chave essenciais da vaga que NÃO estão no currículo. Liste-as nas sugestões.
            2. MÉTODO STAR: Escolha a experiência mais relevante do currículo e sugira uma reescrita rápida: (S)ituação, (T)arefa, (A)ção e (R)esultado quantificável.
            3. MITIGAÇÃO DE GAPS: Para cada falha técnica, dê uma "saída estratégica". Como o candidato pode compensar esse gap?
            4. FONTES E LINKS: Sempre que sugerir o estudo de uma tecnologia ou ferramenta (ex: Python, AWS, Scrum), procure fornecer um link de fonte confiável (Documentação oficial, Coursera, Udemy ou Microsoft Learn) para o candidato se aprofundar.

            [RESUMO] -> (Análise direta baseada no TOM: {style_choice})
            [PONTOS_FORTES] -> (Destaque o que torna este candidato ideal)
            [GAPS] -> (O que falta? Seja honesto e dê a saída estratégica)
            [SUGESTOES] -> (Plano de ação: 5 palavras-chave + 1 exemplo STAR)
            [DICAS_OURO] -> (Gere 3 dicas PERSONALIZADAS e acionáveis para quem busca recolocação).
            [NOTA] -> (Número de 0 a 100 baseado em match técnico real)
            
            ---
            REGRA DE ENGAJAMENTO: 
            Sempre termine sua resposta com uma "PERGUNTA DE MENTOR" desafiadora para o usuário. 
            Exemplo: "Quer que eu simule uma pergunta difícil desta vaga para você treinar?" ou 
            "Gostaria que eu escrevesse uma mensagem de abordagem para você enviar ao recrutador no LinkedIn?"
            
            {formato_instrucao}
            """
            
            self.prompt = PromptTemplate.from_template(self.template)
            self.chain = self.prompt | self.llm | StrOutputParser()
            
            self.logger.info("Cadeia de Processamento LangChain configurada.")
        except Exception as e:
            self.logger.error(f"Falha na inicialização do serviço: {str(e)}")
            raise e

    # Adicionado tone_style como argumento
    def chat(self, cv_text, job_text, history, user_input, tone_style):
        try:
            self.logger.info(f"Processando requisição (Estilo: {tone_style})")
            
            if not history:
                self.logger.info("Modo: Geração de Relatório Técnico.")
                # Primeira análise: Exige o relatório completo
                instrucao = """
                ### FORMATO OBRIGATÓRIO DE RESPOSTA:
                Gere o relatório técnico usando EXATAMENTE estas tags:
                [RESUMO], [PONTOS_FORTES], [GAPS], [SUGESTOES], [DICAS_OURO], [NOTA].
                """
            else:
                self.logger.info("Modo: Chat de Mentoria Ativo.")
                # Chat contínuo: Conversa natural como assistente
                instrucao = """
                ### MODO DE CONVERSA ATIVO:
                O relatório já foi entregue. Agora, responda como um mentor de carreira.
                Responda de forma direta, amigável e natural à pergunta do usuário: "{user_input}"
                NÃO use as [RESUMO], [PONTOS_FORTES], [GAPS], [SUGESTOES], [DICAS_OURO], [NOTA]. Mantenha a conversa fluida.".
                """
            
            variaveis = {
                "candidate_cv": cv_text,
                "job_description": job_text,
                "chat_history": history,
                "user_input": user_input,
                "style_choice": tone_style,
                "formato_instrucao": instrucao
            }
            
            self.logger.info("Renderizando prompt completo para o sistema...")
                            
            # Renderiza o prompt original
            prompt_bruto = self.prompt.format(**variaveis)
            
            # Limpa o prompt para o log ficar bonito (remove os espaços à esquerda de cada linha)
            log_formatado = f"--- PROMPT ENVIADO AO GEMINI ---\n{prompt_bruto}"            
            self.ultimo_prompt_renderizado = self._limpar_prompt_para_log(log_formatado)
            
            self.logger.info("Invocando cérebro da IA...")
            resultado = self.chain.invoke(variaveis)
            
            self.logger.info("Resposta recebida com sucesso.")
            return resultado
        except Exception as e:
            msg_erro = f"Erro na execução do chat: {str(e)}"
            self.logger.error(msg_erro)
            return f"Erro técnico: {str(e)}"
        
    def _limpar_prompt_para_log(self, prompt_sujo):
        """
        Remove recuos excessivos de cada linha individualmente,
        mantendo a estrutura mas eliminando os 'tabs' fantasmas.
        """
        # 1. Divide o texto em linhas
        linhas = prompt_sujo.split('\n')
        # 2. Remove espaços em branco do início e fim de cada linha
        linhas_limpas = [linha.strip() for linha in linhas]
        # 3. Junta tudo de novo com quebras de linha
        return "\n".join(linhas_limpas)        