from framework.application.handler import MessageHandler
from ..domain.events import LowerPriceRegisteredEvent

from smtplib import SMTP
from ssl import create_default_context
from email.mime.text import MIMEText
from config import mail, mail_passwd


# Provisório. Mover para microsserviço de usuários.
class LowerPriceRegisteredHandler(MessageHandler):
    def __call__(self, event: LowerPriceRegisteredEvent):
        sender, passwd = mail, mail_passwd
        recv_list = [sender]

        msg = f"Produto com preço reduzido!" f"{event.component}" f"{event.price}"

        message = MIMEText(msg, "plain")

        message[
            "Subject"
        ] = f"Preço reduzido: {event.component.manufacturer} {event.component.model}!"
        message["From"] = sender

        context = create_default_context()
        with SMTP("smtp.gmail.com", 587) as server:
            server.starttls(context=context)
            server.login(sender, passwd)
            server.send_message(message, sender, recv_list)
