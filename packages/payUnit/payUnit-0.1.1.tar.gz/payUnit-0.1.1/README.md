# PayUnit
<p align="center">
    <h4 align="center">An python payment sdk for MTN Mobile Money,Orange Money,Express Union and Yup transactions.</h4>
</p>

## Installation

```bash
pip install payunit
```

## Usage
**Firstly, Create an instance of payunit, passing as parameter a dictionary with properties**

*   **user_api** :  Your user api from payunit dashboard.
*   **password_api** : Your user password api from payunit dashboard.
*   **api_key** :  Your user password api from payunit dashboard.
*   **return_url** :  The return url to your website, for either transaction completed successfully or transaction failed.

**Call the make payment method, passing in the amount for the transaction as parameters**
#### Example

```py
from payunit import payunit

# Enter your config details as parameters
payment = payunit({
    "user_api": "Your_User_Api",
    "password_api": "Your_Password_Api",
    "api_key": "Your_User_Api_Kay",
    "return_url": "Return_Url_To_Your_Website"
})


# Spawns a new transaction process of 4000
payment.makePayment(4000)
```
