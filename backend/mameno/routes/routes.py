from flask import Blueprint,jsonify,request,send_file
from mameno.extension import db
from mameno.models.models import *
from werkzeug.security import generate_password_hash,check_password_hash
from flask_jwt_extended import create_access_token,jwt_required,get_jwt_identity
from uuid import UUID
from sqlalchemy import or_
from sqlalchemy.orm import joinedload
import pandas as pd
from io import BytesIO
from sqlalchemy import text
from datetime import date


main_bp = Blueprint('main', __name__)

@main_bp.route('/version')
def version():
    return "0.0.1",200

@main_bp.get('/api/complaint')
def get_complaints():
    complaints = DbComp.query.all()
    nnew = DbComp.query.filter_by(status='New').count()
    nprogress = DbComp.query.filter_by(status='On Progress').count()
    nclosed = DbComp.query.filter_by(status='Closed').count()

    return jsonify({
        "complaints": [c.to_dict() for c in complaints],  # assumes dbcomp has a to_dict() method
        "status_counts": {
            "New": nnew,
            "On Progress": nprogress,
            "Closed": nclosed
        }
    })

@main_bp.post('/api/complaint')
def create_complaint():

    data = request.get_json()

    # Check for existing complaint
    existing = DbComp.query.filter_by(no_agr=data['no_agr']).first()
    if existing:
        return jsonify({"error": "Nomor Kontrak Sudah Ada"}), 400

    # Create new complaint
    newcomp = DbComp(
        no_agr=data['no_agr'],
        nama=data['nama'],
        area_cg=data['area_cg'],
        cg_name=data['cg_name'],
        class_comp=data['class_comp'],
        agent_notes=data['agent_notes'],
        input_date=date.today(),
        status='New'
    )
    db.session.add(newcomp)
    db.session.commit()

    return jsonify({"message": "Complaint created successfully"}), 201


@main_bp.get('/api/complaints')
def get_complaints_by_status():
    status = request.args.get('status')

    if status not in ['New', 'On Progress', 'Closed']:
        return jsonify({"error": "Invalid status"}), 400

    complaints = DbComp.query.filter_by(status=status).all()
    return jsonify([c.to_dict() for c in complaints])


# @main_bp.route('/dashboard',methods=['GET','POST'])
# def dashboard():
#     df=pd.read_sql_table('dbfucomp', app.config['SQLALCHEMY_DATABASE_URI'])
#     df["MY"]=df['fudate'].dt.strftime('%Y-%m')
#     res=df[df['status']=='Closed'].groupby("MY")[["idcomp"]].nunique().reset_index()
#     print(res)
#     fig = px.bar(res, x='MY', y='idcomp',labels={'MY':'Tanggal','idcomp':'Jumlah Complaint Closed'})

#     fig.update_xaxes(dtick="M1", tickformat="%b %Y")
#     fig.update_yaxes(dtick=1)
#     fig.update_layout(width=500)
#     graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

#     df=pd.read_sql_table('dbcomp', app.config['SQLALCHEMY_DATABASE_URI'])
#     res=df.groupby("status")[["id"]].nunique().reset_index()
#     fig = px.pie(res, values='id', names='status')
#     fig.update_layout(width=400)
#     graphJSON2 = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

#     df=pd.read_sql_table('dbcomp', app.config['SQLALCHEMY_DATABASE_URI'])
#     res=df[df['status']=='On Progress'].groupby("area_cg")[["id"]].nunique().reset_index()
#     fig = px.bar(res, y='area_cg', x='id', orientation='h',labels={'area_cg':'Area CG','id':'Jumlah No Kontrak'})
#     fig.update_layout(width=500)
#     graphJSON3 = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
#     print(df[df['area_cg']=='area 3'])

#     return render_template("dashboard.html",graphJSON=graphJSON,graphJSON2=graphJSON2,graphJSON3=graphJSON3)

@main_bp.get('/api/complaint/<cid>')
def get_complaint(cid):
    comp = DbComp.query.get_or_404(cid)
    return jsonify(comp.to_dict())

@main_bp.put('/api/complaint/<int:cid>')
def update_complaint(cid):
    comp = DbComp.query.get_or_404(cid)
    data = request.get_json()

    # Assign each attribute explicitly
    comp.no_agr = data.get('no_agr', comp.no_agr)
    comp.nama = data.get('nama', comp.nama)
    comp.area_cg = data.get('area_cg', comp.area_cg)
    comp.cg_name = data.get('cg_name', comp.cg_name)
    comp.class_comp = data.get('class_comp', comp.class_comp)
    comp.agent_notes = data.get('agent_notes', comp.agent_notes)
    comp.input_date = data.get('input_date', comp.input_date)
    comp.status = data.get('status', comp.status)
    comp.last_update_date = data.get('last_update_date', comp.last_update_date)

    db.session.commit()
    return jsonify({
        "message": "Complaint updated successfully",
        "updated": comp.to_dict()
    })



