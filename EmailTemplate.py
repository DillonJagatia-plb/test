from appscript import app, k, its
from mactypes import Alias
from pathlib import Path
import pandas as pd
import BankContacts
from PMDict import pm_bank_dict

BankContacts = BankContacts.contacts


class Outlook(object):
    def __init__(self):
        self.client = app("Microsoft Outlook")


class Message(object):
    def __init__(
        self,
        parent=None,
        subject="",
        body="",
        to_recip=[],
        cc_recip=[],
        show_=True,
        is_html=False,
    ):

        if parent is None:
            parent = Outlook()
        client = parent.client

        self.msg = client.make(
            new=k.outgoing_message,
            with_properties={k.subject: subject, k.content: body},
        )

        self.add_recipients(emails=to_recip, type_="to")
        self.add_recipients(emails=cc_recip, type_="cc")

        # if attachment: self.add_attachment(file_path=attPath)

        if show_:
            self.show()

    def show(self):
        self.msg.open()
        self.msg.activate()

    # def add_attachment(self, p):
    #     # p is a Path() obj, could also pass string

    #     p = Alias(str(p)) # convert string/path obj to POSIX/mactypes path

    #     attach = self.msg.make(new=k.attachment, with_properties={k.file: p})

    def add_recipients(self, emails, type_="to"):
        if not isinstance(emails, list):
            emails = [emails]
        for email in emails:
            self.add_recipient(email=email, type_=type_)

    def add_recipient(self, email, type_="to"):
        msg = self.msg

        if type_ == "to":
            recipient = k.to_recipient
        elif type_ == "cc":
            recipient = k.cc_recipient

        msg.make(new=recipient, with_properties={k.email_address: {k.address: email}})


def hf_request(
    bank, client, pm_bank_dict
):  # Make sure 'client' is passed as an argument

    msg = f"""<html>
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
    </head>
    <body>
        <div style="font-family: Calibri; font-size: 11pt;">
            <p>Hi {BankContacts[bank][0]},</p>

            <p>I trust this email finds well. We have a request from {client} to access the time series of your strategies.</p>

            <p>Would you be fine? The PM is {pm_bank_dict[bank]}.<br>
            We will make a separate request for position data if / when required.</p>

            <p> Our main contact at {client} is {pm_bank_dict[bank]}.</p>
        </div>
    </body>
    </html>"""

    return msg


def data_request(bank, client, PM):  # Ensure 'client' is passed as an argument

    msg = f"""<html>
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
    </head>
    <body>
        <div style="font-family: Calibri; font-size: 11pt;">
            Hi {BankContacts[bank][0]}

            <p>We have a new request from {PM} at {client} for the below strategies.</p>

            <p>Can you please provide the missing data?<br>
            Are we clear to provide access?</p>
        </div>
    </body>
    </html>"""
    return msg
