import pytest

from ..domain.value_object import Money, URL
from ..domain.rule import BusinessRuleValidationException


@pytest.mark.unit
@pytest.mark.domain
def test_money():
    m1 = Money(100)
    m2 = Money(100)
    m3 = Money(100, "USD")
    m4 = Money(150, "USD")

    assert m1 == m2
    assert not (m2 == m3)
    assert m3 < m4


@pytest.mark.unit
@pytest.mark.domain
def test_URL():
    u_w_path = URL.get_URL("https://github.com/ES2-UFPI/WiseBuilder")
    u_wo_path = URL.get_URL("https://github.com")

    assert u_w_path.domain == "github.com"
    assert u_wo_path.domain == "github.com"

    with pytest.raises(BusinessRuleValidationException) as excinfo:
        URL.get_URL("github.com/ES2-UFPI/WiseBuilder")
