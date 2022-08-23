import logging
import smtplib


def send_email(server, addr_to, addr_from, subj, body):
    message = "\r\n".join((
        f"From: {addr_from}",
        f"To: {addr_to}",
        f"Subject: {subj}",
        "",
        body
    ))
    try:
        smtp = smtplib.SMTP(server)
        smtp.sendmail(addr_from, [addr_to], message)
        smtp.quit()
        logging.info("Email sent")
    except smtplib.SMTPException as e:
        logging.error(f"Unable to send email. Check SMTP Settings! {e}")
