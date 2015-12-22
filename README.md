#PagSeguro Python API
É um simples módulo para criar transações e receber o status de notificação.

##Inicializando a API com SandBox

Caso você esteja trabalhando em ambiente de produção, não é necessário instanciar a configuração

```
from pagseguro import PagSeguro, SandBoxConfig
config = SandBoxConfig()
pagseguro = PagSeguro(token='seu-token',
                      email='seu@email.com', config=config)
```

##Adicionando itens a ordem

Antes de tentarmos fazer o checkout da ordem, é necessário adicionar items.

```
pagseguro.add_item(10201, 'O nome do item', price='100.00')
pagseguro.add_item(10202, 'O nome do item', price='200.00')
```

##Configurações adicionais

Podemos adicionar algumas configurações ao nosso checkout, como referencia e url de notificação.

```
pagseguro.reference = 'Referencia da ordem'
pagseguro.notification_url = 'http://url-de-retorno.com'
```

##Fazendo o checkout da ordem

A partir do momento que adicionamos os itens e configuramos nossa ordem, é possível solicitar o checkout. Como resposta obteremos um objeto com atributos de código e url de pagamento.

```
response = pagseguro.checkout()
response.code # Código para processar a ordem
response.payment_url # URL montada para pagamento da ordem
```

## Obtendo a resposta de uma notificação

Quando o PagSeguro obtem uma atualizando de status de uma ordem, ele fará um post na URL de notificação previamente configurada. Podemos utilizar isso para obter novas informações sobre a ordem específica.

```
code = request.POST['notificationCode']
response = pagseguro.check_notification(code)

print(response.transaction.get('code'))
print(response.transaction.get('status'))
print(response.transaction.get('reference'))
```


##Quer ajudar?
Manda um pull request.

### Créditos
Esse módulo foi escrito por Joffily Ferreira, inspirando pelo módulo do Bruno [Link](https://github.com/rochacbruno/python-pagseguro)



