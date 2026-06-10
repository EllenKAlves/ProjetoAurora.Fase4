# Projeto Aurora - Sistema de Monitoramento Operacional

**Integrantes:** Ellen Kauane Rodrigues Alves - RM570885 | Kaua Arthur - RM573734 | Pietra Fanticelli - RM573229 | Renan Mano Otero - RM554911 | Sarah Iraci Bessa de Moura - RM573889

## Resumo do problema

O Projeto Aurora simula o monitoramento de uma base operacional em Marte. O sistema le dados de telemetria, acompanha seis modulos criticos, identifica riscos ambientais e energeticos, gera alertas automaticos e recomenda acoes para proteger a tripulacao e os equipamentos.

Os dados incluem uma crise proposital as `20:00` e uma inconsistencia as `23:00`. O programa percorre todos os horarios para que esses eventos nao sejam ignorados.

## Estrutura do repositorio

```text
ProjetoAurora.Fase4/
|-- README.md
|-- data/
|   |-- Dados.csv
|   `-- Eventos.txt
|-- docs/
|   |-- link_video.txt
|   |-- relatorio.pdf
|   `-- uso_ia.md
`-- src/
    `-- sistema.py
```

## Dados analisados

- Estados binarios `0/1` de suporte a vida, energia, comunicacao, habitat, laboratorio e armazenamento.
- Geracao, consumo e reserva de energia em sete horarios.
- Temperatura interna, radiacao e qualidade da comunicacao.
- Log com eventos simulados da missao.
- Inconsistencia proposital: todos os modulos ativos com geracao e consumo zerados as `23:00`.

## Estruturas de dados utilizadas

- **Lista:** armazena a sequencia de leituras, a fila de alertas e a pilha de eventos criticos.
- **Fila de prioridade:** apresenta primeiro os alertas criticos e depois os alertas operacionais.
- **Pilha:** guarda eventos criticos e os apresenta do mais recente para o mais antigo.
- **Dicionario:** representa cada leitura e permite acessar rapidamente os valores pelo nome.
- **Dicionario aninhado:** organiza a hierarquia da missao em energia, habitat e pesquisa/logistica.
- **Matriz:** representa sete horarios por sete campos principais de telemetria.

## Regras logicas principais

O sistema utiliza `IF`, `ELIF`, `ELSE`, `AND`, `OR` e `NOT`. As principais regras sao:

1. Falha em suporte a vida ou habitat gera estado critico.
2. Consumo maior que geracao gera alerta; com reserva baixa, torna-se critico.
3. Comunicacao offline ou qualidade abaixo de 50% gera estado critico.
4. Radiacao igual ou superior a 7, ou temperatura fora da faixa segura, gera estado critico.
5. Modulos ativos com geracao e consumo zerados geram alerta de inconsistencia.

Expressao booleana principal:

```text
CRITICO =
    (NOT suporte_vida OR NOT habitat)
    OR (consumo > geracao AND reserva < 60)
    OR (NOT comunicacao OR qualidade_comunicacao < 50)
    OR (radiacao >= 7 OR temperatura < 16 OR temperatura > 30)
    OR (todos_modulos_ativos AND geracao == 0 AND consumo == 0)
```

Cada regra gera uma recomendacao relacionada ao risco detectado. Por exemplo, falha de comunicacao recomenda reiniciar o modulo e ativar o canal de emergencia.

## Tecnica de previsao

Foi utilizada a **media das tres ultimas variacoes da reserva energetica**, sem bibliotecas avancadas.

```text
Reservas: [85, 80, 78, 82, 74, 65, 60]
Tres ultimas variacoes: [-8, -9, -5]
Media das variacoes: -7,33 pontos percentuais
Previsao do proximo ciclo: 60 - 7,33 = 52,67%
```

Como a previsao fica abaixo de 60%, o sistema recomenda reduzir cargas nao essenciais no proximo ciclo.

## Como executar

Na raiz do projeto, utilize Python 3:

```bash
python src/sistema.py
```

O programa utiliza somente a biblioteca padrao do Python.

## Exemplo de entrada

Trecho de `data/Dados.csv`:

```csv
20:00,1,1,0,1,1,1,30,65,65,22,7,45
23:00,1,1,1,1,1,1,0,0,60,22,3,95
```

## Exemplo de saida

```text
20:00      | CRITICO  | 3
23:00      | CRITICO  | 1

[CRITICO] 20:00 | Comunicacao: Comunicacao offline ou qualidade abaixo de 50%.
[CRITICO] 20:00 | Ambiente: Radiacao critica ou temperatura fora da faixa segura.
[CRITICO] 23:00 | Diagnostico de dados: Todos os modulos estao ativos, mas geracao e consumo sao zero.

Reserva prevista para o proximo ciclo: 52.67%
Classificacao da previsao: ALERTA
```

## Recomendacoes geradas

- Ativar modo de economia quando houver risco energetico.
- Priorizar suporte a vida e sistemas essenciais.
- Reiniciar a comunicacao e ativar o canal de emergencia.
- Recolher a equipe ao habitat protegido em caso de radiacao critica.
- Validar sensores quando os dados forem inconsistentes.
- Reduzir cargas nao essenciais quando a previsao da reserva estiver abaixo de 60%.

## Video demonstrativo

O link sera inserido em `docs/link_video.txt` depois da gravacao do video.

## Conclusoes e aprendizados

O projeto demonstra como estruturas fundamentais do Python podem transformar telemetria em decisoes justificadas. A equipe aplicou listas, filas, pilhas, dicionarios, matrizes, condicionais e uma previsao simples. O principal aprendizado foi que um sistema de monitoramento precisa analisar todo o historico e tambem validar se os dados recebidos sao coerentes antes de recomendar uma acao.
