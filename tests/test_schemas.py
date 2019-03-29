import pytest

from app.schemas import *


@pytest.fixture
def valid_merchant():
    return  {
            "name": "Elvis",
            "id": 1,
        }

@pytest.fixture
def valid_credit_card():
   return {
        "first_name": "Sylvain",
        "last_name": "Degue",
        "number": 1111222233334444,
        "cvv": 856,
        "exp": "12/2019",
    }

class TestDateSchema(object):

    @pytest.mark.parametrize("month,year", [
        (10,2020),
        (10,2024),

    ], ids=["T1", "T2"])
    def test_valid_credit_card(self, month, year):
        data = {
            "month": month,
            "year": year,

        }
        assert DateSchema().validate(data=data) == {}

class TestCreditCardSchema(object):

    @pytest.mark.parametrize("first_name,last_name, number, cvv, exp", [
        ("John", "Doe", 1111222233334444, "123", {"month": 12, "year": 2024}),
        ("John", "Doe", 1111222233334444, "856", {"month": 10, "year": 2024}),
    ], ids=["T1", "T2"])
    def test_valid_credit_card(self, first_name, last_name, number, cvv, exp):
        data = {
            "first_name": first_name,
            "last_name": last_name,
            "number": number,
            "cvv": cvv,
            "exp": exp,
        }
        assert CreditCardSchema().validate(data=data) == {}

    @pytest.mark.parametrize("first_name,last_name, number, cvv, exp", [
        ("John", "Doe", None, 123, "12/2024"),
        ("John", "Doe", 1111222233334444, "456", "1219"),
        (None, "Doe", 1111222233334444, "678", {"month": 12, "year": 2024}),
        ("John", None, 1111222233334444, "912", {"month": 12, "year": 20249}),
        ("John", "Doe", 3569380356438091, "321", {"month": 12, "year": 2024}),
    ], ids=["T1", "T2", "T3", "T4", "T5"])
    def test_invalid_credit_card(self, first_name, last_name, number, cvv, exp):
        data = {
            "first_name": first_name,
            "last_name": last_name,
            "number": number,
            "cvv": cvv,
            "exp": exp,
        }
        assert CreditCardSchema().validate(data=data) != {}


class TestMerchantSchema(object):

    @pytest.mark.parametrize("name,id", [
        ("H&M", 123),
        ("Simons", 12),
        ("BestBuy", 0),
    ], ids=["T1", "T2","T3"])
    def test_invalid_merchant(self, name, id):
        data = {
            "name": name,
            "id": id,
        }
        assert MerchantSchema().validate(data=data) != {}


    @pytest.mark.parametrize("name,id", [
            (342343, "ID"),
            ("Simons", 12),
            (None, "IDS"),
        ], ids=["T1", "T2","T3"])
    def test_invalid_merchant(self, name, id):
        data = {
            "name": name,
            "id": id,
        }
        assert MerchantSchema().validate(data=data) != {}


class TestTransactionSchema(object):

    @pytest.mark.parametrize("amount,purchase_desc",[
        (500.00, "De la drogue")
    ],ids=[])
    def test_valid_transaction(self,amount,purchase_desc):
        data = {
            MERCHANT_API_KEY: "sdfsadgsadgas",
            "amount": amount,
            "purchase_desc": purchase_desc,
            "merchant": {"name": "Elvis", "id": "fhvg"},
            "credit_card":{
                "first_name": "Sylvain",
                "last_name": "Degue",
                "number": 1111222233334444,
                "cvv": "856",
                "exp": {"month":12,"year":2024},
            }
        }
        assert TransactionCreateSchema().validate(data=data) == {}\


    @pytest.mark.parametrize("amount,purchase_desc",[
        (-100.00, None),
        (123.01, 12),
        (0.001, "Fraction de cent"),
        (1, "Fraction de cent") #Ceci ne devrait pas fonctionner
    ],ids=[])
    def test_invalid_transaction(self,amount,purchase_desc):
        data = {
            "amount": amount,
            "purchase_desc": purchase_desc,
            "merchant": {"name": "Elvis", "id": "fhvg"},
            "credit_card":{
                "first_name": "Sylvain",
                "last_name": "Degue",
                "number": 1111222233334444,
                "cvv": "856",
                "exp": "12/2019",
            }
        }
        assert TransactionCreateSchema().validate(data=data) != {}


class TestTransactionProcessSchema(object):

    @pytest.mark.parametrize("api_key,action,trans_id", [
        ("2135235125", CANCEL_TRANS, 23152352523),
        ("2135235125", CONFIRM_TRANS, 23152352523)
    ], ids=[])
    def test_valid_process(self, api_key, action, trans_id):
        data = {
            "MERCHANT_API_KEY": api_key,
            "action": action,
            "transaction_number": trans_id
        }

        assert TransactionProcessSchema().validate(data=data) == {}

    @pytest.mark.parametrize("api_key,action,trans_id", [
        ("2135235125", CANCEL_TRANS, None),
        ("2135235125", "okok", 23152352523),
        (None, CANCEL_TRANS, 23152352523)
    ], ids=[])
    def test_invalid_process(self, api_key, action, trans_id):
        data = {
            "MERCHANT_API_KEY": api_key,
            "action": action,
            "transaction_number": trans_id
        }

        assert TransactionProcessSchema().validate(data=data) != {}
