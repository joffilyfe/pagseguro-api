# -*- coding: utf-8 -*-
import requests
import xmltodict


class SandBoxConfig(object):
    '''A SandBox Config for PagSeguro Instance'''

    def __init__(self):
        self.payment_url = 'https://sandbox.pagseguro.uol.com.br/v2/checkout/payment.html?code=%s'
        self.notification_url = 'https://ws.sandbox.pagseguro.uol.com.br/v3/transactions/notifications/%s/'
        self.checkout_url = 'https://ws.sandbox.pagseguro.uol.com.br/v2/checkout/'
        self.headers = {
            'Content-Type': 'application/x-www-form-urlencoded; charset=ISO-8859-1'}


class PagSeguroConfig(object):
    '''A Config for PagSeguro Instance'''

    def __init__(self):
        self.payment_url = 'https://pagseguro.uol.com.br/v2/checkout/payment.html?code=%s'
        self.notification_url = 'https://ws.pagseguro.uol.com.br/v3/transactions/notifications/%s/'
        self.checkout_url = 'https://ws.pagseguro.uol.com.br/v2/checkout/'
        self.headers = {
            'Content-Type': 'application/x-www-form-urlencoded; charset=ISO-8859-1'}


class PagSeguroCheckOutResponse(object):
    '''Parser Checkout Response from XML to DICT'''

    def __init__(self, xml, config=None):
        self.xml = xml
        self.code = None
        self.errors = None
        self.payment_url = None
        self.config = config
        self.parse_xml(xml)

    def __str__(self):
        return 'code: %s\nurl: %s' % (self.code, self.payment_url)

    def parse_xml(self, xml):
        try:
            parsed = xmltodict.parse(xml, encoding='iso-8859-1')
        except Exception as e:
            self.errors = {'errors': e}
            return

        if 'errors' in parsed:
            self.errors = parsed['errors']['error']
            return 

        if not 'checkout' in parsed:
            self.errors = {'errors': 'Houve um problema para capturar informações'}
            return

        checkout = parsed.get('checkout')
        self.code = checkout.get('code')
        self.payment_url = self.config.payment_url % self.code


class PagSeguroNotificationResponse(object):
    def __init__(self, xml, config=None):
        self.config = config
        self.xml = xml
        self.errors = None
        self.transaction = None
        self.items = None
        self.parse_xml(xml)

    def parse_xml(self, xml):
        try:
            parsed = xmltodict.parse(xml, encoding='iso-8859-1')
        except Exception as e:
            self.errors = {'errors': e}
            return

        if 'errors' in parsed:
            self.errors = parsed['errors']['error']
            return

        if 'transaction' in parsed:
            self.transaction = parsed.get('transaction')

        if 'items' in self.transaction:
            self.items = self.transaction.get('items')


class PagSeguro(object):
    ''' PagSeguro API'''

    def __init__(self, token=None, email=None, config=None):
        if config is None:
            self.config = PagSeguroConfig()
        else:
            self.config = config
        self.token = token
        self.email = email
        self.items = []
        self.params = None
        self.notification_url = None
        self.reference = None

    def post(self, url):
        """ do a post request """
        return requests.post(url, data=self.params,
                             headers=self.config.headers)

    def get(self, url):
        """ do a get transaction """
        return requests.get(url, params=self.params,
                            headers=self.config.headers)

    def add_item(self, itemid=None, desc=None, price=None, weigth=100, quantity=1):
        '''Add item to order'''

        if not price:
            return {'errors': 'Por favor, informe o valor do objeto'}

        item = {}
        item['id'] = itemid
        item['desc'] = desc
        item['amount'] = price
        item['weight'] = weigth
        item['quantity'] = quantity

        try:
            self.items.append(item)
        except Exception as e:
            return e

    def build_checkout_params(self):
        '''Build Params for requests urls'''

        params = {}
        params['email'] = self.email
        params['token'] = self.token
        params['currency'] = 'BRL'

        if self.notification_url:
            params['notificationURL'] = self.notification_url

        if self.reference:
            params['reference'] = self.reference
        else:
            params['reference'] = 'Ref'


        for i, item in enumerate(self.items):
            i = i + 1
            params['itemId%s' % i] = item.get('id')
            params['itemDescription%s' % i] = item.get('desc')
            params['itemAmount%s' % i] = item.get('amount')
            params['itemQuantity%s' % i] = item.get('quantity')
            params['itemWeight%s' % i] = item.get('weight')
            params['itemShippingCost%s' % i] = '0.00'

        self.params = params

    def build_notification_params(self):
        params = {}
        params['email'] = self.email
        params['token'] = self.token
        self.params = params

    def clean_cart(self):
        items = []

    def checkout(self):
        '''Send itens to API and return a response'''

        if len(self.items) == 0:
            return {'errors': 'Por favor, adicione itens ao pedido'}

        self.build_checkout_params()
        self.clean_cart()
        response = self.post(self.config.checkout_url)

        return PagSeguroCheckOutResponse(response.content, config=self.config)

    def check_notification(self, code):
        self.build_notification_params()
        response = self.get(self.config.notification_url % code)

        return PagSeguroNotificationResponse(response.content, config=self.config)

