# Simple Invoice generating API 

## Requirements
- Python 3.10.1
- Django 4.0
- Django REST Framework

## Installation
 create a virtual environment
```
python -m venv env
```
activate the virtual environment

You can install all the required dependencies by running
```
pip install -r requirements.txt
```
### Install wkhtmltopdf
For PDF generation we need to install wkhtmltopdf. 
Open this link to install wkhtmltopdf

https://wkhtmltopdf.org/downloads.html

After Installing add the wkhtmltopdf path to setting.py

```python
#settings.py

PATH_WKHTMLTOPDF = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
```


## Structure

Endpoint |HTTP Method | CRUD Method | Result
-- | -- |-- |--
`register/` | POST | Create a user
`login/` | POST | Login
`api/token/refresh/` | GET | Get Refresh Token
`item_list/` | GET | Get all items
`item/:id` | GET,PUT,DELETE |  Get/Update/Delete a single item
`invoice/`| POST | Generate Invoice




## Create users 

First we need to create a user, so we can log in
```

http://127.0.0.1:8000/register/ 
method: POST 
body:
{
    "username":"username",
    "password":"password",
    "email":"user@mail.com"
}
```
## Login and Get Token
```

http://127.0.0.1:8000/login/
method: POST 
body:
{
    "username":"username",
    "password":"password",
}
```
We will get token after login
```
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYxNjI5MjMyMSwianRpIjoiNGNkODA3YTlkMmMxNDA2NWFhMzNhYzMxOTgyMzhkZTgiLCJ1c2VyX2lkIjozfQ.hP1wPOPvaPo2DYTC9M1AuOSogdRL_mGP30CHsbpf4zA",
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjE2MjA2MjIxLCJqdGkiOiJjNTNlNThmYjE4N2Q0YWY2YTE5MGNiMzhlNjU5ZmI0NSIsInVzZXJfaWQiOjN9.Csz-SgXoItUbT3RgB3zXhjA2DAv77hpYjqlgEMNAHps"
}
```



We got two tokens, the access token will be used to authenticated all the requests we need to make, this access token will expire after some time.
We can use the refresh token to request a need access token.

requesting new access token
```
http://127.0.0.1:8000/api/token/refresh/
method:POST
Body:
{
    refresh:"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYxNjI5MjMyMSwianRpIjoiNGNkODA3YTlkMmMxNDA2NWFhMzNhYzMxOTgyMzhkZTgiLCJ1c2VyX2lkIjozfQ.hP1wPOPvaPo2DYTC9M1AuOSogdRL_mGP30CHsbpf4zA"
}
```
and we will get a new access token
```
{
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjE2MjA4Mjk1LCJqdGkiOiI4NGNhZmMzMmFiZDA0MDQ2YjZhMzFhZjJjMmRiNjUyYyIsInVzZXJfaWQiOjJ9.NJrs-sXnghAwcMsIWyCvE2RuGcQ3Hiu5p3vBmLkHSvM"
}
```
## Add Items and List Items
To add items
```
http://127.0.0.1:8000/item_list/
method: POST 
body:
{
    "name":"item name"
    "quantity":3
    "unit_price":100
    "tax":10
}
Header:
{
Authorization:Bearer <Access_token>
}
```

To Retrive The Item Lists
```
http://127.0.0.1:8000/item_list/
method: GET
Header:
{
Authorization:Bearer <Access_token>
}
```
It will response the all items list

## Retrieve,Delete or Update single Item

User can retrive , update or delete an item added by them.
```
http://127.0.0.1:8000/item/:id/
method: 
    GET - To retrive an Item
    PUT- To update an Item
    DELETE - To Delete an Item
Header:
{
Authorization:Bearer <Access_token>
}
```
## Generate invoice for list of items

Accepts list of items(each items has 'item_id' and 'quantity') and generates invoce pdf
```
http://127.0.0.1:8000/invoice/
method: POST
Body:
{
    "items":[
        {
            "item_id":1,
            "quantity":2
        },
        {
            "item_id":2,
            "quantity":5
        }
    ],
    "discount":20
}
```
A sample response will be like this
```
{
    "id": 28,
    "invoice": "http://localhost:8000/media/invoices/invoice.pdf",
    "date_created": "2022-01-06T14:52:19.057579Z"
}
```
If the quantity given is greater than the available quantity it will response an error message
```
{
    "Error_list": "product 1.CATE RIGID BAG has only 10 items left"
}
```

###Test inputs and responses are stored in invoice_api.postman_collection.json