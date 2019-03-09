from pip._vendor import requests

from app.utils.aes import encrypt
from app.consts import BANK2_BASE_URL


def preauthorize_payment(card_holder_name, amount, merchant_name, card_number, cvv, month_exp, year_exp):
    url = BANK2_BASE_URL + "/api/v1/paymentGateway/preAuth"
    headers = {"X-API-KEY": "15489123311"}
    data = {
        "amount": amount,
        "merchantDesc": merchant_name,
        "merchantAccountNumber": merchant_name,
        "account": {
            "cardholderName": card_holder_name,
            "number": encrypt(card_number),
            "exp": "{}/{}".format(month_exp, year_exp),
            "cvv": encrypt(cvv)
        }
    }
    r = requests.post(url, headers=headers, data=data)

    return r


def processPaymentWithBank2(bank_transaction_id, action):
    pass


def fundTransfer(account1, account2):
    pass
