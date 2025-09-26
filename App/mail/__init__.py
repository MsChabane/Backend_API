from fastapi_mail import FastMail,ConnectionConfig,MessageSchema,MessageType
from ..config import config
from pathlib import Path
from datetime import date

Base_DIR=Path(__file__).resolve().parent.parent

mail_config=ConnectionConfig(

    MAIL_USERNAME=config.MAIL_USERNAME,   
    MAIL_PASSWORD=config.MAIL_PASSWORD,  
    MAIL_FROM=config.MAIL_FROM,
    MAIL_PORT=config.MAIL_PORT,               
    MAIL_SERVER=config.MAIL_SERVER,
    MAIL_STARTTLS=False,        
    MAIL_SSL_TLS=True,           
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
    TEMPLATE_FOLDER=str(Path(Base_DIR,'templates'))
)

mail = FastMail(config=mail_config)

async def send_verifcation_mail(email:str,token:str):
    message = MessageSchema(
        subject="Verification email",
        recipients=[email],
        template_body={
            'email':email,
            "token":token,
            "year":date.today().year
        },
        subtype=MessageType.html
    )
    await mail.send_message(message=message,template_name='email_verification.html')

async def send_reset_password(email:str,token:str):
    message = MessageSchema(
        subject="Reset Password",
        recipients=[email],
        template_body={
            'email':email,
            "token":token,
            "year":date.today().year
        },
        subtype=MessageType.html
    )
    await mail.send_message(message=message,template_name='reset-password.html')


