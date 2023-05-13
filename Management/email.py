import email
import smtplib
from email.message import EmailMessage

class Email:
    @staticmethod
    def emailGen(name, emailTo, course):
        c = str(course)
        n = str(name)
        subject = "You Have Been Assigned To Course #"+c+""
        text = "Hello "+n+",\n\nYou have been assigned to course #"+c+". Please consult Canvas for full details.\n\nBest,\nUWM CS Department"

        sender = "djangountrained361@gmail.com"
        appPW = "oqbztoxplrfmokrp"

        if sender is None or appPW is None:
            print("did the email or password get set correctly?")
            return False

        msg = EmailMessage()
        msg['Subject'] = subject
        msg['From'] = sender
        msg['To'] = emailTo
        msg.set_content(text)

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(sender, appPW)
            smtp.send_message(msg)