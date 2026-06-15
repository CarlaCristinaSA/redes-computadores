# Passo a passo completo — TP01 TCP/Wireshark

## 1. Preparar as 2 máquinas

Descubra o IP de cada uma:
- Linux/Mac: `ip addr` ou `ifconfig`
- Windows: `ipconfig`

Anote: IP_SERVIDOR e IP_CLIENTE. Teste com `ping IP_SERVIDOR` do lado cliente.

Confirme que ambas têm Python 3 e Wireshark instalados.

## 2. Ajustar o código

No `echo_client.py`, troque a linha:
```python
SERVER_HOST = '192.168.1.10'
```
pelo IP real da máquina servidor (ex: `192.168.50.10`).

O `echo_server.py` não precisa de alteração (já escuta em `0.0.0.0:12345`).

## 3. Configurar firewall (se necessário)

- Linux: `sudo ufw allow 12345/tcp`
- Windows: permitir Python no firewall quando solicitado

## 4. Abrir Wireshark e configurar filtro de captura (ANTES de executar)

Em **ambas** as máquinas:

1. Abra o Wireshark, **não inicie a captura ainda**.
2. No campo "Enter a capture filter" (acima da lista de interfaces), digite:
   ```
   tcp port 12345
   ```
3. Selecione a interface correta (a que está na mesma rede da outra máquina).
4. Clique em **Start (▶)** para iniciar a captura nas duas máquinas.

## 5. Executar a aplicação

**Na máquina servidor**, terminal:
```bash
python3 echo_server.py
```

**Na máquina cliente**, terminal:
```bash
python3 echo_client.py
```

Digite 2 ou 3 caracteres (ex: "a", "b") e depois `#` para encerrar.

## 6. Parar a captura

Após o `#`, pare a captura (■) nas duas máquinas.

## 7. Analisar o handshake no Wireshark

Localize os 3 primeiros pacotes da conversa:

| # | Pacote | Flags | Seq | Ack |
|---|---|---|---|---|
| 1 | Cliente → Servidor | SYN | Seq=0 (relativo) | — |
| 2 | Servidor → Cliente | SYN, ACK | Seq=0 | Ack=1 |
| 3 | Cliente → Servidor | ACK | Seq=1 | Ack=1 |

Para destacar só esses pacotes, use filtro de exibição (depois de capturar):
```
tcp.flags.syn==1 || (tcp port 12345 && tcp.len==0)
```
ou simplesmente role até os 3 primeiros pacotes — eles aparecem no topo.

Opcional: também mostre 1 pacote de dados (quando você digitou o primeiro caractere) — verá `Seq` aumentar em 1 e `Ack` confirmar +1.

## 8. Roteiro do vídeo (até 5 min)

| Tempo | O que falar/mostrar |
|---|---|
| 0:00–0:30 | Nomes da equipe, disciplina, objetivo |
| 0:30–1:15 | Mostrar as 2 máquinas, IPs, e os arquivos echo_server.py / echo_client.py |
| 1:15–2:00 | Mostrar o filtro de captura `tcp port 12345` configurado nas duas máquinas |
| 2:00–2:30 | Rodar servidor, depois cliente, trocar 1-2 caracteres + `#` |
| 2:30–4:00 | Parar captura, analisar os 3 pacotes do handshake lado a lado (flags SYN/SYN-ACK/ACK, Seq/Ack) |
| 4:00–4:45 | Explicar a relação Ack = Seq+1, ISN, e mostrar 1 pacote de dados |
| 4:45–5:00 | Conclusão |

## 9. Explicação teórica (para falar no vídeo)

- **Pacote 1 (SYN)**: cliente escolhe um número de sequência inicial aleatório (ISN) `x`. Não há dados, mas o SYN consome 1 número de sequência.
- **Pacote 2 (SYN-ACK)**: servidor escolhe seu próprio ISN `y`, e confirma o cliente com `Ack = x+1` ("recebi até x, espero x+1 a seguir").
- **Pacote 3 (ACK)**: cliente confirma com `Seq = x+1` e `Ack = y+1`.
- Depois disso a conexão está **estabelecida** e os dados (caracteres do eco) começam a fluir.
- No Wireshark, "Relative Sequence Numbers" está ativado por padrão, então você verá `Seq=0`/`Seq=1` em vez dos valores absolutos — explique que são relativos ao ISN real escolhido pelo SO.

## 10. Checklist final

- [ ] Ping funciona entre as máquinas
- [ ] `SERVER_HOST` correto no cliente
- [ ] Filtro `tcp port 12345` configurado ANTES de iniciar captura, nas duas máquinas
- [ ] Captura iniciada ANTES de rodar o cliente
- [ ] 1-2 caracteres + `#` trocados
- [ ] 3 pacotes do handshake visíveis e identificados
- [ ] Vídeo ≤5min, YouTube não listado
- [ ] Link enviado via Telegram com nomes da equipe (prazo: 16/06/2026)