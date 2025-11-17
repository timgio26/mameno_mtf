import requests
from sqlalchemy import create_engine
import pandas as pd
from datetime import date,timedelta

def send_simple_message():
    html="""<html>
                <head>
                </head>
                <body>
                    <p> Berikut Nama yang akan expired izin nya : </p>"""
    tbl1=df.to_html(classes='wide', escape=False,index=True)
    html=html+tbl1
    html_end="""</body></html>"""
    html=html+html_end

    return requests.post(
        "https://api.mailgun.net/v3/sandboxb904dd6d2fe54ad880b7d398a60e4166.mailgun.org/messages",
        auth=("api", "1fb9d96ee836cb0a2c15b8c3ca443412-100b5c8d-f92aee71"),
        data={"from": "AR APP MTF <mailgun@sandboxb904dd6d2fe54ad880b7d398a60e4166.mailgun.org>",
              "to": ['kamiarmtf2021@gmail.com','t.gio.andi@gmail.com','raymyas@gmail.com'],
              "subject": "Report SPPI {}".format(date.today()),
              "html": html})




SQLALCHEMY_DATABASE_URI="mysql+mysqlconnector://mameno:mysqlmtf2021@mameno.mysql.pythonanywhere-services.com/mameno$default"
cnx = create_engine(SQLALCHEMY_DATABASE_URI)
df=pd.read_sql_table('dbsppi', con=cnx)
# df=df[df['exp_date']>'2023-01-01']
df=df[(df['exp_date']<=str(date.today()+timedelta(30)))&~(df['next_date']>=str(date.today()))].reset_index(drop=True)

if date.today().day==1:
    if df.size>0:
        send_simple_message()
        print('done {}'.format(date.today()))
    else:
        print('no exp account')
else:
    print('bukan tanggal 1')
