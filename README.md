# ProjetoAurora.Fase4
> Ellen Kauane Rodrigues Alves - RM570885 | Pietra Fanticelli - RM573229 | Renan Mano Otero - RM554911 | Sarah Iraci Bessa de Moura - RM573889 | 

## Sistema de Monitoramento Operacional

> Sistema em Python projetado para simular o monitoramento, telemetria e tomada de decisão lógica de uma base operacional em Marte.

O projeto analisa dados ambientais e energéticos coletados via sensores, identifica anomalias críticas no ecossistema da missão, prevê tendências de consumo de recursos e gerencia o fluxo de alertas utilizando estruturas de dados clássicas.

---

## 🛠️ Tecnologias e Paradigmas

* **Linguagem:** Python 3.14.3
* **Persistência de Dados:** Manipulação de arquivos flat (`.txt` para logs históricos) e estruturados (`.csv` para telemetria).
* **Estruturas de Dados:** * **Filas (FIFO):** Utilizadas no processamento ordenado de alertas ativos no painel.
  * **Pilhas (LIFO):** Utilizadas para o desempilhamento e registro cronológico invertido de eventos críticos no arquivo de logs.
* **Análise de Dados:** Algoritmo de média móvel integrada com cálculo de taxa de crescimento para previsão de tendência de consumo.

---

## 📂 Estrutura de Arquivos Necessária

Para o correto funcionamento do script, certifique-se de ter um diretório chamado `data/` no mesmo nível do seu arquivo de código, contendo o arquivo de telemetria:

```microstructural
├── data/
│   ├── Dados.csv         # Massa de dados com as leituras dos sensores
│   └── Eventos.txt       # Arquivo com o histórico de logs atualizado a cada execução
├── docs/
|   ├── relatorio.pdf     # Arquivo com relatório explicando: análise, estruturas, lógica, previsão e decisóes técnicas
|   └── link_video.txt    # Arquivo com link do video no YouTube 
└── main.py               # Código-fonte principal do sistema
```

## 🧠 Arquitetura de Funcionalidades

O script é dividido em blocos funcionais isolados que representam o pipeline de processamento de dados do sistema:
1. `ler_historico_eventos()`: Realiza a leitura e exibição no terminal dos logs gravados em execuções passadas no arquivo `Eventos.txt`.
2. `[carregar_dados_do_csv()`: Realiza o parsing do arquivo `.csv`, mapeia a última linha para o estado atual dos dicionários do sistema e popula as matrizes de histórico.
3. `processar_alertas()`: Aplica regras de lógica proposicional sobre as variáveis do habitat. Se houver inconformidades (Ex: $Oxig\hat{e}nio < 85\%$ ou $Bateria < 30\%$), popula simultaneamente a fila de exibição e a pilha de persistência.
4. `prever_tendencia()`: Analisa os últimos estados da série temporal de consumo para calcular o comportamento energético iminente.
5. `registrar_eventos_txt()`: Desempilha os eventos coletados no ciclo atual de processamento e os anexa (`append mode`) ao arquivo `Eventos.txt`.

## 📜 Entrada e saída esperadas

entrada:
> Tempo,Solar,Eolica,Bateria,Oxigenio,Temperatura,Comunicacao,Consumo
> 1,50.0,30.0,85.0,95.0,22.0,1,45.0
> 2,45.0,25.0,70.0,90.0,21.5,1,55.0
> 3,10.0,15.0,25.0,82.0,19.0,0,65.0

saída:

> ## 📜 HISTÓRICO DE EVENTOS ANTERIORES (data/Eventos.txt)
> ------------------------------------------------------------
> NOVA ANÁLISE DE EVENTOS COMPILADA ---
> Status: Todos os módulos operando em conformidade nominal.
> ------------------------------------------------------------
> ============================================================
> ## SISTEMA DE MONITORAMENTO OPERACIONAL     
>
> ## 📋 TABELA DE STATUS DOS MÓDULOS
> Módulo               | Status Operacional | Leitura Atual
> ------------------------------------------------------------
> ENERGIA (solar) : 🟢 OPERACIONAL      | 10.0
> ENERGIA (eolica) : 🟢 OPERACIONAL      | 15.0
> ENERGIA (baterias) : 🟢 OPERACIONAL      | 25.0
> HABITAT (oxigenio) : 🟢 OPERACIONAL      | 82.0
> HABITAT (temperatura) : 🟢 OPERACIONAL      | 19.0
> HABITAT (comunicacao) : 🔴 FALHA CRÍTICA   | 0.0
>
> ## 🚨 ALERTAS ATIVOS (Fila de Atendimento)
> [CRÍTICO] Suporte à Vida: Risco de asfixia ou blecaute iminente.
> [ALERTA] Comunicação: Sinal com a Terra interrompido.
>
> [🔧 RECOMENDAÇÕES TÉCNICAS AUTOMARES]
> ⚠️ [RECOMENDAÇÃO] Previsão de consumo excede a geração renovável.
> 🛠️ [RECOMENDAÇÃO] Módulo de Comunicação Offline.
>
> ============================================================
> 💾 Novos eventos salvos com sucesso em 'data/Eventos.txt'!
