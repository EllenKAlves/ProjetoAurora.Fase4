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
