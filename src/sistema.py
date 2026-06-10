import csv


CAMINHO_DADOS = "data/Dados.csv"
CAMINHO_EVENTOS = "data/Eventos.txt"

PRIORIDADE = {"NORMAL": 0, "ALERTA": 1, "CRITICO": 2}

MODULOS = {
    "suporte_vida": "Suporte a vida",
    "energia": "Energia",
    "comunicacao": "Comunicacao",
    "habitat": "Habitat",
    "laboratorio": "Laboratorio",
    "armazenamento": "Armazenamento",
}


def ler_historico_eventos():
    """Le o log simulado sem alterar seu conteudo."""
    print("\n[HISTORICO DE EVENTOS SIMULADOS]")
    print("-" * 74)
    try:
        with open(CAMINHO_EVENTOS, mode="r", encoding="utf-8") as arquivo:
            eventos = [linha.strip() for linha in arquivo if linha.strip()]
            for evento in eventos:
                print(evento)
            return eventos
    except FileNotFoundError:
        print(f"Arquivo nao encontrado: {CAMINHO_EVENTOS}")
        return []


def carregar_dados_do_csv():
    """Carrega a telemetria em uma lista de dicionarios e em uma matriz."""
    leituras = []
    matriz_leituras = []

    try:
        with open(CAMINHO_DADOS, mode="r", encoding="utf-8", newline="") as arquivo:
            leitor = csv.DictReader(arquivo)

            for linha in leitor:
                leitura = {"horario": linha["horario"]}

                for modulo in MODULOS:
                    leitura[modulo] = int(linha[modulo])

                for variavel in (
                    "geracao_kwh",
                    "consumo_kwh",
                    "reserva_energia",
                    "temp_interna",
                    "radiacao",
                    "qualidade_comunicacao",
                ):
                    leitura[variavel] = float(linha[variavel])

                leituras.append(leitura)
                matriz_leituras.append(
                    [
                        leitura["horario"],
                        leitura["geracao_kwh"],
                        leitura["consumo_kwh"],
                        leitura["reserva_energia"],
                        leitura["temp_interna"],
                        leitura["radiacao"],
                        leitura["qualidade_comunicacao"],
                    ]
                )

        return leituras, matriz_leituras
    except FileNotFoundError:
        print(f"Erro: o arquivo {CAMINHO_DADOS} nao foi encontrado.")
        return [], []


def organizar_hierarquia(leitura):
    """Organiza a ultima leitura em uma hierarquia de dicionarios."""
    return {
        "energia": {
            "modulo_ativo": leitura["energia"],
            "geracao_kwh": leitura["geracao_kwh"],
            "consumo_kwh": leitura["consumo_kwh"],
            "reserva_percentual": leitura["reserva_energia"],
        },
        "habitat": {
            "modulo_ativo": leitura["habitat"],
            "suporte_vida_ativo": leitura["suporte_vida"],
            "temperatura_c": leitura["temp_interna"],
            "radiacao": leitura["radiacao"],
            "comunicacao": {
                "modulo_ativo": leitura["comunicacao"],
                "qualidade_percentual": leitura["qualidade_comunicacao"],
            },
        },
        "pesquisa_logistica": {
            "laboratorio_ativo": leitura["laboratorio"],
            "armazenamento_ativo": leitura["armazenamento"],
        },
    }


def criar_alerta(horario, nivel, modulo, motivo, recomendacao):
    """Cria um alerta padronizado para a fila e para a pilha."""
    return {
        "horario": horario,
        "nivel": nivel,
        "modulo": modulo,
        "motivo": motivo,
        "recomendacao": recomendacao,
    }


