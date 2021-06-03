# simple-payment-service

## Prerequisites
- docker
- docker-compose

## Install
- run ``docker-compose up``

Service will be available by default on http://localhost:5000

## Linters and tests
- attach to container with ``simplepaymentservice``
- ``flake8 ``
- ``isort . --check-only``
- ``black --check -l 90 -S .``
- ``pytest tests``


## Api

### Docs
``GET`` /docs

### Users
- ``POST`` /api/v1/users - create new user with wallet
    #### Request body
    ```
    {
      "username": "string",
      "password": "string"
    }
    ```

- ``POST`` /api/v1/users/login - get access token by username and password(expire time - 15min)
    #### Request body
    ```
    {
      "username": "string",
      "password": "string"
    }
    ```
    #### Response
    ```
    {
      "access_token": "string"
    }
    ```

- ``GET`` /api/v1/users/me - get account info [auth header required]
    #### Headers
      - Authorization
    #### Response
    ```
    {
      "username": "string",
      "currency_code": "string",
      "balance": Decimal
    }
    ```

### Wallets
- ``PATCH`` /api/v1/wallets/receive - receive money on your wallet
    #### Headers
      - Authorization
      - x-idempotency-key
    #### Request body
    ```
    {
      "amount": Decimal
    }
    ```
    #### Response
    ```
    {
      "balance": Decimal
    }
    ```

- ``PATCH`` /api/v1/wallets/send - send money to other user`s wallet
    #### Headers
      - Authorization
      - x-idempotency-key
    #### Request body
    ```
    {
      "target_username": "string",
      "amount": Decimal
    }
    ```
    #### Response
    ```
    {
      "balance": Decimal
    }
    ```

### Transfers history
- ``GET`` /api/v1/transfers - get transfer history of current account
    #### Headers
      - Authorization
    #### Response
    ```
    [
      {
        "type": "incoming",
        "amount": Decimal,
        "transfer_time": datetime
      }
    ]
    ```

## Example of usage
### Create user
```
curl --location --request POST 'http://localhost:5000/api/v1/users/' \
--header 'Content-Type: application/json' \
--data-raw '{
    "username":"test",
    "password":"123"
}'
```

```
{
    "username": "test"
}
```
### Login
```
curl --location --request POST 'http://localhost:5000/api/v1/users/login' \
--header 'Content-Type: application/json' \
--data-raw '{
    "username":"test",
    "password":"123"
}'
```

```
{
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ0ZXN0IiwiaWF0IjoxNjIyNzA1Mjc1LCJuYmYiOjE2MjI3MDUyNzUsImp0aSI6Ijk0ZThkZjNjLTk0NDMtNDQwMC1iZGFmLTkyOWFmMDI1YTRjNiIsImV4cCI6MTYyMjcwNjE3NSwidHlwZSI6ImFjY2VzcyIsImZyZXNoIjpmYWxzZX0.eQVeXV_1rRZELMzskM3QlCCXrSOvupPCphC6UScGNEQ"
}
```

### Me
```
curl --location --request GET 'http://localhost:5000/api/v1/users/me' \
--header 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ0ZXN0IiwiaWF0IjoxNjIyNzA1Mjc1LCJuYmYiOjE2MjI3MDUyNzUsImp0aSI6Ijk0ZThkZjNjLTk0NDMtNDQwMC1iZGFmLTkyOWFmMDI1YTRjNiIsImV4cCI6MTYyMjcwNjE3NSwidHlwZSI6ImFjY2VzcyIsImZyZXNoIjpmYWxzZX0.eQVeXV_1rRZELMzskM3QlCCXrSOvupPCphC6UScGNEQ'
```
```
{
    "username": "test",
    "currency_code": "USD",
    "balance": 0.0
}
```

### Receive money
```
curl --location --request PATCH 'http://localhost:5000/api/v1/wallets/receive' \
--header 'x-idempotency-key: 54t45g54tg54g5443rgrtg' \
--header 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ0ZXN0IiwiaWF0IjoxNjIyNzA1Mjc1LCJuYmYiOjE2MjI3MDUyNzUsImp0aSI6Ijk0ZThkZjNjLTk0NDMtNDQwMC1iZGFmLTkyOWFmMDI1YTRjNiIsImV4cCI6MTYyMjcwNjE3NSwidHlwZSI6ImFjY2VzcyIsImZyZXNoIjpmYWxzZX0.eQVeXV_1rRZELMzskM3QlCCXrSOvupPCphC6UScGNEQ' \
--header 'Content-Type: application/json' \
--data-raw '{
    "amount":10
}'
```

```
{
    "balance": 10.0
}
```

### Send money
- create ``other_user``
```
curl --location --request PATCH 'http://localhost:5000/api/v1/wallets/send' \
--header 'x-idempotency-key: 4r345t45tyg54t54' \
--header 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ0ZXN0IiwiaWF0IjoxNjIyNzA1Mjc1LCJuYmYiOjE2MjI3MDUyNzUsImp0aSI6Ijk0ZThkZjNjLTk0NDMtNDQwMC1iZGFmLTkyOWFmMDI1YTRjNiIsImV4cCI6MTYyMjcwNjE3NSwidHlwZSI6ImFjY2VzcyIsImZyZXNoIjpmYWxzZX0.eQVeXV_1rRZELMzskM3QlCCXrSOvupPCphC6UScGNEQ' \
--header 'Content-Type: application/json' \
--data-raw '{
    "target_username": "other_user",
    "amount":10
}'
```

```
{
    "balance": 0.0
}
```
