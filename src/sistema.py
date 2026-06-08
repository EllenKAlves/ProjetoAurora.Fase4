import csv

#  FUNÇÃO PARA LER O HISTÓRICO DE LOGS ANTERIORES (data/Eventos.txt)
def ler_historico_eventos():
    """Lê e exibe no terminal os eventos que já foram gravados anteriormente"""
    print("\n[📜 HISTÓRICO DE EVENTOS ANTERIORES (data/Eventos.txt)]")
    print("-" * 60)
    try:
        with open('data/Eventos.txt', mode='r', encoding='utf-8') as arquivo_txt:
            conteudo = arquivo_txt.read()
            if not conteudo.strip():
                print("O arquivo de logs está vazio.")
            else:
                print(conteudo.strip())
    except FileNotFoundError:
        print("ℹ️ Nenhum histórico encontrado. O arquivo 'Eventos.txt' será criado nesta execução.")
    print("-" * 60)

#  FUNÇÃO PARA LER OS DADOS ATUAIS DA MISSÃO (data/Dados.csv)
def carregar_dados_do_csv():
    dados_missao = {}
    historico_consumo = []
    matriz_leituras = []

    try:
        with open('data/Dados.csv', mode='r', encoding='utf-8') as arquivo:
            leitor_csv = csv.reader(arquivo)
            next(leitor_csv) # Pula a linha de cabeçalho
            
            linhas = list(leitor_csv)
            if not linhas:
                print("⚠️ Arquivo 'Dados.csv' está vazio.")
                return None, [], []
                
            ultima_leitura = linhas[-1]
            
            dados_missao = {
                "energia": {
                    "solar": {"status": 1, "valor_atual": float(ultima_leitura[1])},
                    "eolica": {"status": 1, "valor_atual": float(ultima_leitura[2])},
                    "baterias": {"status": 1, "valor_atual": float(ultima_leitura[3])}
                },
                "habitat": {
                    "oxigenio": {"status": 1, "valor_atual": float(ultima_leitura[4])},
                    "temperatura": {"status": 1, "valor_atual": float(ultima_leitura[5])},
                    "comunicacao": {"status": int(ultima_leitura[6]), "valor_atual": float(ultima_leitura[6])}
                }
            }
            
            for linha in linhas:
                matriz_leituras.append([linha[0], float(linha[1]), float(linha[2]), float(linha[4])])
                historico_consumo.append(float(linha[7]))
                
        return dados_missao, historico_consumo, matriz_leituras

    except FileNotFoundError:
        print("❌ Erro: O arquivo 'data/Dados.csv' não foi encontrado.")
        return None, [], []

#  SISTEMA DE DECISÃO LOGICA (Filas e Pilhas)
def processar_alertas(dados_missao):
    fila_alertas = []  
    pilha_eventos = [] 
    
    bateria = dados_missao["energia"]["baterias"]["valor_atual"]
    oxigenio = dados_missao["habitat"]["oxigenio"]["valor_atual"]
    comunicacao_ok = bool(dados_missao["habitat"]["comunicacao"]["status"])
    solar_ok = bool(dados_missao["energia"]["solar"]["status"])
    
    if (oxigenio < 85.0) or (bateria < 30.0 and not solar_ok):
        alerta = {"nivel": "CRÍTICO", "modulo": "Suporte à Vida", "motivo": "Risco de asfixia ou blecaute iminente."}
        fila_alertas.append(alerta)
        pilha_eventos.append(alerta)
        
    if not comunicacao_ok:
        alerta = {"nivel": "ALERTA", "modulo": "Comunicação", "motivo": "Sinal com a Terra interrompido."}
        fila_alertas.append(alerta)
        pilha_eventos.append(alerta)
        
    return fila_alertas, pilha_eventos

#  GRAVAÇÃO DE NOVOS LOGS (data/Eventos.txt)
def registrar_eventos_txt(pilha_eventos):
    """Desempilha os novos eventos e os adiciona ao arquivo histórico"""
    try:
        with open('data/Eventos.txt', mode='a', encoding='utf-8') as arquivo_txt:
            arquivo_txt.write("--- NOVA ANÁLISE DE EVENTOS COMPILADA ---\n")
            if not pilha_eventos:
                arquivo_txt.write("Status: Todos os módulos operando em conformidade nominal.\n")
            else:
                while pilha_eventos:
                    evento = pilha_eventos.pop()
                    arquivo_txt.write(f"[{evento['nivel']}] Módulo: {evento['modulo']} | Motivo: {evento['motivo']}\n")
            arquivo_txt.write("\n")
        print("💾 Novos eventos salvos com sucesso em 'data/Eventos.txt'!")
    except Exception as e:
        print(f"❌ Falha ao gravar arquivo de logs: {e}")

#  TÉCNICA SIMPLES DE PREVISÃO
def prever_tendencia(historico_consumo):
    if len(historico_consumo) < 2:
        return 0.0
    ultimos_dados = historico_consumo[-3:]
    media_movel = sum(ultimos_dados) / len(ultimos_dados)
    taxa_crescimento = historico_consumo[-1] - historico_consumo[-2]
    return media_movel + taxa_crescimento

#  EXECUÇÃO PRINCIPAL
def executar_sistema():
    # NOVIDADE: Lê e mostra o passado antes de analisar o presente
    ler_historico_eventos()

    # Carregamento do arquivo atual
    dados_missao, historico_consumo, matriz_leituras = carregar_dados_do_csv()
    if not dados_missao:
        return
        
    fila_alertas, pilha_eventos = processar_alertas(dados_missao)
    proximo_consumo = prever_tendencia(historico_consumo)
    
    geracao_total = dados_missao["energia"]["solar"]["valor_atual"] + dados_missao["energia"]["eolica"]["valor_atual"]
    bateria_atual = dados_missao["energia"]["baterias"]["valor_atual"]
    
    # Exibição do Painel
    print("="*60)
    print("         SISTEMA DE MONITORAMENTO OPERACIONAL - MARS v2        ")
    print("="*60)
    
    print("\n[📋 TABELA DE STATUS DOS MÓDULOS]")
    print(f"{'Módulo':<20} | {'Status Operacional':<18} | {'Leitura Atual'}")
    print("-" * 60)
    for sistema, sub in dados_missao.items():
        for sub_nome, info in sub.items():
            status_text = "🟢 OPERACIONAL" if info["status"] == 1 else "🔴 FALHA CRÍTICA"
            print(f"{sistema.upper()} ({sub_nome}) : {status_text:<18} | {info['valor_atual']}")
            
    print("\n[🚨 ALERTAS ATIVOS (Fila de Atendimento)]")
    if not fila_alertas:
        print("🟢 Sistema seguro. Sem alertas pendentes.")
    else:
        for alt in fila_alertas:
            print(f"[{alt['nivel']}] {alt['modulo']}: {alt['motivo']}")

    print("\n[🔧 RECOMENDAÇÕES TÉCNICAS AUTOMARES]")
    if proximo_consumo > geracao_total and bateria_atual < 60.0:
        print("⚠️ [RECOMENDAÇÃO] Previsão de consumo excede a geração renovável.")
    if dados_missao["habitat"]["comunicacao"]["status"] == 0:
        print("🛠️ [RECOMENDAÇÃO] Módulo de Comunicação Offline.")

    print("\n" + "="*60)
    
    # Salva os novos dados gerados nesta rodada
    registrar_eventos_txt(pilha_eventos)

if __name__ == "__main__":
    executar_sistema()