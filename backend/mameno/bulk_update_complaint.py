import pandas as pd
import mysql.connector
from datetime import date

mydb = mysql.connector.connect(
  host="mameno.mysql.pythonanywhere-services.com",
  user="mameno",
  password="mysqlmtf2021",
  database="mameno$default"
)
mycursor = mydb.cursor()

df=pd.read_excel('Complaint Agus-Sept awal.xlsx',sheet_name='Sheet1', engine='openpyxl')
df=df[df['No Kontrak'].notnull()]

# print(len(df))
# print(df.columns)
# print(df.head(5))
i=0
while i < len(df):
    # print(str(int(float(str(df.iloc[i,:]['No Kontrak'])))))
    # sql = "INSERT INTO dbsppi (nip,nama,reg,cabang,jabatan,predikat,status,act_date,exp_date,next_date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    # val = (str(df.iloc[i]['Employee Id']), str(df.iloc[i]['Employee Name']),str(df.iloc[i]['Divisi / Regional']),df.iloc[i]['Work Location'],df.iloc[i]['Position Name'],df.iloc[i]['Predikat'],df.iloc[i]['Status'],df.iloc[i]['Tanggal Pelaksanaan'],df.iloc[i]['Expired Date'],df.iloc[i]['Jadwal Sertifikasi Berikutnya'])
    sql = "INSERT INTO dbcomp (no_agr,nama,area_cg,cg_name,class_comp,agent_notes,input_date,status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    val = (str(int(float(str(df.iloc[i,:]['No Kontrak'])))), str(df.iloc[i]['Nama']),str(df.iloc[i]['Area CG']),str(df.iloc[i]['Nama CG']),str(df.iloc[i]['Complaint']),str(df.iloc[i]['Notes']),str(date.today()),'New')
    # print(sql)
    print(df.iloc[i,:]['No Kontrak'])

    mycursor.execute(sql, val)
    # print(df.iloc[i]['No Kontrak'])
    i+=1

mydb.commit()

print(mycursor.rowcount, "record inserted.")