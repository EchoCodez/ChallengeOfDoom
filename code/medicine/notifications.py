from plyer import notification
import os
import base64
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from email.mime.text import MIMEText

class Notification:
    def __init__(self, title: str, message: str, time: str, increment: int =1440):
        self.title = title
        self.message = message
        if len(time) != 8:
            self.time = "0" + time
        else:
            self.time = time
        if self.time[-2] == "P":
            self.time = str(int(self.time[0:2])+12)+self.time[2:5]+":00"
        else:
            self.time = self.time[0:5]+":00"
        self.increment = increment

    def send(self):
        notification.notify(
            title = self.title,
            message = self.message,
        )
        self.credentials_file = 'json/credentials.json'
        self.token_file = 'json/token.json'
        self.scopes = ['https://www.googleapis.com/auth/gmail.send']
        
        self.sender_email = 'healthapp317@gmail.com'
        self.recipient_email = 'mihir.nimkar@gmail.com'

        self.send_email(self.sender_email, self.recipient_email)

    def send_email(self, sender, to):
        flow = InstalledAppFlow.from_client_secrets_file(self.credentials_file, self.scopes)
        if os.path.exists(self.token_file):
            credentials = Credentials.from_authorized_user_file(self.token_file, self.scopes)
        else:
            credentials = flow.run_local_server(port=0)

            with open(self.token_file, 'w') as token:
                token.write(credentials.to_json())

        service = build('gmail', 'v1', credentials=credentials)

        message = MIMEText(self.message)
        message['to'] = to
        message['from'] = sender
        message['subject'] = self.title
        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')
        email = {'raw': raw_message}
        try:
            message = (service.users().messages().send(userId="me", body=email)
                    .execute())
            print('Message sent successfully.')
            return message
        except HttpError as error:
            print('An error occurred:', error)        
    
    def __repr__(self) -> str:
        return "{0}(title={1}, message={2}, time={3})".format(self.__class__.__name__, self.title, self.message, self.time)