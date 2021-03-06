import json
import requests


class SMSCuba:

    '''
    Sends messages (SMS) to Cuba and any other allowed country

    Args:
        client_id (string): Client id of the user, will be provided upon sign in 
        api_key (string): Api KEY, will be provided upon sign in, client can change it.
    
    Example:
        To send a message simply create a SMSCuba object with the correct client ID
        and API, and send the message with the "send_message" function.

            $ sms_client = SMSCuba(<client_id>, <api_key>)
            $ resp = sms_client.send_message('+1234578900', 'Write whatever message you would like')
            $ print(resp)
    '''

    def __init__(self, client_id, api_key):
        self.client_id = client_id
        self.api_key = api_key
        self.base_url = 'https://us-central1-sms-cuba.cloudfunctions.net'
        self.url_sms = '{}/sms_request'.format(self.base_url)
        self.url_validate = '{}/validate_client'.format(self.base_url)

        # Logs the client
        self.login_client()


    def login_client(self):
        client_logged = True

        # Quick sanity check for values
        if not self.client_id:
            raise ValueError('Please enter a valid Client ID')

        if not self.api_key:
            raise ValueError('Please enter a valid API Key')

        params = {
            'client_id': self.client_id,
            'api_key': self.api_key,
        }
        response = requests.get(self.url_validate, params=params)
        response_data = json.loads(response.content)

        if response_data['status'] != 'success':
            client_logged = False
        
        if client_logged is not True:
            raise ConnectionError('Invalid credentials, please check your Client ID and/or API Key')

        return response_data


    def send_message(self, recipients, message):
        '''
        Args:
            recipient
        '''
        params = {
            'client_id': self.client_id,
            'api_key': self.api_key,
            'recipient': recipients,
            'message': message
        }

        response = requests.get(self.url_sms, params=params)
        return response.content