def analisar_leitura(leitura):
    """Aplica regras logicas a uma leitura de telemetria."""
    alertas = []
    horario = leitura["horario"]

    # Regra 1: falhas binarias dos modulos essenciais e nao essenciais.
    if not leitura["suporte_vida"] or not leitura["habitat"]:
        alertas.append(
            criar_alerta(
                horario,
                "CRITICO",
                "Suporte a vida",
                "Suporte a vida ou habitat indisponivel.",
                "Priorizar suporte a vida e iniciar protocolo de emergencia.",
            )
        )
    elif not leitura["energia"]:
        alertas.append(
            criar_alerta(
                horario,
                "CRITICO",
                "Energia",
                "Modulo principal de energia indisponivel.",
                "Ativar fontes de reserva e desligar sistemas nao essenciais.",
            )
        )
    elif not leitura["laboratorio"] or not leitura["armazenamento"]:
        alertas.append(
            criar_alerta(
                horario,
                "ALERTA",
                "Pesquisa e logistica",
                "Laboratorio ou armazenamento indisponivel.",
                "Verificar o modulo afetado sem interromper sistemas essenciais.",
            )
        )

    # Regra 2: equilibrio entre geracao, consumo e reserva.
    if leitura["reserva_energia"] < 30 or (
        leitura["consumo_kwh"] > leitura["geracao_kwh"]
        and leitura["reserva_energia"] < 60
    ):
        alertas.append(
            criar_alerta(
                horario,
                "CRITICO",
                "Energia",
                "Reserva critica ou deficit energetico com pouca reserva.",
                "Ativar modo de economia e priorizar sistemas essenciais.",
            )
        )
    elif leitura["consumo_kwh"] > leitura["geracao_kwh"]:
        alertas.append(
            criar_alerta(
                horario,
                "ALERTA",
                "Energia",
                "Consumo maior que a geracao disponivel.",
                "Reduzir cargas nao essenciais e acompanhar a reserva.",
            )
        )

    # Regra 3: comunicacao considera o estado binario e a qualidade do sinal.
    if not leitura["comunicacao"] or leitura["qualidade_comunicacao"] < 50:
        alertas.append(
            criar_alerta(
                horario,
                "CRITICO",
                "Comunicacao",
                "Comunicacao offline ou qualidade abaixo de 50%.",
                "Reiniciar o modulo e ativar o canal de emergencia.",
            )
        )
    elif leitura["qualidade_comunicacao"] < 75:
        alertas.append(
            criar_alerta(
                horario,
                "ALERTA",
                "Comunicacao",
                "Qualidade da comunicacao abaixo de 75%.",
                "Reposicionar a antena e monitorar a estabilidade do sinal.",
            )
        )

    # Regra 4: faixas de seguranca ambientais.
    if (
        leitura["radiacao"] >= 7
        or leitura["temp_interna"] < 16
        or leitura["temp_interna"] > 30
    ):
        alertas.append(
            criar_alerta(
                horario,
                "CRITICO",
                "Ambiente",
                "Radiacao critica ou temperatura fora da faixa segura.",
                "Recolher a equipe ao habitat protegido e verificar o controle termico.",
            )
        )
    elif (
        leitura["radiacao"] >= 5
        or leitura["temp_interna"] < 18
        or leitura["temp_interna"] > 27
    ):
        alertas.append(
            criar_alerta(
                horario,
                "ALERTA",
                "Ambiente",
                "Variavel ambiental proxima do limite de seguranca.",
                "Intensificar o monitoramento ambiental.",
            )
        )

    # Regra 5: inconsistencia proposital dos dados.
    modulos_ativos = all(leitura[modulo] == 1 for modulo in MODULOS)
    if (
        modulos_ativos
        and leitura["geracao_kwh"] == 0
        and leitura["consumo_kwh"] == 0
    ):
        alertas.append(
            criar_alerta(
                horario,
                "CRITICO",
                "Diagnostico de dados",
                "Todos os modulos estao ativos, mas geracao e consumo sao zero.",
                "Validar os sensores de energia antes de tomar decisoes operacionais.",
            )
        )

    return alertas


def prever_reserva(leituras):
    """Preve a reserva do proximo ciclo pela media das 3 ultimas variacoes."""
    reservas = [leitura["reserva_energia"] for leitura in leituras]

    if len(reservas) < 4:
        return None

    variacoes = []
    for indice in range(1, len(reservas)):
        variacoes.append(reservas[indice] - reservas[indice - 1])

    ultimas_variacoes = variacoes[-3:]
    media_variacoes = sum(ultimas_variacoes) / len(ultimas_variacoes)
    reserva_prevista = reservas[-1] + media_variacoes
    reserva_prevista = max(0.0, min(100.0, reserva_prevista))

    if reserva_prevista < 30:
        nivel = "CRITICO"
        recomendacao = "Ativar imediatamente o modo de economia de energia."
    elif reserva_prevista < 60:
        nivel = "ALERTA"
        recomendacao = "Reduzir cargas nao essenciais no proximo ciclo."
    else:
        nivel = "NORMAL"
        recomendacao = "Manter o acompanhamento da reserva energetica."

    return {
        "reservas": reservas,
        "ultimas_variacoes": ultimas_variacoes,
        "media_variacoes": media_variacoes,
        "reserva_prevista": reserva_prevista,
        "nivel": nivel,
        "recomendacao": recomendacao,
    }


