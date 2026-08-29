import uuid

import pytest


@pytest.mark.asyncio
async def test_create_wallet(client):
    resp = await client.post("/api/v1/wallets")
    assert resp.status_code == 201
    data = resp.json()
    assert "id" in data
    assert "balance" in data
    assert data["balance"] == 0
    uid = uuid.UUID(data["id"])
    assert str(uid) == data["id"]


@pytest.mark.asyncio
async def test_get_wallet_success(client):
    create_resp = await client.post("/api/v1/wallets")
    assert create_resp.status_code == 201
    wallet = create_resp.json()

    get_resp = await client.get(f"/api/v1/wallets/{wallet['id']}")
    assert get_resp.status_code == 200
    data = get_resp.json()
    assert data["id"] == wallet["id"]
    assert data["balance"] == wallet["balance"]


@pytest.mark.asyncio
async def test_get_wallet_not_found(client):
    fake_id = str(uuid.uuid4())
    resp = await client.get(f"/api/v1/wallets/{fake_id}")
    assert resp.status_code == 404
    data = resp.json()
    assert "detail" in data and "Wallet not found" in data["detail"]


@pytest.mark.asyncio
async def test_deposit_operation(client):
    create_resp = await client.post("/api/v1/wallets")
    assert create_resp.status_code == 201
    wallet = create_resp.json()

    amount = 100
    resp = await client.post(
        f"/api/v1/wallets/{wallet['id']}/operation",
        json={"operation_type": "DEPOSIT", "amount": amount},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert "balance" in data
    assert data["balance"] == amount


@pytest.mark.asyncio
async def test_withdraw_operation(client):
    create_resp = await client.post("/api/v1/wallets")
    assert create_resp.status_code == 201
    wallet = create_resp.json()

    deposit_amount = 200
    await client.post(
        f"/api/v1/wallets/{wallet['id']}/operation",
        json={"operation_type": "DEPOSIT", "amount": deposit_amount},
    )

    withdraw_amount = 50
    resp = await client.post(
        f"/api/v1/wallets/{wallet['id']}/operation",
        json={"operation_type": "WITHDRAW", "amount": withdraw_amount},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["balance"] == deposit_amount - withdraw_amount


@pytest.mark.asyncio
async def test_invalid_operation_type(client):
    create_resp = await client.post("/api/v1/wallets")
    assert create_resp.status_code == 201
    wallet = create_resp.json()

    resp = await client.post(
        f"/api/v1/wallets/{wallet['id']}/operation",
        json={"operation_type": "INVALID_TYPE", "amount": 10},
    )
    assert resp.status_code == 422


@pytest.mark.asyncio
async def test_negative_amount_rejected(client):
    create_resp = await client.post("/api/v1/wallets")
    assert create_resp.status_code == 201
    wallet = create_resp.json()

    resp = await client.post(
        f"/api/v1/wallets/{wallet['id']}/operation",
        json={"operation_type": "DEPOSIT", "amount": -10},
    )
    assert resp.status_code == 422
