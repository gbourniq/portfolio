from unittest.mock import Mock


class TestItem:
    def test_1(self, monkeypatch, item_instance):
        mock_1 = Mock()
        return mock_1

    def test_2(self, monkeypatch, item_instance):
        mock_2 = Mock()
        return mock_2
