# -*- coding: utf-8 -*-
"""
Created on Wed Aug 01 15:37:20 2018

@author: martinig
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Aug 01 10:41:41 2018

@author: martinig
"""

import time
import os

import pandas as pd 
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.backends.backend_pdf import PdfPages

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
import smtplib
from email import Encoders

# ==================================================
# CONSOLE
# ==================================================
BASE_DIR = os.getcwd()
recipient_name = 'Tim'
# ==================================================
# Define the actual time in the Netherlands, considering both winter and summer time
# ==================================================

time_unit = "D"
no_days_back = 5
now_epoch = (time.time())*1000000000 
localtime=time.localtime()
now_dt = pd.to_datetime(now_epoch)
print(now_dt)
print(localtime)
hour=now_dt.hour
print(hour)
if localtime[3]-hour==1:
    now_epoch=(time.time()+3600)*1000000000 
elif localtime[3]-hour==-23:
    now_epoch=(time.time()+3600)*1000000000
else:
    now_epoch=(time.time()+3600*2)*1000000000
now_dt = pd.to_datetime(now_epoch)

# Beginning of the current month
start_cm2=pd.datetime(localtime[0],localtime[1],1)

# Beginning of the previous month
if localtime[1]==1:
    pv_month=12
    pv_year=localtime[0]-1
else:
    pv_month=localtime[1]-1
    pv_year=localtime[0]
start_pv=pd.datetime(pv_year,pv_month,1)
print(start_pv)

# ==================================================
# Create the Report cover
# ==================================================
with PdfPages('Pilot Element ' +start_pv.strftime(' %B %Y ')+' Performance Overview.pdf') as pdf:
    fig1=plt.figure()
    ax1 = plt.subplot(221)
    ax2 = plt.subplot(222)
    ax3 = plt.subplot(223)
    ax1.axis('off')
    ax2.axis('off')
    ax3.axis('off')
    img1=mpimg.imread(os.path.join(BASE_DIR,'solaroad_logo.png'))
    ax1.imshow(img1)
    img2=mpimg.imread(os.path.join(BASE_DIR,'tno-logo-1.png'))
    ax2.imshow(img2)
    txt = 'Pilot Element '+start_pv.strftime('%B %Y')+' Performance Overview'
    plt.text(0.25,0.50,txt, transform=fig1.transFigure, size=16)
    plt.tight_layout(pad=0.1,w_pad=20,h_pad=2)
    txt2=now_dt.strftime('%d %B %Y')
    plt.text(0.05,0.05,txt2, transform=fig1.transFigure, size=10)
    fig1.set_size_inches([10,10])
    pdf.savefig(fig1,bbox_inches='tight')
    
# inserting a new page
    fig2=plt.figure()
    ax4 = plt.subplot(221)
    img3=mpimg.imread('C:\Users\martinig\Desktop\Python\misc\solaroad_logo.png')
    ax4.imshow(img3)
    pdf.savefig(fig2,bbox_inches='tight')
    
# ==================================================
# Sending e-mail
# ==================================================

# Create a "related" message container that will hold the HTML 
msg = MIMEMultipart(_subtype='related')
emailcontent = (f"Dear {recipient_name},<br> <br> That is a first sketch for the cover of the future reports .<br> The Pdf attached and the email have been created via a script in Python to simulate the report creation :) <br> regards,<br><br> Giulia"
                )
msg.attach(MIMEText(emailcontent, _subtype='html'))

# Attach a file

mail_file = MIMEBase('application', 'pdf')
mail_file.set_payload(open('Pilot Element ' +start_pv.strftime(' %B %Y ')+' Performance Overview.pdf', 'rb').read())
mail_file.add_header('Content-Disposition', 'attachment', filename='Pilot Element ' +start_pv.strftime(' %B %Y ')+' Performance Overview.pdf')
Encoders.encode_base64(mail_file)
msg.attach(mail_file)
   
email_from = "martini.giulia94@gmail.com"
email_to1 = "martini.giulia94@gmail.com"

email_subject = 'New report cover'
smtp_server = 'smtp.gmail.com'
smtp_port = 587  
smtp_username = "martini.giulia94@gmail.com"
smtp_password = "Birmania1994"

server = smtplib.SMTP(smtp_server, smtp_port)
server.starttls()
server.login(smtp_username, smtp_password)

msg["From"] = email_from
msg["Subject"] = email_subject
msg["To"] = email_to1

server.sendmail(email_from, email_to1, msg.as_string())

print('Job complete')