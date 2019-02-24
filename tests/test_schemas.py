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
        "number": "1111222233334444",
        "cvv": 856,
        "exp": "12/19",
    }

class TestCreditCardSchema(object):

    @pytest.mark.parametrize("first_name,last_name, number, cvv, exp", [
        ("John", "Doe", "1111222233334444", 123, "12/24"),
        ("John", "Doe", "1111222233334444", 856, "12/19"),
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
        ("John", "Doe", None, 123, "12/24"),
        ("John", "Doe", "1111222233334444", 456, "1219"),
        (None, "Doe", "1111222233334444", 678, "12/29"),
        ("John", None, "1111222233334444", 912, "12/29"),
        ("John", "Doe", "3569380356438091", 321, "12/29"),
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
        (500,"De la drogue")
    ],ids=[])
    def test_valid_transaction(self,amount,purchase_desc):
        data = {
            "amount": amount,
            "purchase_desc": purchase_desc,
            "merchant": {"name": "Elvis", "id": "fhvg"},
            "credit_card":{
                "first_name": "Sylvain",
                "last_name": "Degue",
                "number": "1111222233334444",
                "cvv": 856,
                "exp": "12/19",
            }
        }
        assert TransactionCreateSchema().validate(data=data) == {}\


    @pytest.mark.parametrize("amount,purchase_desc",[
        (-100,None),
        (123,12),
    ],ids=[])
    def test_invalid_transaction(self,amount,purchase_desc):
        data = {
            "amount": amount,
            "purchase_desc": purchase_desc,
            "merchant": {"name": "Elvis", "id": "fhvg"},
            "credit_card":{
                "first_name": "Sylvain",
                "last_name": "Degue",
                "number": "1111222233334444",
                "cvv": 856,
                "exp": "12/19",
            }
        }
        assert TransactionCreateSchema().validate(data=data) != {}