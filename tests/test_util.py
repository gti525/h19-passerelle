
import pytest
from  app.utils.genrators import add_leading_zero

class TestUtil(object):

    @pytest.mark.parametrize("input,output", [
        (1,"01"),
        ("01","01"),
    ])
    def test_add_en(self, input, output):
        assert output == add_leading_zero(input)
