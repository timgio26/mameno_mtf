from flask import Flask,render_template,url_for,redirect,make_response,session,request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func,desc,create_engine,asc
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from flask_migrate import Migrate
from wtforms import StringField,SubmitField,SelectField,PasswordField
from wtforms.validators import DataRequired,Optional
from wtforms.fields import DateField,IntegerField
# import os
from datetime import datetime,date,timedelta
from flask_restful import Resource,Api
import pandas as pd
import json,plotly
import plotly.express as px


app = Flask(__name__)
app.config.from_pyfile('config.py')
db = SQLAlchemy(app)
Migrate(app,db)
bootstrap = Bootstrap(app)
api=Api(app)

class tbl_nota(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    penulis_nota=db.Column(db.Text)
    judul_nota=db.Column(db.Text)
    tanggal_buat=db.Column(db.Date)
    tahun_nota=db.Column(db.Integer)
    no=db.Column(db.Integer)
    no_nota=db.Column(db.Text)
    linknota=db.Column(db.Text)

class tbl_memo(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    penulis_memo=db.Column(db.Text)
    judul_memo=db.Column(db.Text)
    tanggal_buat=db.Column(db.Date)
    tahun_memo=db.Column(db.Integer)
    no=db.Column(db.Integer)
    no_memo=db.Column(db.Text)
    linkmemo=db.Column(db.Text)

class tbl_beli(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    penulis_beli=db.Column(db.Text)
    judul_beli=db.Column(db.Text)
    tanggal_buat=db.Column(db.Date)
    tahun_beli=db.Column(db.Integer)
    no=db.Column(db.Integer)
    no_beli=db.Column(db.Text)
    linkbeli=db.Column(db.Text)

class alluser(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    username=db.Column(db.String(20),unique=True)
    nama=db.Column(db.Text)
    password=db.Column(db.String(20))

class dbsppi(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    nip=db.Column(db.String(10))
    nama=db.Column(db.String(30))
    reg=db.Column(db.String(20))
    cabang=db.Column(db.String(30))
    jabatan=db.Column(db.String(20))
    predikat=db.Column(db.String(20))
    status=db.Column(db.String(20))
    act_date=db.Column(db.Date)
    next_date=db.Column(db.Date)
    # next_date_str=db.Column(db.String(20))
    exp_date=db.Column(db.Date)

class dbcomp(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    no_agr=db.Column(db.String(20),unique=True)
    nama=db.Column(db.String(20))
    area_cg=db.Column(db.String(20))
    cg_name=db.Column(db.String(20))
    class_comp=db.Column(db.String(20))
    agent_notes=db.Column(db.Text)
    input_date=db.Column(db.Date)
    status=db.Column(db.String(20))
    last_update_date=db.Column(db.Date)

class dbfucomp(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    idcomp=db.Column(db.Integer)
    fupic=db.Column(db.String(25))
    fudate=db.Column(db.Date)
    notes=db.Column(db.Text)
    status=db.Column(db.String(20))

class upsppiapi(Resource):
    def post(self,inp_nip,inp_nama):
        newdata=dbsppi(nip=inp_nip,nama=inp_nama)
        db.session.add(newdata)
        db.session.commit()

api.add_resource(upsppiapi,'/api/<inp_nip>/<inp_nama>')


class fucompform(FlaskForm):
    fudate=DateField('Follow Up date:',validators=[DataRequired()])
    notes=StringField('Notes:',validators=[DataRequired()])
    status=SelectField('Status:',choices=['On Progress','Closed'],validators=[DataRequired()])
    submit=SubmitField('Enter')

class formsppi(FlaskForm):
    nip=StringField('NIP:',validators=[DataRequired()])
    nama=StringField('Nama:',validators=[DataRequired()])
    reg=SelectField('Regional/Divisi:',choices=['Regional 1','Regional 2','Regional 3','Regional 4','Regional 5', 'Regional 6', 'Regional 7', 'Regional 8', 'Regional 9', 'Fleet AR Management'],validators=[DataRequired()])
    cabang=StringField('Work Location:',validators=[DataRequired()])
    jabatan=SelectField('Jabatan:',choices=['AMO','ARMO','AR Head','Remedial Head','SAM Head','Recovery Head'],validators=[DataRequired()])
    predikat=SelectField('Predikat:',choices=['Lulus','Tidak Lulus','Belum Ada Hasil','Belum Sertifikasi'],validators=[DataRequired()])
    status=SelectField('Status:',choices=['Active','Expired','Tidak Lulus','Belum Sertifikasi'],validators=[DataRequired()])
    act_date=DateField('Tanggal Pelaksanaan:',validators=[Optional()])
    exp_date=DateField('Exp Date:',validators=[DataRequired()])
    # next_date=StringField('Jadwal Sertifikasi Berikutnya:')
    next_date=DateField('Jadwal Sertifikasi Berikutnya:',validators=[Optional()])
    submit=SubmitField('Enter')

class editsppi(formsppi):
    submit=SubmitField('Edit')

class editfu(fucompform):
    submit=SubmitField('Edit')

class compform(FlaskForm):
    no_agr=StringField('No Agreement:',validators=[DataRequired()])
    nama=StringField('Nama:',validators=[DataRequired()])
    area_cg=SelectField('Area CG:',choices=['Area 1','Area 2','Area 3','Area 4','Area 5','Area 6','Area 7','Area 8','Area 9'],validators=[DataRequired()])
    cg_name=StringField('CG Name:',validators=[DataRequired()])
    class_comp=StringField('Complaint:',validators=[DataRequired()])
    agent_notes=StringField('Agent Notes:',validators=[DataRequired()])
    status=SelectField('Status:',choices=['New','On Progress','Closed'],validators=[DataRequired()])
    submit=SubmitField('Tambah')

class editcomp(compform):
    submit=SubmitField('Edit')

class delcomp(FlaskForm):
    submit=SubmitField('Hapus')

class tambah_baru(FlaskForm):
    # penulis_memo=StringField('Penulis Surat:')
    dropdown_list = ['Nota','Memo','Form Pembelian','Nota Bersama']
    type=SelectField('Jenis:',choices=dropdown_list,validators=[DataRequired()])
    judul=StringField('Judul Memo/Nota:',validators=[DataRequired()])
    # tanggal_memo=DateField('Tanggal Surat:', format='%Y-%m-%d')
    submit=SubmitField('Tambah')

class formupdate(FlaskForm):
    # penulis_memo=StringField('Penulis Surat:')
    pic=StringField('PIC:',validators=[DataRequired()])
    judul=StringField('Judul Memo/Nota:',validators=[DataRequired()])
    url=StringField('URL:')
    tgl_update=DateField('Tanggal Surat:', format='%Y-%m-%d')
    no=StringField('No Memo/nota:',validators=[DataRequired()])
    submit=SubmitField('Update')

class tambah_historis(FlaskForm):
    dropdown_list = ['Nota','Memo','Form Pembelian']
    type=SelectField('Jenis:',choices=dropdown_list,validators=[DataRequired()])
    pic=StringField('PIC:',validators=[DataRequired()])
    judul=StringField('Judul:',validators=[DataRequired()])
    nomor=IntegerField('No:')
    tanggal=DateField('Tanggal Surat:', format='%Y-%m-%d',validators=[DataRequired()])
    submit=SubmitField('Tambah')

class filterform(FlaskForm):
    filterjudul=StringField('Judul:')
    filtertahun=IntegerField('Tahun:')
    submit=SubmitField('Cari !')

class signup_form(FlaskForm):
    username=StringField('New Username:',validators=[DataRequired()])
    nama=StringField('Nama Lengkap:',validators=[DataRequired()])
    password=PasswordField('New Password:',validators=[DataRequired()])
    submit=SubmitField('Daftar')

class login_form(FlaskForm):
    username=StringField('Username:',validators=[DataRequired()])
    password=PasswordField('Password:',validators=[DataRequired()])
    submit=SubmitField('Masuk')


@app.route('/',methods=['GET', 'POST'])
def portal():
    return render_template('home2.html')


@app.route('/mameno',methods=['GET', 'POST'])
def index():
    return render_template('home.html')

@app.route('/complaint',methods=['GET', 'POST'])
def complaint():
    if session.get('user',None):
        form=compform()
        df=dbcomp.query.all()
        # df=db.session.query(dbcomp,dbfucomp).join(dbfucomp,dbcomp.id==dbfucomp.idcomp).all()
        nnew=dbcomp.query.filter_by(status='New').count()
        nprogress=dbcomp.query.filter_by(status='On Progress').count()
        nclossed=dbcomp.query.filter_by(status='Closed').count()
        res=[nnew,nprogress,nclossed]
        if form.validate_on_submit():
            exist_comp=dbcomp.query.filter_by(no_agr=form.no_agr.data).first()
            if exist_comp==None:
                newcomp=dbcomp(no_agr=form.no_agr.data,nama=form.nama.data,area_cg=form.area_cg.data,cg_name=form.cg_name.data,class_comp=form.class_comp.data,agent_notes=form.agent_notes.data,input_date=date.today(),status='New')
                db.session.add(newcomp)
                db.session.commit()
                return redirect(url_for('complaint'))
            else :
                return render_template('complaint.html',form=form,df=df,res=res,msg="Error :  Nomor Kontrak Sudah Ada")
        return render_template('complaint.html',form=form,df=df,res=res)
    else:
        return redirect(url_for('masuk'))

@app.route('/complaintnew',methods=['GET','POST'])
def complaintnew():
    df1=dbcomp.query.filter_by(status='New').all()
    return render_template('new_comp.html',df=df1)

@app.route('/complaintop',methods=['GET','POST'])
def complaintop():
    df1=dbcomp.query.filter_by(status='On Progress').all()
    return render_template('op_comp.html',df=df1)

@app.route('/dashclosed',methods=['GET','POST'])
def dashclosed():
    df1=dbcomp.query.filter_by(status='Closed').all()
    return render_template("dashclosed.html",df=df1)

@app.route('/dashboard',methods=['GET','POST'])
def dashboard():
    df=pd.read_sql_table('dbfucomp', app.config['SQLALCHEMY_DATABASE_URI'])
    df["MY"]=df['fudate'].dt.strftime('%Y-%m')
    res=df[df['status']=='Closed'].groupby("MY")[["idcomp"]].nunique().reset_index()
    print(res)
    fig = px.bar(res, x='MY', y='idcomp',labels={'MY':'Tanggal','idcomp':'Jumlah Complaint Closed'})

    fig.update_xaxes(dtick="M1", tickformat="%b %Y")
    fig.update_yaxes(dtick=1)
    fig.update_layout(width=500)
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    df=pd.read_sql_table('dbcomp', app.config['SQLALCHEMY_DATABASE_URI'])
    res=df.groupby("status")[["id"]].nunique().reset_index()
    fig = px.pie(res, values='id', names='status')
    fig.update_layout(width=400)
    graphJSON2 = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    df=pd.read_sql_table('dbcomp', app.config['SQLALCHEMY_DATABASE_URI'])
    res=df[df['status']=='On Progress'].groupby("area_cg")[["id"]].nunique().reset_index()
    fig = px.bar(res, y='area_cg', x='id', orientation='h',labels={'area_cg':'Area CG','id':'Jumlah No Kontrak'})
    fig.update_layout(width=500)
    graphJSON3 = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    print(df[df['area_cg']=='area 3'])

    return render_template("dashboard.html",graphJSON=graphJSON,graphJSON2=graphJSON2,graphJSON3=graphJSON3)


@app.route('/editcomplaint<cid>',methods=['GET','POST'])
def editcomplaint(cid):
    form=editcomp()
    comp=dbcomp.query.get(cid)
    if request.method == 'GET':
        form.no_agr.data = comp.no_agr
        form.nama.data = comp.nama
        form.area_cg.data = comp.area_cg
        form.cg_name.data = comp.cg_name
        form.class_comp.data = comp.class_comp
        form.agent_notes.data = comp.agent_notes
        form.status.data = comp.status
    if form.validate_on_submit():
        comp.no_agr=form.no_agr.data
        comp.nama=form.nama.data
        comp.area_cg=form.area_cg.data
        comp.cg_name=form.cg_name.data
        comp.class_comp=form.class_comp.data
        comp.agent_notes=form.agent_notes.data
        comp.status=form.status.data
        db.session.add(comp)
        db.session.commit()
        return redirect(url_for('complaint'))
    return render_template('editcomp.html',comp=comp,form=form)

@app.route('/fucomp<cid>',methods=['GET','POST'])
def fucomp(cid):
    form=fucompform()
    comp=dbcomp.query.get(cid)
    df=dbfucomp.query.filter_by(idcomp=cid).all()

    print(db.session.query(func.max(dbfucomp.fudate)).filter_by(idcomp=cid).scalar())
    last_update=db.session.query(func.max(dbfucomp.fudate)).filter_by(idcomp=cid).scalar()
    # df_pandas=pd.read_sql_table('dbfucomp', SQLALCHEMY_DATABASE_URI)
    # last_update=df_pandas[df_pandas['idcomp']==cid]['fudate'].max()
    comp.last_update_date=last_update
    db.session.add(comp)
    db.session.commit()



    if form.validate_on_submit():
        newfu=dbfucomp(idcomp=cid,fudate=form.fudate.data,fupic=session['user'],notes=form.notes.data,status=form.status.data)
        db.session.add(newfu)
        db.session.commit()

        comp.status=form.status.data
        db.session.add(comp)
        db.session.commit()
        return redirect(url_for('fucomp',cid=cid))
    return render_template('fucomp.html',form=form,df=df,comp=comp)

@app.route('/editfucomp<fid>',methods=['GET','POST'])
def editfucomp(fid):
    form=editfu()
    fu=dbfucomp.query.get(fid)
    if request.method == 'GET':
        form.fudate.data=fu.fudate
        form.notes.data=fu.notes
        form.status.data=fu.status
    if form.validate_on_submit():
        fu.fudate=form.fudate.data
        fu.notes=form.notes.data
        fu.status=form.status.data
        db.session.add(fu)
        db.session.commit()
        return redirect(url_for('fucomp',cid=fu.idcomp))
    return render_template('editfucomp.html',form=form)

@app.route('/delfu<fid>',methods=['GET','POST'])
def delfu(fid):
    fu=dbfucomp.query.get(fid)
    print (fu)
    cid=fu.idcomp
    db.session.delete(fu)
    db.session.commit()
    return redirect(url_for('fucomp',cid=cid))

@app.route('/delcomplaint<cid>',methods=['GET','POST'])
def delcomplaint(cid):
    form=delcomp()
    comp=dbcomp.query.get(cid)
    if form.validate_on_submit():
        fu=dbfucomp.query.filter_by(idcomp=cid).all()
        for i in fu:
            db.session.delete(i)
            db.session.commit()
        db.session.delete(comp)
        db.session.commit()
        return redirect(url_for('complaint'))
    return render_template('delcomp.html',form=form,comp=comp)

@app.route('/sppi',methods=['GET','POST'])
def sppi():
    if session.get('user',None):
        form=formsppi()
        df=dbsppi.query.all()
        if form.validate_on_submit():
            newdata=dbsppi(nip=form.nip.data,nama=form.nama.data,reg=form.reg.data,cabang=form.cabang.data,jabatan=form.jabatan.data,predikat=form.predikat.data,status=form.status.data,act_date=form.act_date.data,exp_date=form.exp_date.data,next_date=form.next_date.data)
            db.session.add(newdata)
            db.session.commit()
            return redirect(url_for('sppi'))
        return render_template('sppi.html',form=form,df=df)
    else:
        return redirect(url_for('masuk'))

@app.route('/sppi_exp',methods=['GET','POST'])
def sppi_exp():
    df=dbsppi.query.filter(dbsppi.exp_date<=date.today()+timedelta(30),dbsppi.next_date<=date.today()).all()
    return render_template('sppi_exp.html',df=df)

@app.route('/sppiedit/<id>',methods=['GET','POST'])
def sppiedit(id):
    form=editsppi()
    sppi=dbsppi.query.get(id)
    if request.method == 'GET':
        form.nip.data=sppi.nip
        form.nama.data=sppi.nama
        form.jabatan.data=sppi.jabatan
        form.reg.data=sppi.reg
        form.cabang.data=sppi.cabang
        form.jabatan.data=sppi.jabatan
        form.predikat.data=sppi.predikat
        form.status.data=sppi.status
        form.act_date.data=sppi.act_date
        form.next_date.data=sppi.next_date
        form.exp_date.data=sppi.exp_date
    if form.validate_on_submit():
        sppi.nip=form.nip.data
        sppi.nama=form.nama.data
        sppi.jabatan=form.jabatan.data
        sppi.reg=form.reg.data
        sppi.cabang=form.cabang.data
        sppi.jabatan=form.jabatan.data
        sppi.predikat=form.predikat.data
        sppi.status=form.status.data
        sppi.act_date=form.act_date.data
        sppi.next_date=form.next_date.data
        sppi.exp_date=form.exp_date.data
        db.session.add(sppi)
        db.session.commit()
        return redirect(url_for('sppi'))
    return render_template('sppiedit.html',form=form)

@app.route('/delsppi/<id>',methods=['GET','POST'])
def delsppi(id):
    deldata=dbsppi.query.get(id)
    db.session.delete(deldata)
    db.session.commit()
    return redirect(url_for('sppi'))


@app.route('/tambah_all',methods=['GET', 'POST'])
def tambah_all():
    if session.get('user',None):
        form=tambah_baru()
        if form.validate_on_submit():
            if (form.type.data=="Nota"):
                now=date.today()
                if (now.month == 1):
                    mr="I"
                elif (now.month == 2):
                    mr="II"
                elif (now.month == 3):
                    mr="III"
                elif (now.month == 4):
                    mr="IV"
                elif (now.month == 5):
                    mr="V"
                elif (now.month == 6):
                    mr="VI"
                elif (now.month == 7):
                    mr="VII"
                elif (now.month == 8):
                    mr="VIII"
                elif (now.month == 9):
                    mr="IX"
                elif (now.month == 10):
                    mr="X"
                elif (now.month == 11):
                    mr="XI"
                else:
                    mr="XII"

                max = db.session.query(func.max(tbl_nota.no)).filter_by(tahun_nota=now.year).scalar()
                if(max == None):
                    no=1
                else:
                    no=max+1

                if len(str(no))==1:
                    adj="00"
                elif len(str(no))==2:
                    adj="0"
                else:
                    adj=""

                no_nota=f"{adj}{no}/Nota-ARM/MTF/{mr}/{now.year}"
                newnota=tbl_nota(penulis_nota=session['namauser'],judul_nota=form.judul.data,tanggal_buat=now,tahun_nota=now.year,no=no,no_nota=no_nota)
                db.session.add(newnota)
                db.session.commit()
                return redirect(url_for('result',type='nota',id=newnota.id))
            elif(form.type.data=="Form Pembelian"):
                
                now=date.today()
                if (now.month == 1):
                    mr="I"
                elif (now.month == 2):
                    mr="II"
                elif (now.month == 3):
                    mr="III"
                elif (now.month == 4):
                    mr="IV"
                elif (now.month == 5):
                    mr="V"
                elif (now.month == 6):
                    mr="VI"
                elif (now.month == 7):
                    mr="VII"
                elif (now.month == 8):
                    mr="VIII"
                elif (now.month == 9):
                    mr="IX"
                elif (now.month == 10):
                    mr="X"
                elif (now.month == 11):
                    mr="XI"
                else:
                    mr="XII"

                max = db.session.query(func.max(tbl_beli.no)).filter_by(tahun_beli=now.year).scalar()
                if(max == None):
                    no=1
                else:
                    no=max+1

                if len(str(no))==1:
                    adj="00"
                elif len(str(no))==2:
                    adj="0"
                else:
                    adj=""

                no_beli=f"{adj}{no}/FPPA-ARM/MTF/{mr}/{now.year}"
                newbeli=tbl_beli(penulis_beli=session['namauser'],judul_beli=form.judul.data,tanggal_buat=now,tahun_beli=now.year,no=no,no_beli=no_beli)
                db.session.add(newbeli)
                db.session.commit()
                return redirect(url_for('result',type='beli',id=newbeli.id))


            else:
                now=date.today()
                # newmemo=tbl_memo(penulis_memo=session['namauser'],judul_memo=form.judul.data,tanggal_buat=now,tahun_memo=now.year)
                # db.session.add(newmemo)
                # db.session.commit()
                if (now.month == 1):
                    mr="I"
                elif (now.month == 2):
                    mr="II"
                elif (now.month == 3):
                    mr="III"
                elif (now.month == 4):
                    mr="IV"
                elif (now.month == 5):
                    mr="V"
                elif (now.month == 6):
                    mr="VI"
                elif (now.month == 7):
                    mr="VII"
                elif (now.month == 8):
                    mr="VIII"
                elif (now.month == 9):
                    mr="IX"
                elif (now.month == 10):
                    mr="X"
                elif (now.month == 11):
                    mr="XI"
                else:
                    mr="XII"
                # newmemo=tbl_memo.query.get(newmemo.id)
                max = db.session.query(func.max(tbl_memo.no)).filter_by(tahun_memo=now.year).scalar()
                if(max == None):
                    no=1
                else:
                    no=max+1
                if len(str(no))==1:
                    adj="00"
                elif len(str(no))==2:
                    adj="0"
                else:
                    adj=""
                no_memo=f"{adj}{no}/Memo-ARM/MTF/{mr}/{now.year}"
                # newmemo.no_memo=no_memo
                # print(now.date)
                newmemo=tbl_memo(penulis_memo=session['namauser'],judul_memo=form.judul.data,tanggal_buat=now,tahun_memo=now.year,no=no,no_memo=no_memo)
                db.session.add(newmemo)
                db.session.commit()
                return redirect(url_for('result',type="memo",id=newmemo.id))
        else:
            return render_template('tambah_all.html',form=form)
    else:
        return redirect(url_for('masuk'))

@app.route('/result/<type>/<id>',methods=['GET','POST'])
def result(type,id):
    if type=='memo':
        x=tbl_memo.query.get(id)
    elif type=='beli':
        x=tbl_beli.query.get(id)
    else:
        x=tbl_nota.query.get(id)
    return render_template('result.html',x=x)

@app.route('/list_nota',methods=['GET','POST'])
def list_nota():
    form=filterform()
    if session.get('user',None):
        if form.validate_on_submit():
            session['src_tahun']=form.filtertahun.data
            df=tbl_nota.query.order_by(asc(tbl_nota.no)).filter_by(tahun_nota=form.filtertahun.data).filter(tbl_nota.judul_nota.contains(form.filterjudul.data)).all()
            return render_template ('list_nota.html',form=form,df=df,year=form.filtertahun.data)
        else:
            if session.get('src_tahun',None):
                year=session['src_tahun']
            else:
                year=datetime.now().year
            df=tbl_nota.query.order_by(asc(tbl_nota.no)).filter_by(tahun_nota=year).all()
            return  render_template ("list_nota.html",df=df,form=form,year=year)
    else:
        return redirect(url_for('masuk'))

@app.route('/delnota/<id>',methods=['GET', 'POST'])
def delnota(id):
    delnota=tbl_nota.query.get(id)
    db.session.delete(delnota)
    db.session.commit()
    return redirect(url_for('list_nota'))

@app.route('/delbeli/<id>',methods=['GET', 'POST'])
def delbeli(id):
    delitem=tbl_beli.query.get(id)
    db.session.delete(delitem)
    db.session.commit()
    return redirect(url_for('list_beli'))

@app.route('/updatenota/<id>',methods=['GET', 'POST'])
def updatenota(id):
    form=formupdate()
    upnota=tbl_nota.query.get(id)
    if form.validate_on_submit():
        upnota.linknota=form.url.data
        upnota.penulis_nota=form.pic.data
        upnota.judul_nota=form.judul.data
        upnota.no_nota=form.no.data
        upnota.tanggal_buat=form.tgl_update.data
        db.session.add(upnota)
        db.session.commit()
        return redirect(url_for('list_nota'))
    else:
        return render_template('update.html',x=upnota,form=form)
    
@app.route('/updatefbeli/<id>',methods=['GET', 'POST'])
def updatefbeli(id):
    form=formupdate()
    upmemo=tbl_beli.query.get(id)
    if form.validate_on_submit():
        upmemo.linkbeli=form.url.data
        upmemo.penulis_beli=form.pic.data
        upmemo.judul_beli=form.judul.data
        upmemo.no_beli=form.no.data
        upmemo.tanggal_buat=form.tgl_update.data
        db.session.add(upmemo)
        db.session.commit()
        return redirect(url_for('list_beli'))
    else:
        return render_template('update.html',x=upmemo,form=form)

@app.route('/list_memo',methods=['GET','POST'])
def list_memo():
    form=filterform()
    if session.get('user',None):
        if form.validate_on_submit():
            session['src_tahun']=form.filtertahun.data
            df=tbl_memo.query.order_by(asc(tbl_memo.no)).filter_by(tahun_memo=form.filtertahun.data).filter(tbl_memo.judul_memo.contains(form.filterjudul.data)).all()
            return  render_template ("list_memo.html",df=df,form=form,year=form.filtertahun.data)
        else:
            if session.get('src_tahun',None):
                year=session['src_tahun']
            else:
                year=datetime.now().year
            df=tbl_memo.query.order_by(asc(tbl_memo.no)).filter_by(tahun_memo=year).all()
            return  render_template ("list_memo.html",df=df,form=form,year=year)
    else:
        return redirect(url_for('masuk'))
    
@app.route('/list_beli',methods=['GET','POST'])
def list_beli():

    if session.get('user',None):

        df=tbl_beli.query.all()
        return  render_template ("list_beli.html",df=df)
    else:
        return redirect(url_for('masuk'))

@app.route('/delmemo/<id>',methods=['GET', 'POST'])
def delmemo(id):
    delmemo=tbl_memo.query.get(id)
    db.session.delete(delmemo)
    db.session.commit()
    return redirect(url_for('list_memo'))

@app.route('/updatememo/<id>',methods=['GET', 'POST'])
def updatememo(id):
    form=formupdate()
    upmemo=tbl_memo.query.get(id)
    if form.validate_on_submit():
        upmemo.linkmemo=form.url.data
        upmemo.penulis_memo=form.pic.data
        upmemo.judul_memo=form.judul.data
        upmemo.no_memo=form.no.data
        upmemo.tanggal_buat=form.tgl_update.data
        db.session.add(upmemo)
        db.session.commit()
        return redirect(url_for('list_memo'))
    else:
        return render_template('update.html',x=upmemo,form=form)

@app.route('/tambah_historis',methods=['GET', 'POST'])
def th():
    form=tambah_historis()
    if (session['user']=='admin'):
        if form.validate_on_submit():
            if(form.type.data=="Memo"):
                tgl=form.tanggal.data
                now=form.tanggal.data

                # db.session.add(newmemo)
                # db.session.commit()
                if (now.month == 1):
                    mr="I"
                elif (now.month == 2):
                    mr="II"
                elif (now.month == 3):
                    mr="III"
                elif (now.month == 4):
                    mr="IV"
                elif (now.month == 5):
                    mr="V"
                elif (now.month == 6):
                    mr="VI"
                elif (now.month == 7):
                    mr="VII"
                elif (now.month == 8):
                    mr="VIII"
                elif (now.month == 9):
                    mr="IX"
                elif (now.month == 10):
                    mr="X"
                elif (now.month == 11):
                    mr="XI"
                else:
                    mr="XII"
                # newmemo=tbl_memo.query.get(newmemo.id)
                if form.nomor.data:
                    no=form.nomor.data
                else:
                    max = db.session.query(func.max(tbl_memo.no)).filter_by(tahun_memo=tgl.year).scalar()
                    if(max == None):
                        no=1
                    else:
                        no=max+1
                if len(str(no))==1:
                    adj="00"
                elif len(str(no))==2:
                    adj="0"
                else:
                    adj=""
                no_memo=f"{adj}{no}/Memo-ARM/MTF/{mr}/{tgl.year}"

                newmemo=tbl_memo(penulis_memo=form.pic.data,judul_memo=form.judul.data,tanggal_buat=form.tanggal.data,tahun_memo=tgl.year,no=no,no_memo=no_memo)
                db.session.add(newmemo)
                db.session.commit()
                return redirect(url_for('result',type="memo",id=newmemo.id))
            elif(form.type.data=="Form Pembelian"):
                tgl=form.tanggal.data
                now=form.tanggal.data

                # db.session.add(newmemo)
                # db.session.commit()
                if (now.month == 1):
                    mr="I"
                elif (now.month == 2):
                    mr="II"
                elif (now.month == 3):
                    mr="III"
                elif (now.month == 4):
                    mr="IV"
                elif (now.month == 5):
                    mr="V"
                elif (now.month == 6):
                    mr="VI"
                elif (now.month == 7):
                    mr="VII"
                elif (now.month == 8):
                    mr="VIII"
                elif (now.month == 9):
                    mr="IX"
                elif (now.month == 10):
                    mr="X"
                elif (now.month == 11):
                    mr="XI"
                else:
                    mr="XII"
                # newmemo=tbl_memo.query.get(newmemo.id)
                if form.nomor.data:
                    no=form.nomor.data
                else:
                    max = db.session.query(func.max(tbl_beli.no)).filter_by(tahun_beli=tgl.year).scalar()
                    if(max == None):
                        no=1
                    else:
                        no=max+1
                if len(str(no))==1:
                    adj="00"
                elif len(str(no))==2:
                    adj="0"
                else:
                    adj=""
                no_memo=f"{adj}{no}/FPPA-ARM/MTF/{mr}/{tgl.year}"

                newitem=tbl_beli(penulis_beli=form.pic.data,judul_beli=form.judul.data,tanggal_buat=form.tanggal.data,tahun_beli=tgl.year,no=no,no_beli=no_memo)
                db.session.add(newitem)
                db.session.commit()
                return redirect(url_for('result',type="beli",id=newitem.id))
            else:
                tgl=form.tanggal.data
                now=form.tanggal.data

                # db.session.add(newnota)
                # db.session.commit()
                if (now.month == 1):
                    mr="I"
                elif (now.month == 2):
                    mr="II"
                elif (now.month == 3):
                    mr="III"
                elif (now.month == 4):
                    mr="IV"
                elif (now.month == 5):
                    mr="V"
                elif (now.month == 6):
                    mr="VI"
                elif (now.month == 7):
                    mr="VII"
                elif (now.month == 8):
                    mr="VIII"
                elif (now.month == 9):
                    mr="IX"
                elif (now.month == 10):
                    mr="X"
                elif (now.month == 11):
                    mr="XI"
                else:
                    mr="XII"
                # newnota=tbl_nota.query.get(newnota.id)
                if form.nomor.data:
                    no=form.nomor.data
                else:
                    max = db.session.query(func.max(tbl_nota.no)).filter_by(tahun_nota=tgl.year).scalar()
                    if(max == None):
                        no=1
                    else:
                        no=max+1
                if len(str(no))==1:
                    adj="00"
                elif len(str(no))==2:
                    adj="0"
                else:
                    adj=""
                no_nota=f"{adj}{no}/Nota-ARM/MTF/{mr}/{tgl.year}"
                newnota=tbl_nota(penulis_nota=form.pic.data,judul_nota=form.judul.data,tanggal_buat=form.tanggal.data,tahun_nota=tgl.year,no=no,no_nota=no_nota)
                db.session.add(newnota)
                db.session.commit()
                return redirect(url_for('result',type='nota',id=newnota.id))
        else:
            return render_template("tambah_historis.html",form=form)
    else:
        return redirect(url_for('index'))

@app.route('/masuk',methods=['GET', 'POST'])
def masuk():
    form=login_form()
    if form.validate_on_submit():
        entry=alluser.query.filter_by(username=form.username.data).first()
        if entry==None:
            return render_template('login.html',form=form,msg='username/password salah')
        else:
            if entry.password==form.password.data:
                session['user']=entry.username
                session['namauser']=entry.nama
                return redirect(url_for('portal'))
            else:
                return render_template('login.html',form=form,msg='username/password salah')
    else:
        return render_template('login.html',form=form)

@app.route('/daftar',methods=['GET', 'POST'])
def daftar():
    form=signup_form()
    session['user']=None
    if form.validate_on_submit():
        userbaru=alluser(username=form.username.data,nama=form.nama.data,password=form.password.data)
        db.session.add(userbaru)
        db.session.commit()
        return redirect(url_for('masuk'))
    else:
        return render_template('signup.html',form=form)

@app.route('/download/<type>',methods=['GET', 'POST'])
def download(type):
    cnx = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
    if type=='nota':
        df=pd.read_sql_table('tbl_nota', con=cnx)
    elif type=='telecol':
        df=pd.read_sql_table('dbcomp', con=cnx)
        df2=pd.read_sql_table('dbfucomp', con=cnx)
        df=df.merge(df2,how='left',left_on='id',right_on='idcomp')
    elif type=='sppi':
        df=pd.read_sql_table('dbsppi', con=cnx)
    else:
        df=pd.read_sql_table('tbl_memo', con=cnx)
    resp = make_response(df.to_csv(index=False))
    resp.headers["Content-Disposition"] = f"attachment; filename=export_{type}.csv"
    resp.headers["Content-Type"] = "text/csv"
    return resp

@app.route('/profile',methods=['GET', 'POST'])
def profile():
    return render_template('profile.html')

@app.route('/keluar',methods=['GET', 'POST'])
def keluar():
    session.clear()
    return redirect(url_for('portal'))

if __name__ == '__main__':
    app.run(debug=True)