@main_bp.route('/fucomp<cid>',methods=['GET','POST'])
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

@main_bp.route('/editfucomp<fid>',methods=['GET','POST'])
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

@main_bp.route('/delfu<fid>',methods=['GET','POST'])
def delfu(fid):
    fu=dbfucomp.query.get(fid)
    print (fu)
    cid=fu.idcomp
    db.session.delete(fu)
    db.session.commit()
    return redirect(url_for('fucomp',cid=cid))

@main_bp.route('/delcomplaint<cid>',methods=['GET','POST'])
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

@main_bp.route('/sppi',methods=['GET','POST'])
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

@main_bp.route('/sppi_exp',methods=['GET','POST'])
def sppi_exp():
    df=dbsppi.query.filter(dbsppi.exp_date<=date.today()+timedelta(30),dbsppi.next_date<=date.today()).all()
    return render_template('sppi_exp.html',df=df)

@main_bp.route('/sppiedit/<id>',methods=['GET','POST'])
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

@main_bp.route('/delsppi/<id>',methods=['GET','POST'])
def delsppi(id):
    deldata=dbsppi.query.get(id)
    db.session.delete(deldata)
    db.session.commit()
    return redirect(url_for('sppi'))


@main_bp.route('/tambah_all',methods=['GET', 'POST'])
def tambah_all():
    if session.get('user',None):
        form=tambah_baru()
        # if form.validate_on_submit():
        if request.method=='POST':
            print(form.type.data)
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

                no_nota=f"{adj}{no}/Nota-CARM/MTF/{mr}/{now.year}"
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

                no_beli=f"{adj}{no}/FPPA-CARM/MTF/{mr}/{now.year}"
                newbeli=tbl_beli(penulis_beli=session['namauser'],judul_beli=form.judul.data,tanggal_buat=now,tahun_beli=now.year,no=no,no_beli=no_beli)
                db.session.add(newbeli)
                db.session.commit()
                return redirect(url_for('result',type='beli',id=newbeli.id))
            elif(form.type.data=="Nota Bersama"):
                divlist=['div1','div2','div3','div4','div5']
                list= "-".join([request.form.get(x).upper().replace(" ",'') for x in divlist if request.form.get(x)])
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

                max = db.session.query(func.max(tbl_bersama.no)).filter_by(tahun=now.year).scalar()
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

                no_beli=f"{adj}{no}/Nota Bersama-{list}/MTF/{mr}/{now.year}"
                newdata=tbl_bersama(penulis=session['namauser'],judul=form.judul.data,tanggal_buat=now,tahun=now.year,no=no,no_bersama=no_beli)
                db.session.add(newdata)
                db.session.commit()
                return redirect(url_for('result',type='bersama',id=newdata.id))
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
                no_memo=f"{adj}{no}/Memo-CARM/MTF/{mr}/{now.year}"
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

@main_bp.route('/result/<type>/<id>',methods=['GET','POST'])
def result(type,id):
    if type=='memo':
        x=tbl_memo.query.get(id)
    elif type=='beli':
        x=tbl_beli.query.get(id)
    elif type=='bersama':
        x=tbl_bersama.query.get(id)
    else:
        x=tbl_nota.query.get(id)
    return render_template('result.html',x=x)

@main_bp.route('/list_nota',methods=['GET','POST'])
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

@main_bp.route('/delnota/<id>',methods=['GET', 'POST'])
def delnota(id):
    delnota=tbl_nota.query.get(id)
    db.session.delete(delnota)
    db.session.commit()
    return redirect(url_for('list_nota'))

@main_bp.route('/delbeli/<id>',methods=['GET', 'POST'])
def delbeli(id):
    delitem=tbl_beli.query.get(id)
    db.session.delete(delitem)
    db.session.commit()
    return redirect(url_for('list_beli'))

@main_bp.route('/delbersama/<id>',methods=['GET', 'POST'])
def delbersama(id):
    delitem=tbl_bersama.query.get(id)
    db.session.delete(delitem)
    db.session.commit()
    return redirect(url_for('list_bersama'))

@main_bp.route('/updatenota/<id>',methods=['GET', 'POST'])
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

@main_bp.route('/updatefbeli/<id>',methods=['GET', 'POST'])
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

