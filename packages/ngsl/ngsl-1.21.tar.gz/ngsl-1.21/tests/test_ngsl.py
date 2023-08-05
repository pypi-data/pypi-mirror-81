from ngsl import ngsl
from ngsl.dictionary import DICTIONARY


def test_include():
    assert ngsl.include('smile')
    assert ngsl.include('smiles')


def test_get_infinitiv():
    assert ngsl.get_infinitiv('smiles') == 'smile'


def test_get_infinitiv_list():
    assert ngsl.get_infinitiv_list(['smiles', 'quarterback']) == set(['smile'])


def test_all_infinitiv():
    assert ngsl.all_infinitiv() == DICTIONARY.keys()
