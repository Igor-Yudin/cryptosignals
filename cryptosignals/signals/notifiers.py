import smtplib
import json

import telegram
import slackweb
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_fixed

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

class TelegramNotifier:
    """Used to notify user of events via telegram.
    """

    def __init__(self, token, chat_id, parse_mode):
        """Initialize TelegramNotifier class
        Args:
            token (str): The telegram API token.
            chat_id (str): The chat ID you want the bot to send messages to.
        """

        self.bot = telegram.Bot(token=token)
        self.chat_id = chat_id
        self.parse_mode = parse_mode


    @retry(
        retry=retry_if_exception_type(telegram.error.TimedOut),
        stop=stop_after_attempt(3),
        wait=wait_fixed(5)
    )
    def notify(self, message):
        """Send the notification.
        Args:
            message (str): The message to send.
        """

        max_message_size = 4096
        message_chunks = self.chunk_message(message=message, max_message_size=max_message_size)
        #print(message_chunks)
        #exit()
        for message_chunk in message_chunks:
            self.bot.send_message(chat_id=self.chat_id, text=message_chunk, parse_mode=self.parse_mode)

class SlackNotifier:
    """Class for handling slack notifications
    """

    def __init__(self, slack_webhook):
        """Initialize SlackNotifier class
        Args:
            slack_webhook (str): Slack web hook to allow message sending.
        """

        # self.logger = structlog.get_logger()
        self.slack_name = "crypto-signal"
        self.slack_client = slackweb.Slack(url=slack_webhook)

    def notify(self, message):
        """Sends the message.
        Args:
            message (str): The message to send.
        """

        assert len(message) <= 4096
        # max_message_size = 4096
        # message_chunks = self.chunk_message(message=message, max_message_size=max_message_size)

        # for message_chunk in message_chunks:
        self.slack_client.notify(text=message)