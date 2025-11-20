import numbers
import threading, time
from paho.mqtt import client, subscribe
import notion_client
from paho.mqtt.enums import CallbackAPIVersion

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

range_value_dict = {
    'meca3_2025/sensores/temperatura1': 0.1,
    'meca3_2025/sensores/temperatura2': 0.1,
    'meca3_2025/sensores/nivel': 0.25,
    'meca3_2025/sensores/vazao': 0.001
}

# It is always necessary to specify the API version (VERSION2 or newer)
mqtt_client = client.Client(callback_api_version=CallbackAPIVersion.VERSION2)
# Setting the credentials to doing the connection sucessfully
mqtt_client.username_pw_set(username=data['user_mqtt']['username'], password=data['user_mqtt']['password'])
mqtt_client.connect(host=data['host_mqtt'], port=1883)

# Connecting to the Notion API
notion = notion_client.Client(auth=data['notion_token'])

def update_dashboard(page_id, prop: str, value):
    '''
    This function makes updates in our dashboard.
    page_id: 16 characters id of the page. It can be obtained using 'notion_client.extract_page_id' function.
    prop: the property that must be modified.
    value: value to be applied to property.
    '''
    keys = {
        '1': 'Ativo',
        '0': 'Inativo'
    }

    if prop == 'Valor':
        value = {'number': float(value)}
    
    elif prop == 'Status':
        value = {'status': {'name': keys[f'{value}']}}
    
    notion.pages.update(
        page_id,
        properties={
            prop: value
        }
    )

def update_db_thread():
    '''
    This function updates automatically without sync with 'on_message' events
    '''
    old_dict = {}
    while True:
        temporary_dict = dict(data['dashboard'])
        # Skip to the next loop step if 'temporary_dict' is empty
        if not temporary_dict:
            time.sleep(0.1)
            continue

        for topic in temporary_dict:
            page_id = notion_client.extract_page_id(data['topics'][topic]['url_link'])
            prop = data['topics'][topic]['prop']
            value = temporary_dict[topic]

            # Goes out of the 'for' loop if 'old_dict' is empty, because next steps don't match
            if not old_dict:
                break

            # Skip to the next 'for' loop step if the current topic isn't in 'old_dict', until this condition is true
            if not (topic in old_dict):
                continue
                
            if (prop == 'Status') and (temporary_dict[topic] != old_dict[topic]):
                update_dashboard(page_id, prop, value)
                print(f'new value in {topic}: {value}')
            
            elif (prop == 'Valor'):
                if abs(temporary_dict[topic] - old_dict[topic]) >= range_value_dict[topic]:
                    update_dashboard(page_id, prop, value)
                    print(f'new value in {topic}: {value}')
                else:
                    print(f'{value} was not published in {topic}.')
                    # The line below is important because an value increment inside the range defined at 'range_value_dict[topic]'
                    # would goes unnoticed by the code without that line
                    temporary_dict[topic] = old_dict[topic]
            
            else:
                print(f'{value} was not published in {topic}.')
        
        time.sleep(0.1)
            
        old_dict = dict(temporary_dict)

# It calls 'update_dashboard' function
def on_message(client, userdata, message):
    topic: str = message.topic
    value: str = message.payload.decode()

    if (topic in data['topics']) and value.isnumeric():
        data['dashboard'][topic] = float(value) if 'sensores' in topic else int(value)

# 't' will run in paralel with the rest of the code
t = threading.Thread(target=update_db_thread)
t.start()

# It always calls the function 'on_message' whenever something is published on the defined topics.
subscribe.callback(
    callback=on_message,
    topics=[*data['topics']],
    hostname=data['host_mqtt']
)
