# Coins wallet service API
## Version: v1
## Base path: /wallet

### /accounts/

#### GET
##### Description:

Return a list of all the existing accounts.

##### Parameters

None.

##### Responses

| Code | Description | Schema                  |
| ---- | ----------- | ----------------------- |
| 200  |             | [ [Account](#account) ] |

#### POST
##### Description:

Create a new account instance.

##### Parameters

| Name | Located in | Description | Required | Schema              |
| ---- | ---------- | ----------- | -------- | ------------------- |
| data | body       |             | Yes      | [Account](#account) |

##### Responses

| Code | Description | Schema              |
| ---- | ----------- | ------------------- |
| 201  |             | [Account](#account) |

### /accounts/{id}/

#### GET
##### Description:

Return the given account.

##### Parameters

| Name | Located in | Description                                      | Required | Schema  |
| ---- | ---------- | ------------------------------------------------ | -------- | ----    |
| id   | path       | A unique integer value identifying this account. | Yes      | integer |

##### Responses

| Code | Description | Schema              |
| ---- | ----------- | ------------------- |
| 200  |             | [Account](#account) |

### /payments/

#### GET
##### Description:

Return a list of all the existing payments.

##### Parameters

| Name                | Located in | Description | Required | Schema |
| ------------------- | ---------- | ----------- | -------- | ------ |
| source_account      | query      |             | No       | string |
| destination_account | query      |             | No       | string |

##### Responses

| Code | Description | Schema                  |
| ---- | ----------- | ----------------------- |
| 200  |             | [ [Payment](#payment) ] |

#### POST
##### Description:

Create a new payment instance.

##### Parameters

| Name | Located in | Description | Required | Schema              |
| ---- | ---------- | ----------- | -------- | ------------------- |
| data | body       |             | Yes      | [Payment](#payment) |

##### Responses

| Code | Description | Schema              |
| ---- | ----------- | ------------------- |
| 201  |             | [Payment](#payment) |

### Models


#### Account

| Name     | Type             | Description                | Required | ReadOnly |
| -------- | ---------------- | -------------------------- | -------- | -------- |
| id       | integer          |                            | No       | Yes      |
| name     | string           | unique name of account     | Yes      | No       |
| balance  | string (decimal) | amount of money in account | Yes      | No       |
| currency | enum (USD, PHP)  | money currency of account  | Yes      | No       |

#### Payment

| Name                | Type             | Description                    | Required | ReadOnly |
| ------------------- | ---------------- | ------------------------------ | -------- | -------- |
| id                  | integer          |                                | No       | Yes      |
| source_account      | integer          | account from which money comes | Yes      | No       |
| destination_account | integer          | account to which money comes   | Yes      | No       |
| amount              | string (decimal) | payment amount                 | Yes      | No       |
| currency            | enum (USD, PHP)  | money currency of payment      | No       | Yes      |
| created_datetime    | dateTime         | time of payment                | No       | yes      |
