# CTFTime-Bot-BR
Bot para o Telegram que te atualiza dos ultimos CTFs que vão sair, no horário de Brasilia!

Requisitos:
Ter o Python3 instalado

E instalar as bibliotecas necessarias usando o requirements.txt usando os seguinte comando:
 ```
    pip3 install -r requirements.txt
```

## Atualização 07/02/2019
Agora o bot trabalha na AWS, utilizando Lambda e API Gateway. O Bot se encaixa perfeitamente na Free Tier. O que precisa de ser feito é criar uma váriavel de ambiente com o nome TELEGRAM_TOKEN, com o valor sendo o token do bot do Telegram, e configurar o webhook do bot do Telegram para o API Gateway. Logo após, configurar o API Gateway para ativar uma trigger no Telegram sempre que um post acontecer. Mais tarde vou fazer um video ensinando a criar um bot no Telegram usando API Gateway e Lambda.
