# ProjetoAurora.Fase4
> Ellen Kauane Rodrigues Alves - RM570885 | Kaua Arthur - RM573734 | Pietra Fanticelli - RM573229 | Renan Mano Otero - RM554911 | Sarah Iraci Bessa de Moura - RM573889 | 

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

O script é dividido em blocos funcionais isolados que representam o pipeline de processamento e monitoramento telemetria do sistema:

1. `ler_historico_eventos()`: Realiza a leitura e exibição no terminal dos logs gravados em execuções passadas no arquivo `Eventos.txt`.
2. `carregar_dados_do_csv()`: Realiza o parsing cirúrgico do arquivo `.csv`, mapeia a última linha capturada para o estado atual dos dicionários do sistema (segmentados em energia, suporte de habitat e pesquisa/logística) e popula as matrizes de histórico. Mapeia e valida dados críticos como consumo_kwh, geracao_kwh, radiacao, temp_interna, laboratorio e armazenamento.
3. `processar_alertas()`: Aplica regras de lógica proposicional sobre as variáveis do habitat e infraestrutura de energia. Se houver inconformidades (Ex: colapso no suporte à vida/oxigênio ou $Bateria < 30\%$ em modo offline/falha geral de geração), popula simultaneamente a fila de exibição e a pilha de persistência.
4. `prever_tendencia()`: Analisa os últimos estados da série temporal de consumo energético baseado na coluna consumo_kwh para calcular e prever analiticamente o comportamento energético iminente.
5. `registrar_eventos_txt()`: Desempilha de forma segura os eventos coletados no ciclo atual de processamento e os anexa (`append mode`) ao arquivo histórico `Eventos.txt`.

## 📜 Entrada e saída esperadas

entrada:
---
<img width="868" height="107" alt="image" src="https://github.com/user-attachments/assets/7f83ec8d-1761-4686-a361-6f142740461c" />

saída:
---
<img width="506" height="609" alt="image" src="https://github.com/user-attachments/assets/8197c06c-bcb9-499a-8bad-de01485a6395" />

