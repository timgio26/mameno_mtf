from flask import Blueprint,jsonify,request,send_file
from mameno.extension import db,TodayMonthToRoman,GenerateDocNumber
from mameno.models.models import *
from werkzeug.security import generate_password_hash,check_password_hash
from flask_jwt_extended import create_access_token,jwt_required,get_jwt_identity
from uuid import UUID
from sqlalchemy import or_,asc
from sqlalchemy.orm import joinedload
import pandas as pd
from io import BytesIO
from sqlalchemy import text
from datetime import date,datetime


main_bp = Blueprint('main', __name__)

@main_bp.route('/version')
def version():
    return "0.0.1",200

################### CREATE

@main_bp.post('/api/nota')
def create_nota():
    data = request.get_json()
    now = date.today()
    no, no_nota = GenerateDocNumber(model=TblNota, prefix="Nota-CARM")

    newnota = TblNota(
        # penulis_nota=data.get("penulis"),
        user_id=UUID(data.get("user_id")),
        judul_nota=data.get("judul"),
        tanggal_buat=now,
        # tahun_nota=now.year,
        no=no,
        no_nota=no_nota
    )
    db.session.add(newnota)
    db.session.commit()

    return jsonify({
        "message": "Nota created successfully",
        "id": newnota.id,
        "no_nota": no_nota
    }), 201

@main_bp.post('/api/memo')
def create_memo():
    data = request.get_json()
    now = date.today()
    no, no_memo = GenerateDocNumber(model=TblMemo, prefix="Memo-CARM")

    newmemo = TblMemo(
        # penulis_memo=data.get("penulis"),
        user_id=UUID(data.get("user_id")),
        judul_memo=data.get("judul"),
        tanggal_buat=now,
        # tahun_memo=now.year,
        no=no,
        no_memo=no_memo
    )
    db.session.add(newmemo)
    db.session.commit()

    return jsonify({
        "message": "Memo created successfully",
        "id": newmemo.id,
        "no_memo": no_memo
    }), 201

@main_bp.post('/api/beli')
def create_beli():
    data = request.get_json()
    now = date.today()
    no, no_beli = GenerateDocNumber(model=TblBeli, prefix="FPPA-CARM")

    newbeli = TblBeli(
        # penulis_beli=data.get("penulis"),
        user_id=UUID(data.get("user_id")),
        judul_beli=data.get("judul"),
        tanggal_buat=now,
        # tahun_beli=now.year,
        no=no,
        no_beli=no_beli
    )
    db.session.add(newbeli)
    db.session.commit()

    return jsonify({
        "message": "Form Pembelian created successfully",
        "id": newbeli.id,
        "no_beli": no_beli
    }), 201

@main_bp.post('/api/bersama')
def create_bersama():
    data = request.get_json()
    now = date.today()
    divlist = ['div1', 'div2', 'div3', 'div4', 'div5']
    list_str = "-".join([data.get(x, "").upper().replace(" ", "") for x in divlist if data.get(x)])
    no, no_bersama = GenerateDocNumber(model=TblBersama, prefix=f"Nota Bersama-{list_str}")

    newdata = TblBersama(
        # penulis=data.get("penulis"),
        user_id=UUID(data.get("user_id")),
        judul=data.get("judul"),
        tanggal_buat=now,
        # tahun=now.year,
        no=no,
        no_bersama=no_bersama
    )
    db.session.add(newdata)
    db.session.commit()

    return jsonify({
        "message": "Nota Bersama created successfully",
        "id": newdata.id,
        "no_bersama": no_bersama
    }), 201

################### READ

@main_bp.get('/api/memo')
def get_memo_list():
    # tahun = request.args.get('tahun', type=int)
    judul = request.args.get('judul', '', type=str)

    # Default to current year if no tahun provided
    # if not tahun:
    #     tahun = datetime.now().year

    query = TblMemo.query.order_by(asc(TblMemo.no))#.filter_by(tahun_memo=tahun)

    if judul:
        query = query.filter(TblMemo.judul_memo.contains(judul))

    records = query.all()

    return jsonify({
        # "tahun": tahun,
        # "judul_filter": judul,
        "data": [r.to_dict() for r in records]
    }), 200

@main_bp.get('/api/beli')
def get_beli_list():
    records = TblBeli.query.all()
    return jsonify({
        "judul": "Form Pembelian",
        "data": [r.to_dict() for r in records]
    }), 200

@main_bp.get('/api/bersama')
def get_bersama_list():
    records = TblBersama.query.all()
    return jsonify({
        "judul": "Nota Bersama",
        "data": [r.to_dict() for r in records]
    }), 200

@main_bp.get('/api/nota')
def get_nota_list():
    # tahun = request.args.get('tahun', type=int)
    judul = request.args.get('judul', '', type=str)

    # # Default to current year if no tahun provided
    # if not tahun:
    #     tahun = datetime.now().year

    query = TblNota.query.order_by(asc(TblNota.no))#.filter_by(tahun_nota=tahun)

    if judul:
        query = query.filter(TblNota.judul_nota.contains(judul))

    records = query.all()

    return jsonify({
        # "tahun": tahun,
        # "judul_filter": judul,
        "data": [r.to_dict() for r in records]
    }), 200

