from django.core.checks import messages
from django.core.mail import mail_managers, send_mail  , EmailMultiAlternatives
from django.conf import settings
import qrcode
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.files.storage import FileSystemStorage
from email.mime.image import MIMEImage
from PIL import Image , ImageDraw , ImageFont
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import (Mail, Attachment, FileContent, FileName, FileType, Disposition)
import base64


STORAGE_PREFIX = "http://127.0.0.1:8000"


def mail_services(message , recipient_list):
    message = Mail(
    from_email="vaccine@katzpharmacy.com",
    to_emails=recipient_list,
    subject='Vaccine Management Portal',
    html_content='<strong>' + message + '</strong>')

    sg = SendGridAPIClient("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")
    response = sg.send(message)


def QR_code_Service(recipient_id , message ,mail_message, user_id , STORAGE_PREFIX =STORAGE_PREFIX ):

    subject = 'Vaccine Management portal'
    qr_code = qrcode.make(message)
    fs = FileSystemStorage()
    qr_location = str(user_id) + ".png"
    qr_code.save("media/QR/" + qr_location)
    uploaded_file_url =  STORAGE_PREFIX + fs.url(qr_location)
    with open("media/QR/" + qr_location,'rb') as f:
        x = f.read()   



    message = Mail(
    from_email="vaccine@katzpharmacy.com",
    to_emails=recipient_id,
    subject='Vaccine Management Portal',
    html_content='<strong>' + mail_message + '</strong>')

    encoded_file = base64.b64encode(x).decode()  
    attachedFile = Attachment(
    FileContent(encoded_file),
    FileName('attachment.png'),
    FileType('application/pdf'),
    Disposition('attachment'))

    message.attachment = attachedFile   

    sg = SendGridAPIClient("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")
    response = sg.send(message)


    return 1


# # Certificate generation service
# def generate_certificate(name , date  ,vaccine_name, vaccinated_by , message):
#     image = Image.open('media/External_document/template.jpg')
#     font = ImageFont.truetype("media/External_document/arial.ttf", size=25)
#     draw = ImageDraw.Draw(image)
#     draw.text(xy=(585,471),text='{}'.format(name) , fill=(0,0,0),font=font)
#     draw.text(xy=(456,582),text='{}'.format(vaccine_name) , fill=(0,0,0),font=font)
#     draw.text(xy=(267,644),text='{}'.format(date) , fill=(0,0,0),font=font)
#     draw.text(xy=(379,747),text='{}'.format(vaccinated_by) , fill=(0,0,0),font=font)
#     draw.text(xy=(349,700),text='{}'.format(message) , fill=(0,0,0),font=font)
#     location = ("media/Certificates/" + name + date[:15] + ".pdf").replace(" ","-")
#     image.save(location)
#     fs = FileSystemStorage()
#     uploaded_file_url =  "https://127.0.0.1:8000" + fs.url(location)[6:]
#     return uploaded_file_url
    
