import pytest
@pytest.mark.api
@pytest.mark.auth
def test_auth_api():
   pass

@pytest.mark.ui
@pytest.mark.auth
def test_auth_ui():
   pass

@pytest.mark.api
@pytest.mark.event
def test_event_api():
   pass

@pytest.mark.ui
@pytest.mark.event
def test_event_ui():
   pass

# путь выглядит так (venv) C:\pythonProject\SF_mod_21
# в терминале задать pytest 21_5.py -v -m "api"
# другие варианты команд в терминале
# pytest test.py -v -m "auth or event"
# pytest 21_5.py -v -m "ui and auth"

