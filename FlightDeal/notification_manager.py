import os
from twilio.rest import Client
import smtplib, ssl

class NotificationManager:
    #This class is responsible for sending notifications with the deal flight details.
    def __init__(self) -> None:
        # Twilio Account data
        # account_sid = os.environ["TWILIO_ACCOUNT_SID"]
        # auth_token = os.environ["TWILIO_AUTH_TOKEN"]
        # self.account_number = os.environ["ACCOUNT_NUMBER"]
        # self.my_number = os.environ["MY_NUMBER"]
        account_sid = "___________"
        auth_token = "___________"
        self.account_number = "_________"
        self.my_number = "___________"
        
        self.client = Client(account_sid, auth_token)   # Creating client to be able to send twilio messages.
        
        # Gmail Account data
        # self.gmail_email = os.environ["GMAIL"]
        # gmail_password = os.environ["GMAIL_PASSWORD"]
        self.gmail_email = "__________"
        gmail_password = "___________"
        # Connecting to gmail SMTP server
        context = ssl.create_default_context()
        self.connection = smtplib.SMTP_SSL(host= "smtp.gmail.com", context= context)
        self.connection.login(self.gmail_email, gmail_password)
    
    def send_message(self ,message: str) -> str:
        """Connect to Twilio API and send a message.

        Args:
            message (str): The message to send.

        Returns:
            str: Status of the operation.
        """
        
        message = self.client.messages.create(
            body = message,
            from_ = self.account_number,
            to = self.my_number,
        )
        
        return message.status
    
    def send_email(self, receiving_email: str, email_message: str) -> None:
        self.connection.sendmail(self.gmail_email, receiving_email, email_message)