from dio import dio
from jotaro import jotaro
from joseph import joseph
from hello import hello


def test_dio():
    assert dio() == 'The World!!!!(Time stops)'


def test_hello():
    assert hello() == 'Hello World'


def test_jotaro():
    assert jotaro() == 'yare yare'


def test_joseph():
    assert joseph() == 'Oh My God!!!'


