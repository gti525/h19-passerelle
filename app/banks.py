import logging
import json as jjson
import requests

from app.consts import *
from app.utils import genrators
from app.utils.aes import encrypt

logger = logging.getLogger(__name__)

BANK1_ID = 1111
BANK2_ID = 5105
BANKX_ID = 0000

PRE_AUTHORIZE_TRANS_ACTION = "PRE_AUTH_ACTION"
PROCESS_TRANS_ACTION = "PROCESS_ACTION"


def call_real_bank(bank_id, act=None, **kwargs):
    response = None
    logger.info("ACTION = {} to BANK = {}".format(act,bank_id))

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
        results = response.json()
        parsed_res = jjson.loads(jjson.dumps(results))
        logger.info("Response data: {}".format(jjson.dumps(parsed_res, indent=4, sort_keys=True)))

        if COMMITTED in results.values() or ACCEPTED in results.values():
            return response.status_code, results

    except requests.HTTPError as e:
        logger.error("HTTPError status-code={}  message={}".format(response.status_code, str(e)))
        return response.status_code, {}
    except Exception as e:
        logger.error("Exception: {}".format(str(e)))
        return response.status_code, {}

    return 400, {}


def call_fake_bank(act=None, **kwargs):
    code = 200
    resp_data = {}

    try:
        if act == PRE_AUTHORIZE_TRANS_ACTION:
            resp_data["transactionId"] = genrators.random_with_N_digits(12)
        elif act == PROCESS_TRANS_ACTION:
            pass
        return code, resp_data
    except Exception as e:
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
            "merchantAccountNumber": int(merchant.account_number),
            "account": {
                "cardholderName": card_holder_name,
                "number": encrypt(card_number),
                "exp": "{}/{}".format(month_exp, year_exp),
                "cvv": encrypt(cvv)
            }
        }
        r = requests.post(url, headers=headers, json=data)
        log_data(r, data)

        return r

    @staticmethod
    def process_transaction(bank_transaction_id, action):
        url = BANK2_BASE_URL + "/api/v1/paymentGateway/process"
        headers = {"X-API-KEY": "15489123311"}
        data = {
            "transactionID": bank_transaction_id,
            "action": action
        }
        r = requests.post(url, headers=headers, json=data)
        log_data(r, data)

        return r


class Bank1(Bank):
    @staticmethod
    def pre_authorize_transaction(card_holder_name, amount, merchant, card_number, cvv, month_exp, year_exp):
        url = BANK1_BASE_URL + "/api/paymentgateway/preauth"
        descBank1 = ''
        if amount >= 0:
            descBank1 = 'Achat chez ' + merchant.name
        else:
            descBank1 = 'Remboursement en provenance de ' + merchant.name
        cHolderNames = card_holder_name.split()
        headers = {"apikey": "FyufTW2r!"}
        data = {
            "merchantAccountNo": str(merchant.account_number),
            "firstName": cHolderNames[0],
            "lastName": cHolderNames[1],
            "ccNumber": str(card_number),
            "cvv": int(cvv),
            "expiryDate": "{}/{}".format(month_exp, year_exp),
            "amount": str(amount),
            "transactionDesc": descBank1
        }
        r = requests.post(url, headers=headers, json=data)
        log_data(r, data)
        return r

    @staticmethod
    def process_transaction(bank_transaction_id, action):
        url = BANK1_BASE_URL + "/api/paymentgateway/process"

        headers = {"apikey": "FyufTW2r!"}
        data = {
            "transactionId": bank_transaction_id,
            "action": action,
        }
        r = requests.post(url, headers=headers, json=data)
        log_data(r, data)

        return r


def get_bank_id(number):
    bank_id = int(str(number)[:4])
    if bank_id == BANK1_ID:
        return BANK1_ID
    elif bank_id == BANK2_ID:
        return BANK2_ID
    else:
        return BANKX_ID


def log_data(response, data):
    #   parsed_headers = jjson.loads(jjson.dumps(dict(response.headers)))
    parsed_data = jjson.loads(jjson.dumps(data))
    #    logger.info("Headers: {}".format(jjson.dumps(parsed_headers, indent=4, sort_keys=True)))
    logger.info("Data: {}".format(jjson.dumps(parsed_data, indent=4, sort_keys=True)))
