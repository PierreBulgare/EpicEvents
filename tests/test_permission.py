from utils.permission import Permission

def test_client_management():
    assert Permission.client_management("Commercial") is True
    assert Permission.client_management("Gestion") is False
    assert Permission.client_management("Support") is False

def test_contract_management():
    assert Permission.contract_management("Commercial") is True
    assert Permission.contract_management("Gestion") is True
    assert Permission.contract_management("Support") is False

def test_sign_contract():
    assert Permission.sign_contract("Commercial") is True
    assert Permission.sign_contract("Gestion") is False
    assert Permission.sign_contract("Support") is False

def test_collab_management():
    assert Permission.collab_management("Commercial") is False
    assert Permission.collab_management("Gestion") is True
    assert Permission.collab_management("Support") is False

def test_create_event():
    assert Permission.create_event("Commercial") is True
    assert Permission.create_event("Gestion") is False
    assert Permission.create_event("Support") is False

def test_assign_event():
    assert Permission.assign_event("Commercial") is False
    assert Permission.assign_event("Gestion") is True
    assert Permission.assign_event("Support") is False

def test_update_event():
    assert Permission.update_event("Commercial") is True
    assert Permission.update_event("Gestion") is False
    assert Permission.update_event("Support") is True

def test_delete_event():
    assert Permission.delete_event("Commercial") is True
    assert Permission.delete_event("Gestion") is False
    assert Permission.delete_event("Support") is False