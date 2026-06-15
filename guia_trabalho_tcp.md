# Guia de Execução — TP01: Análise de Conexões TCP com Wireshark

Este guia complementa o enunciado do trabalho e cobre, passo a passo:
1. Como montar o ambiente de laboratório com duas máquinas;
2. Como executar o servidor e o cliente de eco fornecidos;
3. Como configurar o filtro de captura no Wireshark;
4. A teoria do *three-way handshake* com exemplo numérico, para usar na explicação do vídeo;
5. Um roteiro sugerido para o vídeo de até 5 minutos.

---

## 1. Montando o ambiente de laboratório

Vocês precisam de **duas máquinas** capazes de se comunicar por TCP/IP, cada uma rodando o **Wireshark** (para capturar "dos dois lados" da conexão).

### Opção A — Duas máquinas virtuais (mais simples de controlar)

1. Instale o **VirtualBox** (ou VMware) e crie duas VMs (ex.: duas instalações leves de Ubuntu/Debian, que já vêm com Python 3).
2. Em cada VM, configure o **Adaptador de Rede** como **"Rede Interna" (Internal Network)** ou **"Adaptador Host-Only"**, usando o mesmo nome de rede nas duas VMs (ex.: `intnet`). Isso cria uma rede privada só entre as duas VMs, isolando o tráfego de outros ruídos.
3. Dentro de cada VM, defina um IP fixo na mesma sub-rede, por exemplo:
   - VM Servidor: `192.168.50.10/24`
   - VM Cliente: `192.168.50.11/24`
   - No Linux: `sudo ip addr add 192.168.50.10/24 dev enp0s3` (ajuste o nome da interface).
4. Teste a conectividade com `ping 192.168.50.10` (do cliente para o servidor).
5. Instale o Wireshark nas duas VMs: `sudo apt install wireshark` e permita captura sem root (`sudo usermod -aG wireshark $USER`, depois reabra a sessão).

### Opção B — Dois computadores físicos na mesma rede local

1. Conecte ambos à mesma rede Wi-Fi/cabeada.
2. Descubra o IP de cada máquina:
   - Linux/Mac: `ip addr` ou `ifconfig`
   - Windows: `ipconfig`
3. Verifique se o firewall não está bloqueando a porta escolhida (12345 no código fornecido). Em redes domésticas, geralmente é só permitir o Python no firewall do Windows ou usar `sudo ufw allow 12345/tcp` no Linux.
4. Instale o Wireshark nas duas máquinas.

> **Dica:** a opção A (rede interna no VirtualBox) é mais recomendada porque reduz drasticamente o tráfego "estranho" capturado (broadcasts, mDNS, etc.), facilitando a leitura do PCAP mesmo sem o filtro.

---

## 2. Executando a aplicação de eco

Os arquivos `echo_server.py` e `echo_client.py` já implementam o comportamento exigido pelo enunciado (cliente envia 1 caractere, servidor exibe e ecoa, cliente exibe o eco, repetindo até o caractere `#`).

1. **Na máquina servidor**, copie `echo_server.py` e execute:
   ```bash
   python3 echo_server.py
   ```
   Ele vai escutar em todas as interfaces, na porta `12345`.

2. **Na máquina cliente**, copie `echo_client.py` e **edite a variável `SERVER_HOST`** no topo do arquivo, colocando o IP real da máquina servidor (ex.: `192.168.50.10`).

3. **Antes de conectar**, inicie a captura no Wireshark em **ambas** as máquinas (veja seção 3).

4. Execute o cliente:
   ```bash
   python3 echo_client.py
   ```

5. Digite alguns caracteres e observe o eco. Para terminar, digite `#`.

Você pode trocar a porta `12345` por outra de sua preferência — basta alterar `PORT` nos dois arquivos (servidor e cliente) para o **mesmo valor**.

---

## 3. Configurando o filtro de captura no Wireshark

O enunciado exige um **filtro de captura** (não apenas um filtro de exibição), restringindo a captura apenas aos pacotes da conexão da aplicação.

Passo a passo:

1. Abra o Wireshark **antes** de executar o cliente.
2. Na tela inicial, **não clique duas vezes na interface ainda**. Em vez disso:
   - Clique no ícone de engrenagem ⚙️ ao lado da interface correta (a que está na mesma rede da outra máquina), **ou**
   - Digite o filtro no campo **"Enter a capture filter…"** acima da lista de interfaces.
3. Use um filtro de captura no formato BPF (Berkeley Packet Filter), por exemplo:

   - Na **máquina servidor** (IP do cliente = 192.168.50.11):
     ```
     host 192.168.50.11 and tcp port 12345
     ```
   - Na **máquina cliente** (IP do servidor = 192.168.50.10):
     ```
     host 192.168.50.10 and tcp port 12345
     ```

   Se preferir um filtro mais simples (válido para ambas as máquinas, já que só essa aplicação usa a porta 12345):
   ```
   tcp port 12345
   ```

4. Selecione a interface correta e clique em **Start** (▶) para iniciar a captura.
5. Execute o cliente e troque algumas mensagens.
6. Pare a captura (■) após enviar o caractere `#`.

> **Atenção:** filtro de *captura* (definido antes de iniciar) é diferente do filtro de *exibição* (digitado na barra superior do Wireshark depois de capturar, com sintaxe `ip.addr == ... && tcp.port == ...`). O enunciado pede o filtro de **captura**, mas vocês também podem usar um filtro de exibição adicional no vídeo para destacar só os 3 pacotes do handshake (`tcp.flags.syn==1 || (tcp.flags.syn==1 && tcp.flags.ack==1)` ou simplesmente procurar os 3 primeiros pacotes da conversa).

