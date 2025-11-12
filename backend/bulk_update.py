import pandas as pd
import mysql.connector

mydb = mysql.connector.connect(
  host="mameno.mysql.pythonanywhere-services.com",
  user="mameno",
  password="mysqlmtf2021",
  database="mameno$default"
)
mycursor = mydb.cursor()

df=pd.read_excel('Data Sertifikasi Penagihan (to AR Management) - 30 April 2022.xlsx',sheet_name='Sheet2', engine='openpyxl')

print(len(df))
i=1
while i < len(df):
    # sql = "INSERT INTO dbsppi (nip,nama,reg,cabang,jabatan,predikat,status,act_date,exp_date,next_date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    # val = (str(df.iloc[i]['Employee Id']), str(df.iloc[i]['Employee Name']),str(df.iloc[i]['Divisi / Regional']),df.iloc[i]['Work Location'],df.iloc[i]['Position Name'],df.iloc[i]['Predikat'],df.iloc[i]['Status'],df.iloc[i]['Tanggal Pelaksanaan'],df.iloc[i]['Expired Date'],df.iloc[i]['Jadwal Sertifikasi Berikutnya'])
    sql = "INSERT INTO dbsppi (nip,nama,reg,cabang,jabatan,predikat,status,act_date,exp_date,next_date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    val = (str(df.iloc[i]['Employee Id']), str(df.iloc[i]['Employee Name']),str(df.iloc[i]['Divisi / Regional']),str(df.iloc[i]['Work Location']),str(df.iloc[i]['Position Name']),str(df.iloc[i]['Predikat']),str(df.iloc[i]['Status']),str(df.iloc[i]['Tanggal Pelaksanaan']),str(df.iloc[i]['Expired Date']),str(df.iloc[i]['Jadwal Sertifikasi Berikutnya']))


    mycursor.execute(sql, val)
    print(df.iloc[i]['Employee Id'])
    i+=1

mydb.commit()

print(mycursor.rowcount, "record inserted.")