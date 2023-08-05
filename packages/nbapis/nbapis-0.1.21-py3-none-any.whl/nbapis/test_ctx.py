from .ctx import Ctx


def test_ctx():
    c1 = Ctx(auth='')
    c2 = Ctx(auth='')
    c1.uid = '1'
    assert c1.uid == '1'
    c2.uid = '2'
    assert c1.uid == '1'
    assert c2.uid == '2'