---

## 4. Teoria: o Three-Way Handshake e os campos Seq/Ack

Esta seção é o conteúdo que vocês devem **explicar verbalmente no vídeo**, relacionando com os números reais observados na captura.

### 4.1 Os três segmentos

Antes de qualquer dado ser trocado, o cliente e o servidor TCP executam o *three-way handshake*:

1. **SYN** (cliente → servidor): o cliente envia um segmento com a flag `SYN = 1` e um **número de sequência inicial (ISN)** escolhido aleatoriamente, digamos `Seq = x`. Esse segmento não carrega dados de aplicação, mas o próprio SYN "consome" um número de sequência.

2. **SYN, ACK** (servidor → cliente): o servidor responde com `SYN = 1` e `ACK = 1`. Ele escolhe seu próprio número de sequência inicial `Seq = y`, e confirma o recebimento do SYN do cliente colocando `Ack = x + 1` (ou seja, "recebi até o byte x, espero o próximo a partir de x+1").

3. **ACK** (cliente → servidor): o cliente confirma o SYN-ACK do servidor enviando `ACK = 1`, com `Seq = x + 1` (porque seu próprio SYN consumiu o número x) e `Ack = y + 1` (confirmando o SYN do servidor).

Após esse terceiro segmento, a conexão está **estabelecida** e os dados de aplicação (no caso, os caracteres do eco) podem ser trocados.

### 4.2 Exemplo numérico (ilustrativo)

Suponha que, na captura, o Wireshark mostre (valores absolutos — sem a opção "Relative Sequence Numbers", que é o padrão e mais fácil de explicar):

| # | Segmento | Origem → Destino | Seq | Ack | Flags |
|---|---|---|---|---|---|
| 1 | SYN | Cliente → Servidor | 1000 | — | SYN |
| 2 | SYN-ACK | Servidor → Cliente | 5000 | 1001 | SYN, ACK |
| 3 | ACK | Cliente → Servidor | 1001 | 5001 | ACK |

Observem o padrão: **Ack = Seq recebido + 1**. Isso vale especificamente para os segmentos SYN/SYN-ACK porque, mesmo sem dados, eles ocupam 1 número de sequência (é uma convenção do protocolo, assim como o FIN também consome 1 número).

> **Dica para o vídeo:** o Wireshark, por padrão, ativa "Relative Sequence Numbers", mostrando `Seq=0` e `Seq=1` (relativos ao início da conexão) em vez dos valores absolutos. Vocês podem manter assim (é mais didático) — só expliquem que esses são valores *relativos* ao ISN de cada lado, e que na prática o sistema operacional escolhe um ISN aleatório por questões de segurança.

### 4.3 Depois do handshake — pacotes de dados

Quando o cliente envia o primeiro caractere (1 byte), o segmento de dados terá `Seq = x+1` (o mesmo valor usado no ACK do handshake) e, ao confirmá-lo, o servidor responderá com `Ack = x+2` (porque 1 byte foi recebido). Esse é exatamente o conceito de **número de sequência = posição do primeiro byte de dados no fluxo**, e **número de reconhecimento = próximo byte esperado**. Mostrar esse comportamento nos primeiros pacotes de dados (após o handshake) é uma ótima forma de reforçar, na prática, o que foi visto em aula.

---

## 5. Roteiro sugerido para o vídeo (até 5 minutos)

| Tempo | Conteúdo |
|---|---|
| 0:00–0:30 | Identificação da equipe (nomes), disciplina e objetivo do trabalho |
| 0:30–1:15 | Mostrar rapidamente a topologia: as duas máquinas/VMs, seus IPs, e os arquivos `echo_server.py` / `echo_client.py` |
| 1:15–2:00 | Mostrar o filtro de captura configurado no Wireshark em cada máquina antes de iniciar a captura |
| 2:00–2:30 | Executar o servidor e depois o cliente, trocar 1–2 caracteres |
| 2:30–4:00 | Parar a captura e analisar, lado a lado (servidor e cliente), os **3 pacotes do handshake**: apontar as flags SYN/SYN-ACK/ACK e os campos Seq/Ack de cada um |
| 4:00–4:45 | Relacionar os valores observados com a teoria (Ack = Seq+1, ISN, etc.) e, se der tempo, mostrar 1 pacote de dados após o handshake |
| 4:45–5:00 | Encerramento/conclusão |

---

## 6. Checklist final antes de gravar

- [ ] As duas máquinas conseguem se comunicar (teste com `ping`).
- [ ] `SERVER_HOST` no `echo_client.py` aponta para o IP correto do servidor.
- [ ] Wireshark instalado e com permissão de captura nas duas máquinas.
- [ ] Filtro de captura configurado **antes** de iniciar a captura, nas duas máquinas.
- [ ] Captura iniciada **antes** de executar o cliente (para não perder o handshake).
- [ ] Pelo menos 1–2 caracteres trocados, depois `#` para encerrar.
- [ ] Os 3 pacotes do handshake aparecem claramente na lista capturada.
- [ ] Vídeo gravado, com no máximo 5 minutos, e enviado ao YouTube como **não listado**.
- [ ] Link enviado via Telegram com o nome dos integrantes.