def classificar_horario(alertas):
    """Classifica um horario como NORMAL, ALERTA ou CRITICO."""
    if any(alerta["nivel"] == "CRITICO" for alerta in alertas):
        return "CRITICO"
    elif any(alerta["nivel"] == "ALERTA" for alerta in alertas):
        return "ALERTA"
    else:
        return "NORMAL"


def processar_alertas(leituras):
    """Percorre todos os horarios e monta fila priorizada e pilha critica."""
    fila_alertas = []
    pilha_eventos_criticos = []
    diagnosticos = []

    for leitura in leituras:
        alertas_horario = analisar_leitura(leitura)
        diagnosticos.append(
            {
                "horario": leitura["horario"],
                "status": classificar_horario(alertas_horario),
                "quantidade_alertas": len(alertas_horario),
            }
        )

        for alerta in alertas_horario:
            fila_alertas.append(alerta)
            if alerta["nivel"] == "CRITICO":
                pilha_eventos_criticos.append(alerta)

    # A lista funciona como fila de prioridade: criticos aparecem primeiro.
    fila_alertas.sort(key=lambda alerta: PRIORIDADE[alerta["nivel"]], reverse=True)
    return fila_alertas, pilha_eventos_criticos, diagnosticos


def exibir_status_modulos(ultima_leitura):
    print("\n[STATUS BINARIO DOS MODULOS NO ULTIMO HORARIO]")
    print(f"{'Modulo':<24} | {'Valor':<5} | Status")
    print("-" * 52)

    for chave, nome in MODULOS.items():
        valor = ultima_leitura[chave]
        status = "NORMAL" if valor == 1 else "CRITICO"
        print(f"{nome:<24} | {valor:<5} | {status}")


def exibir_resultados(leituras, matriz_leituras):
    fila_alertas, pilha_eventos_criticos, diagnosticos = processar_alertas(leituras)
    previsao = prever_reserva(leituras)
    hierarquia = organizar_hierarquia(leituras[-1])

    print("\n" + "=" * 74)
    print("SISTEMA DE MONITORAMENTO OPERACIONAL - PROJETO AURORA")
    print("=" * 74)

    print("\n[STATUS DA MISSAO POR HORARIO]")
    print(f"{'Horario':<10} | {'Status':<8} | Alertas detectados")
    print("-" * 48)
    for diagnostico in diagnosticos:
        print(
            f"{diagnostico['horario']:<10} | "
            f"{diagnostico['status']:<8} | "
            f"{diagnostico['quantidade_alertas']}"
        )

    exibir_status_modulos(leituras[-1])

    print("\n[ALERTAS PRIORIZADOS - FILA]")
    for alerta in fila_alertas:
        print(
            f"[{alerta['nivel']}] {alerta['horario']} | "
            f"{alerta['modulo']}: {alerta['motivo']}"
        )

    print("\n[ULTIMOS EVENTOS CRITICOS - PILHA]")
    for alerta in reversed(pilha_eventos_criticos):
        print(f"{alerta['horario']} | {alerta['modulo']}: {alerta['motivo']}")

    print("\n[PREVISAO DA RESERVA ENERGETICA]")
    print(f"Reservas utilizadas: {previsao['reservas']}")
    print(f"Ultimas variacoes: {previsao['ultimas_variacoes']}")
    print(f"Media das variacoes: {previsao['media_variacoes']:.2f} pontos percentuais")
    print(f"Reserva prevista para o proximo ciclo: {previsao['reserva_prevista']:.2f}%")
    print(f"Classificacao da previsao: {previsao['nivel']}")

    print("\n[RECOMENDACOES TECNICAS AUTOMATICAS]")
    recomendacoes = []
    for alerta in fila_alertas:
        if alerta["recomendacao"] not in recomendacoes:
            recomendacoes.append(alerta["recomendacao"])
    if previsao["recomendacao"] not in recomendacoes:
        recomendacoes.append(previsao["recomendacao"])
    for indice, recomendacao in enumerate(recomendacoes, start=1):
        print(f"{indice}. {recomendacao}")

    print("\n[ESTRUTURAS ORGANIZADAS]")
    print(f"Matriz de leituras: {len(matriz_leituras)} linhas x {len(matriz_leituras[0])} colunas")
    print(f"Grupos da hierarquia: {list(hierarquia.keys())}")
    print("=" * 74)


def executar_sistema():
    ler_historico_eventos()
    leituras, matriz_leituras = carregar_dados_do_csv()

    if not leituras:
        return

    exibir_resultados(leituras, matriz_leituras)


if __name__ == "__main__":
    executar_sistema()
