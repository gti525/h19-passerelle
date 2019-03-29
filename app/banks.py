import logging

import requests

from app.consts import BANK2_BASE_URL
from app.utils import genrators
from app.utils.aes import encrypt

logger = logging.getLogger(__name__)

BANK1_ID = 1111
BANK2_ID = 5105
BANKX_ID = 0000

PRE_AUTHORIZE_TRANS_ACTION = "pre_auth"
PROCESS_TRANS_ACTION = "process"


def call_real_bank(bank_id, act=None, **kwargs):
    response = None

    if act == PRE_AUTHORIZE_TRANS_ACTION:

        if bank_id == BANK2_ID:
            response = Bank2.pre_authorize_transaction(**kwargs)
        elif bank_id == BANK1_ID:
            response = Bank1.pre_authorize_transaction(**kwargs)

    elif act == PROCESS_TRANS_ACTION:
        if bank_id == BANK1_ID:
            response = Bank1.process_transaction(**kwargs)

        elif bank_id == BANK2_ID:
            response = Bank2.process_transaction(**kwargs)

    try:
        response.raise_for_status()
        return response.status_code, response.json()[0]

    except requests.HTTPError as e:
        logger.error("HTTPError status-code={}  message={}".format(response.status_code,str(e)))
        return response.status_code, {}
    except Exception as e:
        logger.error("Exception".format(str(e)))
        return response.status_code, {}


def call_fake_bank(act=None, **kwargs):
    code = 200
    resp_data = {}

    try:
        if act == PRE_AUTHORIZE_TRANS_ACTION:
            resp_data["transactionId"] = genrators.random_with_N_digits(12)
        elif act == PROCESS_TRANS_ACTION:
            pass
        return code, resp_data
    except Exception as e :
        logger.error("Exception message={}".format(str(e)))
        return 400, {}


class Bank:
    @staticmethod
    def pre_authorize_transaction(card_holder_name, amount, merchant, card_number, cvv, month_exp, year_exp):
        pass

    @staticmethod
    def process_transaction(bank_transaction_id, action):
        pass


class Bank2(Bank):
    @staticmethod
    def pre_authorize_transaction(card_holder_name, amount, merchant, card_number, cvv, month_exp, year_exp):
        url = BANK2_BASE_URL + "/api/v1/paymentGateway/preAuth"
        headers = {"X-API-KEY": "15489123311"}
        data = {
            "amount": amount,
            "merchantDesc": merchant.name,
            "merchantAccountNumber": merchant.account_number,
            "account": {
                "cardholderName": card_holder_name,
                "number": encrypt(card_number),
                "exp": "{}/{}".format(month_exp, year_exp),
                "cvv": encrypt(cvv)
            }
        }
        r = requests.post(url, headers=headers, data=data)
        return r

    @staticmethod
    def process_transaction(bank_transaction_id, action):
        url = BANK2_BASE_URL + "/api/v1/paymentGateway/process"
        headers = {"X-API-KEY": "15489123311"}
        data = {
            "transactionID": bank_transaction_id,
            "action": action
        }
        r = requests.post(url, headers=headers, data=data)
        return r


class Bank1(Bank):
    # TODO wating for bank1 ...
    pass


def get_bank_id(number):
    bank_id = int(str(number)[:4])
    if bank_id == BANK1_ID:
        return BANK1_ID
    elif bank_id == BANK2_ID:
        return BANK2_ID
    else:
        return BANKX_ID
