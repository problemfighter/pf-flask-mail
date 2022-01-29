from pf_flask_mail.common.pffm_config import PFFMConfig
from pf_flask_mail.pffm_send_mail import PFFMSendMail

if __name__ == '__main__':
    config = PFFMConfig()
    config.smtpServer = "smtp.gmail.com"
    config.smtpUser = "pfdevtester@gmail.com"
    config.smtpPassword = ""
    config.smtpPort = 465

    send_email = PFFMSendMail(config)

    send_email.compose(["hmtmcse@gmail.com"], "Attachment")
    send_email.add_html_message("<h1>This is HTML Body With Attachment</h1>")
    send_email.add_attachment("logo.png")
    send_email.add_attachment("test.pdf")
    send_email.send(False)

    send_email.compose(["hmtmcse.office@gmail.com", "hmtmcse@gmail.com"], "Test only Text Email")
    send_email.add_text_message("This is Text email from send email test")
    send_email.send(False)

    send_email.compose("hmtmcse@gmail.com", "Test with cc")
    send_email.add_text_message("CC Email Test")
    send_email.add_cc("hmtmcse.office@gmail.com")
    send_email.send(False)

    send_email.compose("hmtmcse@gmail.com", "Test with BCC")
    send_email.add_text_message("BCC Email Test")
    send_email.add_bcc("hmtmcse.office@gmail.com")
    send_email.send(False)

    send_email.compose(["hmtmcse@gmail.com"], "HTML Email Test")
    send_email.add_html_message("<h1>This is HTML Body </h1>")
    send_email.send(False)

    send_email.compose("hmtmcse@gmail.com", "Test only Text Email")
    send_email.add_text_message("This is Text email from send email test")
    send_email.send()
