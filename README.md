# Relatório Mosquitto Meca3

**Grupo**: Grupo 7 - Mosquitto

**Alunos**: Erick Riquelme, Ysaak Costa

### Resumo
Todas as nossas anotações estão dispostas no arquivo [`relatório.md`](relatório.md). Os registros foram deixados na pasta [`registros/`](registros/) e o código fonte em Python do nosso programa que usa a API do Notion, [`notion_mqtt_sync.py`](mosquitto_python_and_notion/notion_mqtt_sync.py), para se conectar a um dashboard remoto e atualizar os dados continuamente está na pasta [`mosquitto_python_and_notion`](mosquitto_python_and_notion/), bem como o [`mqtt_pub.py`](mosquitto_python_and_notion/mqtt_pub.py), que simula uma leitura de dados e publica em cada tópico presente abaixo com seus respectivos valores:
```txt
meca3_2025/sensores/temperatura1
meca3_2025/sensores/temperatura2
meca3_2025/sensores/nivel
meca3_2025/sensores/vazao
meca3_2025/atuadores/aquecedor
meca3_2025/atuadores/motor
meca3_2025/atuadores/valvula
```
Tais tópicos foram organizados na seguinte estrutura hierárquica:
```
meca3_2025/
├── sensores/
│       ├── temperatura1
│       ├── temperatura2
│       ├── nivel
│       └── vazao
└── atuadores/
          ├── aquecedor
          ├── motor
          └── valvula
```

De fato tem sido um ótimo aprendizado para nós, componentes do grupo responsável pela parte do Broker MQTT, pois os desafios que encontramos nos fizeram aprender coisas novas e de grande utilidade para nosso futuro.