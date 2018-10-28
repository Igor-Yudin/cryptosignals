import smtplib

from tenacity import retry, retry_if_exception_type, stop_after_attempt

class GmailNotifier():
    """Class for handling gmail notifications
    """

    def __init__(self, username, password, destination_addresses):
        """Initialize GmailNotifier class
        Args:
            username (str): Username of the gmail account to use for sending message.
            password (str): Password of the gmail account to use for sending message.
            destination_addresses (list): A list of email addresses to notify.
        """

        self.username = username
        self.password = password
        self.destination_addresses = destination_addresses


    @retry(stop=stop_after_attempt(3))
    def notify(self, subject, message):
        message = """From: %s\nTo: %s\nSubject: %s\n\n%s
        """ % (self.username, ', '.join(self.destination_addresses), subject, message)
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(self.username, self.password)
        server.sendmail(self.username, self.destination_addresses, message)
        server.close()