@main_bp.route('/list_memo',methods=['GET','POST'])
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

@main_bp.route('/list_beli',methods=['GET','POST'])
def list_beli():

    if session.get('user',None):

        df=tbl_beli.query.all()
        return  render_template ("list_beli.html",df=df,judul='Form Pembelian')
    else:
        return redirect(url_for('masuk'))

@main_bp.route('/list_bersama',methods=['GET','POST'])
def list_bersama():

    if session.get('user',None):

        df=tbl_bersama.query.all()
        return  render_template ("list_beli.html",df=df,judul='Nota Bersama')
    else:
        return redirect(url_for('masuk'))

@main_bp.route('/delmemo/<id>',methods=['GET', 'POST'])
def delmemo(id):
    delmemo=tbl_memo.query.get(id)
    db.session.delete(delmemo)
    db.session.commit()
    return redirect(url_for('list_memo'))

@main_bp.route('/updatememo/<id>',methods=['GET', 'POST'])
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

@main_bp.route('/tambah_historis',methods=['GET', 'POST'])
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
                no_memo=f"{adj}{no}/Memo-CARM/MTF/{mr}/{tgl.year}"

                newmemo=tbl_memo(penulis_memo=form.pic.data,judul_memo=form.judul.data,tanggal_buat=form.tanggal.data,tahun_memo=tgl.year,no=no,no_memo=no_memo)
                db.session.add(newmemo)
                db.session.commit()
                return redirect(url_for('result',type="memo",id=newmemo.id))
            elif(form.type.data=="Nota Bersama"):
                divlist=['div1','div2','div3','div4','div5']
                list= "-".join([request.form.get(x).upper().replace(" ",'') for x in divlist if request.form.get(x)])
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
                # no_memo=f"{adj}{no}/FPPA-CARM/MTF/{mr}/{tgl.year}"
                no_nota=f"{adj}{no}/Nota Bersama-{list}/MTF/{mr}/{tgl.year}"

                newitem=tbl_bersama(penulis=form.pic.data,judul=form.judul.data,tanggal_buat=form.tanggal.data,tahun=tgl.year,no=no,no_bersama=no_nota)
                db.session.add(newitem)
                db.session.commit()
                return redirect(url_for('result',type="bersama",id=newitem.id))
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
                no_memo=f"{adj}{no}/FPPA-CARM/MTF/{mr}/{tgl.year}"

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
                no_nota=f"{adj}{no}/Nota-CARM/MTF/{mr}/{tgl.year}"
                newnota=tbl_nota(penulis_nota=form.pic.data,judul_nota=form.judul.data,tanggal_buat=form.tanggal.data,tahun_nota=tgl.year,no=no,no_nota=no_nota)
                db.session.add(newnota)
                db.session.commit()
                return redirect(url_for('result',type='nota',id=newnota.id))
        else:
            return render_template("tambah_historis.html",form=form)
    else:
        return redirect(url_for('index'))

@main_bp.route('/masuk',methods=['GET', 'POST'])
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

@main_bp.post('/api/signup')
def signup():
    data = request.get_json()
    # Check if username already exists
    if AllUser.query.filter_by(username=data['username']).first():
        return jsonify({"error": "Username already exists"}), 409

    # Create new user
    userbaru = AllUser(
        username=data['username'],
        nama=data['nama'],
        password=data['password']  # Consider hashing this in production
    )
    db.session.add(userbaru)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201


# @main_bp.route('/download/<type>',methods=['GET', 'POST'])
# def download(type):
#     cnx = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
#     if type=='nota':
#         df=pd.read_sql_table('tbl_nota', con=cnx)
#     elif type=='telecol':
#         df=pd.read_sql_table('dbcomp', con=cnx)
#         df2=pd.read_sql_table('dbfucomp', con=cnx)
#         df=df.merge(df2,how='left',left_on='id',right_on='idcomp')
#     elif type=='sppi':
#         df=pd.read_sql_table('dbsppi', con=cnx)
#     else:
#         df=pd.read_sql_table('tbl_memo', con=cnx)
#     resp = make_response(df.to_csv(index=False))
#     resp.headers["Content-Disposition"] = f"attachment; filename=export_{type}.csv"
#     resp.headers["Content-Type"] = "text/csv"
#     return resp

# @main_bp.route('/profile',methods=['GET', 'POST'])
# def profile():
#     return render_template('profile.html')

# @main_bp.route('/keluar',methods=['GET', 'POST'])
# def keluar():
#     session.clear()
#     return redirect(url_for('portal'))
