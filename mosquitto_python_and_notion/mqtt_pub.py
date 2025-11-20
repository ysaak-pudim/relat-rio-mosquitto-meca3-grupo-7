from paho.mqtt import client, publish
from data import data
from paho.mqtt.enums import CallbackAPIVersion
import time
import random
import threading

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

while True:
    pub_dict = {}
    pub_list = []
    for i in range(1, 4):
        topic = random.choice(topics)
        payload = random.choice(topic_data[topic])
        pub_dict[f'{topic}'] = payload
    
    for k in pub_dict:
        pub_list.append((k, pub_dict[k]))

    publish.multiple(pub_list)

    for (topic, payload) in pub_list:
        print(f'published {payload} in {topic}')
    
    time.sleep(1)