################### DELETE

@main_bp.delete('/api/nota/<id>')
def delete_nota(id):
    print(id)
    nota = TblNota.query.get_or_404(UUID(id))
    db.session.delete(nota)
    db.session.commit()
    return jsonify({
        "message": "Nota deleted successfully",
        "deleted_id": id
    }), 200

@main_bp.delete('/api/memo/<id>')
def delete_memo(id):
    memo = TblMemo.query.get_or_404(id)

    db.session.delete(memo)
    db.session.commit()

    return jsonify({
        "message": "Memo deleted successfully",
        "deleted_id": id
    }), 200

@main_bp.delete('/api/beli/<id>')
def delete_beli(id):
    item = TblBeli.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    return jsonify({
        "message": "Pembelian deleted successfully",
        "deleted_id": id
    }), 200

@main_bp.delete('/api/bersama/<id>')
def delete_bersama(id):
    item = TblBersama.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    return jsonify({
        "message": "Nota Bersama deleted successfully",
        "deleted_id": id
    }), 200

################### UPDATE

@main_bp.put('/api/nota/<id>')
def update_nota(id):
    upnota = TblNota.query.get_or_404(id)
    data = request.get_json()

    # Assign each attribute explicitly
    upnota.linknota = data.get('url', upnota.linknota)
    upnota.penulis_nota = data.get('pic', upnota.penulis_nota)
    upnota.judul_nota = data.get('judul', upnota.judul_nota)
    upnota.no_nota = data.get('no', upnota.no_nota)
    upnota.tanggal_buat = data.get('tgl_update', upnota.tanggal_buat)

    db.session.commit()

    return jsonify({
        "message": "Nota updated successfully",
        "updated": upnota.to_dict()
    }), 200

@main_bp.put('/api/memo/<id>')
def update_memo(id):
    upmemo = TblMemo.query.get_or_404(id)
    data = request.get_json()

    upmemo.linkmemo = data.get('url', upmemo.linkmemo)
    upmemo.penulis_memo = data.get('pic', upmemo.penulis_memo)
    upmemo.judul_memo = data.get('judul', upmemo.judul_memo)
    upmemo.no_memo = data.get('no', upmemo.no_memo)
    upmemo.tanggal_buat = data.get('tgl_update', upmemo.tanggal_buat)

    db.session.commit()

    return jsonify({
        "message": "Memo updated successfully",
        "updated": upmemo.to_dict()
    }), 200

@main_bp.put('/api/beli/<id>')
def update_beli(id):
    upmemo = TblBeli.query.get_or_404(id)
    data = request.get_json()

    # Assign each attribute explicitly
    upmemo.linkbeli = data.get('url', upmemo.linkbeli)
    upmemo.penulis_beli = data.get('pic', upmemo.penulis_beli)
    upmemo.judul_beli = data.get('judul', upmemo.judul_beli)
    upmemo.no_beli = data.get('no', upmemo.no_beli)
    upmemo.tanggal_buat = data.get('tgl_update', upmemo.tanggal_buat)

    db.session.commit()

    return jsonify({
        "message": "Purchase record updated successfully",
        "updated": upmemo.to_dict()
    }), 200

@main_bp.put('/api/bersama/<id>')
def update_bersama(id):
    data = request.get_json()
    now = date.today()

    bersama = TblBersama.query.get_or_404(id)

    # Update fields
    bersama.penulis = data.get("penulis", bersama.penulis)
    bersama.judul = data.get("judul", bersama.judul)
    bersama.tanggal_buat = now
    bersama.tahun = now.year

    # Optional: regenerate no_bersama if divisions are updated
    divlist = ['div1', 'div2', 'div3', 'div4', 'div5']
    list_str = "-".join([data.get(x, "").upper().replace(" ", "") for x in divlist if data.get(x)])
    if list_str:
        _, no_bersama = GenerateDocNumber(model=TblBersama, prefix=f"Nota Bersama-{list_str}")
        bersama.no_bersama = no_bersama

    db.session.commit()

    return jsonify({
        "message": "Nota Bersama updated successfully",
        "id": bersama.id,
        "no_bersama": bersama.no_bersama
    }), 200

################### authentication

@main_bp.post('/api/login')
def login():
    data = request.get_json()

    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "Missing username or password"}), 400

    entry = AllUser.query.filter_by(username=username).first()

    if not check_password_hash(entry.password,password):
        return jsonify({"error": "Invalid username or password"}), 401

    # Create JWT token
    access_token = create_access_token(identity=entry.id)

    return jsonify({
        "message": "Login successful",
        "token": access_token,
        "user": {
            "username": entry.username,
            "nama": entry.nama
        }
    }), 200

@main_bp.post('/api/signup')
def signup():
    data = request.get_json()
    # Check if username already exists
    if AllUser.query.filter_by(username=data['username']).first():
        return jsonify({"error": "Username already exists"}), 409

    # Create new user
    userbaru = AllUser(
        username=data['username'],
        nama=data['name'],
        password=generate_password_hash(data['password'])  # Consider hashing this in production
    )
    db.session.add(userbaru)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201