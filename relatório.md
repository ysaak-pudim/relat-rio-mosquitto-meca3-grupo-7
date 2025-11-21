### Parte inicial
A partir do site https://mosquitto.org/download/ tentamos instalar a versão mais recente do Mosquitto.
No entanto, aparecia um erro ao completar a instalação que apontava para a inexistência de um arquivo `.dll`.

Para contornar esse erro, recorremos ao link https://mosquitto.org/files/binary/ disponibilizado pelo próprio site que continha as versões compatíveis com as configurações da máquina utilizada (Windows 7 32-bit).
A instalação foi concluída com êxito, e pudemos fazer todo o restante do procedimento.

### Configurando o Mosquitto
Para a configuração, primeiramente copiamos o arquivo `mosquitto.conf` do diretório '*C:\Program Files\mosquitto*' para um caminho não gerenciado pelo sistema.
Depois, abrimos a cópia usando o Bloco de Notas do Windows substituímos seu conteúdo por todo o código a seguir:
```conf
# Permite conexões de qualquer lugar na rede (0.0.0.0)
listener 1883 0.0.0.0

# ===== SEGURANÇA =====
# Impede que dispositivos se conectem sem usuário e senha
#allow_anonymous false
allow_anonymous true #test

# Caminho para o arquivo que guardará os usuários e senhas
password_file C:\Program Files\mosquitto\passwd

# Definir o arquivo de log
log_dest file C:\Program Files\mosquitto\mosquitto.log

# Definir os tipos de log
log_type error
log_type warning
log_type information
log_type debug  # Se quiser incluir logs de debug

# Outras configurações que você pode querer incluir no arquivo de configuração
# defina a porta, persistência, etc.

# Habilitar persistência de tópicos e mensagens
persistence true
persistence_location C:\Program Files\mosquitto\data
```
Depois foi só mover a cópia para a pasta do Mosquitto.

Após esse evento, precisamos aprender um pouco sobre os comandos do Mosquitto no Prompt de Comando para terminar a primeira configuração.

Como o Windows não identificou os programas `mosquitto`, `mosquitto_pub`, `mosquitto_sub` e todos os outros restantes como variáveis de ambiente (para operar no ambiente Windows), tivemos que ir no Menu Iniciar e pesquisar por 'Propriedades do Sistema'. Em tal janela, clicamos em 'Avançado > Variáveis de Ambiente...' e adicionamos o caminho '*C:\Program Files\mosquitto*' como sendo uma fonte extra de variáveis (que abriga os comandos que queremos) para executarmos a missão.

Terminando isso, prosseguimos para o terminal (mas dessa vez aberto novamente para carregar as alterações). Todas as linhas abaixo foram inseridas uma por vez no cmd:
```bash
mosquitto -c "C:\Program Files\mosquitto\mosquitto.conf"

net stop mosquitto

net start mosquitto

mosquitto_passwd -c passwd grupo1

meca31

mosquitto_passwd grupo2

meca32

mosquitto_passwd grupo3

meca33

mosquitto_passwd grupo4

meca34

mosquitto_passwd grupo5

meca35

mosquitto_passwd grupo6

meca36

mosquitto_passwd grupo7

meca37

mosquitto_passwd grupo8

meca38

mosquitto_passwd grupo9

meca39
```
Resumidamente, garantimos que o mosquito fosse executado no terminal considerando o arquivo padrão de configuração `mosquitto.conf`, reiniciamos o Mosquitto, definimos `passwd` como sendo o arquivo com os usuários e suas respectivas senhas e inserimos todas as credenciais dos grupos.

Também nos certificamos de que os arquivos `mosquitto.log`, `passwd` e `data` existiam no caminho '*C:\Program Files\mosquitto*', e fizemos as devidas alterações na pasta.
Após tudo isso, fomos capazes de finalizar toda a configuração do nosso Broker MQTT.

### Testes e Resultados
Após finalmente termos concluído os passos cruciais, temos aqui o primeiro teste, que foi efetuado para verificar a integridade do Mosquitto:

<img src="registros/WhatsApp Image 2025-11-12 at 10.48.54.jpeg">

Traduzindo o que está acontecendo acima, abrimos dois termiais como administrador e usamos o primeiro para a função `mosquitto_pub` e o segundo para a função `mosquitto_sub`:
- **`mosquitto_pub`**: publica no host local (na própria máquina que está rodando o broker) no tópico '*teste/tópico*' as mensagens de teste 'Olá, Mosquitto!' e 'fechar registro'.
- **`mosquitto_sub`**: verifica no tópico em questão do host local se há alguma mensagem publicada. Caso isso ocorra, tal mensagem é exibida no terminal.

E assim terminamos as partes fundamentais para que o projeto se mantesse de pé. Agora basta o usuário se conectar ao endereço IPv4 da máquina (que é facilmente encontrado nas configurações de rede) com suas credenciais.

### Observações
- O arquivo que registra os *logs*, `mosquitto.log`, permaneceu vazio o tempo todo, e não conseguimos encontrar a solução para este problema. Tivemos a suspeita de que, pela versão instalada do Mosquitto ser de 2014, alguns componentes podem estar faltando ou simplesmente não se tinha naquela época.

### Extras
Como não ficamos satisfeitos por já ter concluído o papel atribuído ao nosso grupo, quisemos ir além: tivemos a ideia de criar um dashboard para dar um aroma mais elegante para o Mosquitto. Sabemos que a elaboração de tal dashboard não era obrigação da nossa parte, mas não ligamos pra isso e botamos a mão na massa.

O programa que utilizamos como cobaia para essa ideia maluca foi o [Notion](https://www.notion.com/pt), pois continha as principais ferramentas que precisávamos: bases de dados, exibição em gráficos, propriedades, valores etc.

Criamos dois scripts em Python para executar nossa brincadeira:
- `mqtt_pub.py`: este publica os dados dos sensores e motores em seus respectivos tópicos. Nesse caso, tivemos que forçar uma "leitura", utilizando uma biblioteca que gera números pseudoaleatórios.
- `notion_mqtt_sync.py`: esse arquivo foi divertido de se fazer. Cada alteração nova no valor de um tópico é registrada e inserida na página estruturada do Notion por meio da [API oficial do Notion](https://developers.notion.com/), que é nativamente em Javascript, mas a biblioteca [notion-client](https://pypi.org/project/notion-client/) resolveu nosso problema.

Como esses scripts ainda estavam em fase de teste, deixaremos de lado os registros mais detalhados, mas segue abaixo um vídeo do dashboard funcionando:

[2025-11-21 20-50-45.mkv](registros/2025-11-21%2020-50-45.mkv)

Resumidamente foi esse o nosso relatório.