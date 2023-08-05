from ngsl import ngsl


def test_search():
    assert ngsl.include('smile')
    assert ngsl.include('smiles')
    assert ngsl.get_infinitiv('smiles') == 'smile'
