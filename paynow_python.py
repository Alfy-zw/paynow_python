from paynow import Paynow
import time
from pytictoc import TicToc


# wait for payment response using transaction poll url
def payment_status_handler(check_poll_url):
    # initialising timer, to monitor transaction execution time
    timer = TicToc()
    timer.tic()
    trans_response = {'status': '', 'transaction_data': ''}
    #
    while True:
        # ten second delay waiting for paid status
        time.sleep(10)
        transaction_state = paynow.check_transaction_status(check_poll_url)
        print(transaction_state.status)
        if transaction_state.status == 'paid' or timer.tocvalue() > 12.00:
            trans_response.update({'status': transaction_state.status,
                                   'transaction_data': {'amount': transaction_state.amount,
                                                        'local_ref': transaction_state.reference,
                                                        'paynow_ref': transaction_state.paynow_reference,
                                                        'poll_url': check_poll_url,
                                                        'hash': transaction_state.hash}})
            return trans_response


# initialising paynow object
paynow = Paynow(
    'INTEGRATION_ID',
    'INTEGRATION_KEY',
    'http://google.com',
    'http://google.com'
)

# customer detail for transaction
customer_email = 'alfredtkudiwa@gmail.com'
customer_mobile_number = '0771111111'

# transaction detail
invoice_ref = 'Order'
transaction_amount = 1.20
transaction_description = 'Payment for stuff'

# wallet name
if customer_mobile_number[0:3] == '073':
    wallet_name = 'telecash'
elif customer_mobile_number[0:3] == '071':
    wallet_name = 'onemoney'
else:
    wallet_name = 'ecocash'

# initialising paynow transaction
payment = paynow.create_payment(invoice_ref, customer_email)
# adding items to payment transaction object
payment.add(transaction_description, transaction_amount)
# sending transaction through paynow to customer for mobile wallet authorization
response = paynow.send_mobile(payment, customer_mobile_number, wallet_name)

if response.success:
    # wait for paynow response from the status handler function
    paynow_response = payment_status_handler(response.poll_url)
else:
    paynow_response = {'status': 'error', 'error': 'unknown error'}

# response from paynow transaction
print(paynow_response)
