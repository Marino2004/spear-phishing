import smtplib
import json
import os
from string import Template
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class MailSender:
    def __init__(self, smtp_server='localhost', smtp_port=1025):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port

    def load_user_data(self, filename="../../script/output.json"):
        path = os.path.join(os.path.dirname(__file__), filename)
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    def load_template(self, user_data, template_path="../../../templates/mail.html"):
        full_path = os.path.join(os.path.dirname(__file__), template_path)
        with open(full_path, "r", encoding="utf-8") as file:
            raw_template = Template(file.read())

        return raw_template.substitute(
            name=user_data["name"],
            location=user_data["location"],
            lang=user_data["top"],
            link=user_data["link"])

    def create_email(self, user_data):
        from_email = "recrutement@github.com"
        to_email = f"{user_data['user']}@example.com"
        subject = "Offre d'emploi exclusive de GitHub"

        html_content = self.load_template(user_data)

        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = from_email
        message["To"] = to_email
        message.attach(MIMEText(html_content, "html"))

        return from_email, to_email, message.as_string()

    def send_email(self):
        user_data = self.load_user_data()
        from_email, to_email, message = self.create_email(user_data)

        try:
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.sendmail(from_email, to_email, message)
                print(f"✅ Email envoyé à {to_email}")
        except Exception as e:
            print(f"❌ Erreur lors de l'envoi de l'email : {e}")

if __name__ == "__main__":
    sender = MailSender()
    sender.send_email()