import bl


def test_GetPrice():
    assert bl.GetPrice("THB_BTC") > 0


def test_GetMyBalances():
    assert any(bl.GetMyBalances())


def test_GetMyOrder():
    assert any(bl.GetMyOrder('THB_SNT'))


def test_CancelOrder():
    assert bl.CancelOrder('') > 0


def test_SellOrder():
    assert bl.SellOrder('', 0, 0) > 0


def test_BuyOrder():
    assert bl.BuyOrder('', 0, 0) > 0


def test_Authenticate():
    assert len(bl.Authenticate('', '')) == 0


def test_Trading():
    assert bl.Trading("ADA") == "OK"
