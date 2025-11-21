from paho.mqtt import client, publish
from paho.mqtt.enums import CallbackAPIVersion
import time
import random

data = {
    'host_mqtt': 'localhost',
    'user_mqtt': {
        'username': 'grupo7',
        'password': 'meca37'
    },
    'notion_token': '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',
    'topics': {
        'meca3_2025/sensores/temperatura1': {
            'url_link': 'https://www.notion.so/Temperatura-1-2ac4ad00b97280b6b5f0ec774fcb6cff?source=copy_link',
            'prop': 'Valor'
        },
        'meca3_2025/sensores/temperatura2': {
            'url_link': 'https://www.notion.so/Temperatura-2-2ac4ad00b97280e388dcdaab9014e5ff?source=copy_link',
            'prop': 'Valor'
        },
        'meca3_2025/sensores/nivel': {
            'url_link': 'https://www.notion.so/N-vel-de-gua-2ac4ad00b9728046b3daefc5a18701f8?source=copy_link',
            'prop': 'Valor'
        },
        'meca3_2025/sensores/vazao': {
            'url_link': 'https://www.notion.so/Vaz-o-2ac4ad00b97280d3bba6f8c51900db56?source=copy_link',
            'prop': 'Valor'
        },
        'meca3_2025/atuadores/aquecedor': {
            'url_link': 'https://www.notion.so/Aquecedor-2ac4ad00b9728082b50bf9ef616e9880?source=copy_link',
            'prop': 'Status'
        },
        'meca3_2025/atuadores/motor': {
            'url_link': 'https://www.notion.so/Motor-2ac4ad00b97280ecbb42f0629770ca50?source=copy_link',
            'prop': 'Status'
        },
        'meca3_2025/atuadores/valvula': {
            'url_link': 'https://www.notion.so/V-lvula-2ac4ad00b97280cdb6dbcd8391196561?source=copy_link',
            'prop': 'Status'
        }
    },
    'dashboard': {} #key: topic, value: numeric
}

topics = [*data['topics']]
topic_data = dict()
for topic in topics:
    if 'temperatura' in topic:
        topic_data[topic] = [0.5 * t for t in range(30, 51)]
    elif 'nivel' in topic:
        topic_data[topic] = [d for d in range(5, 41)]
    elif 'vazao' in topic:
        topic_data[topic] = [0.05 * v for v in range(1, 10)]
    elif 'aquecedor' in topic:
        topic_data[topic] = [0, 1]
    elif 'motor' in topic:
        topic_data[topic] = [0, 1]
    elif 'valvula' in topic:
        topic_data[topic] = [0, 1]


mqtt_client = client.Client(callback_api_version=CallbackAPIVersion.VERSION2)
mqtt_client.username_pw_set(username=data['user_mqtt']['username'], password=data['user_mqtt']['password'])
mqtt_client.connect(host=data['host_mqtt'], port=1883)

old_topic = ''

while True:
    pub_dict = {}
    pub_list = []
    for i in range(1, 4):
        topic = random.choice(topics)
        if topic != old_topic:
            payload = random.choice(topic_data[topic])
            pub_dict[f'{topic}'] = payload
            old_topic = topic
    
    for k in pub_dict:
        publish.single(topic=k, payload=pub_dict[k], keepalive=0)
        print(f'published {payload} in {topic}')

    time.sleep(1)