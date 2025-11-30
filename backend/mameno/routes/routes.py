from flask import Blueprint,jsonify,request,send_file
from mameno.extension import db,GenerateDocNumber
from mameno.models.models import *
from werkzeug.security import generate_password_hash,check_password_hash
from flask_jwt_extended import create_access_token,jwt_required,create_refresh_token,set_access_cookies,set_refresh_cookies,unset_jwt_cookies,get_jwt_identity,get_jwt
from uuid import UUID
from sqlalchemy import or_,desc,text
from datetime import date
import pandas as pd
from io import BytesIO


main_bp = Blueprint('main', __name__)

@main_bp.route('/version')
def version():
    return "0.0.1",200

@main_bp.get('/api/notauth')
def notauth():
    return "",401

@main_bp.get('/api/user')
@jwt_required()
def get_all_user():
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))
    offset = (page - 1) * per_page
    # users = AllUser.query.all()
    query = AllUser.query
    users = query.offset(offset).limit(per_page).all()
    total = query.count()
    return jsonify({
        "data": [r.to_dict() for r in users],
        "page": page,
        "total_pages": (total + per_page - 1) // per_page
    }), 200

@main_bp.delete('/api/user/<id>')
@jwt_required()
def del_user(id):
    user = AllUser.query.get_or_404(UUID(id))
    db.session.delete(user)
    db.session.commit()
    return jsonify({
        "message": "User deleted successfully",
        "deleted_id": id
    }), 200

@main_bp.put('/api/user/<id>')
@jwt_required()
def update_user(id):
    user = AllUser.query.get_or_404(UUID(id))
    data = request.get_json()

    user.nama = data.get('name', user.nama)
    user.username = data.get('username', user.username)
    user.role = data.get('role', user.role)
    user.active = data.get('active', user.active)
    # upmemo.no_memo = data.get('no', upmemo.no_memo)
    # upmemo.tanggal_buat = data.get('tgl_update', upmemo.tanggal_buat)

    db.session.commit()

    return jsonify({
        "message": "Memo updated successfully",
        "updated": user.to_dict()
    }), 200

################### CREATE

@main_bp.post('/api/nota')
@jwt_required()
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
        "no_doc": no_nota,
        "pic":newnota.user.nama,
        "judul":newnota.judul_nota
    }), 201

@main_bp.post('/api/memo')
@jwt_required()
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
        "no_doc": no_memo,
        "pic":newmemo.user.nama,
        "judul":newmemo.judul_memo
    }), 201

@main_bp.post('/api/beli')
@jwt_required()
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
        "no_doc": newbeli.no_beli,
        "pic":newbeli.user.nama,
        "judul":newbeli.judul_beli
    }), 201

@main_bp.post('/api/bersama')
@jwt_required()
def create_bersama():
    data = request.get_json()
    now = date.today()
    # print(data.get("divisi"))
    # divlist = ['div1', 'div2', 'div3', 'div4', 'div5']
    list_str = "-".join([str(div).upper() for div in data.get("divisi")])
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
        "no_doc": newdata.no_bersama,
        "pic":newdata.user.nama,
        "judul":newdata.judul
    }), 201

################### READ

@main_bp.get('/api/memo')
@jwt_required()
def get_memo_list():
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))  # default 20 items per page
    search = str(request.args.get('search'))

    # Calculate offset
    offset = (page - 1) * per_page
    query = TblMemo.query.order_by(desc(TblMemo.tanggal_buat))

    # Apply filtering only if search is provided
    if len(search)>0:
        query = query.filter(or_(
            TblMemo.judul_memo.contains(f"%{search}%"),
            TblMemo.no_memo.contains(f"%{search}%")
        ))

    total = query.count()
    records = query.offset(offset).limit(per_page).all()

    return jsonify({
        # "tahun": tahun,
        # "judul_filter": judul,
        "data": [r.to_dict() for r in records],
        "page": page,
        # "per_page": per_page,
        # "total": total,
        "total_pages": (total + per_page - 1) // per_page
    }), 200

@main_bp.get('/api/beli')
@jwt_required()
def get_beli_list():
    # records = TblBeli.query.all()
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))  # default 20 items per page
    search = str(request.args.get('search'))

    # Calculate offset
    offset = (page - 1) * per_page
    query = TblBeli.query.order_by(desc(TblBeli.tanggal_buat))

    # Apply filtering only if search is provided
    if len(search)>0:
        query = query.filter(or_(
            TblBeli.judul_beli.contains(f"%{search}%"),
            TblBeli.no_beli.contains(f"%{search}%")
        )
        )

    total = query.count()
    records = query.offset(offset).limit(per_page).all()
    return jsonify({
        "data": [r.to_dict() for r in records],
        "page": page,
        "total_pages": (total + per_page - 1) // per_page
    }), 200

@main_bp.get('/api/bersama')
@jwt_required()
def get_bersama_list():
    # records = TblBersama.query.all()
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))  # default 20 items per page
    search = str(request.args.get('search'))

    # Calculate offset
    offset = (page - 1) * per_page
    query = TblBersama.query.order_by(desc(TblBersama.tanggal_buat))

    # Apply filtering only if search is provided
    if len(search)>0:
        query = query.filter(or_(

            TblBersama.judul.contains(f"%{search}%"),
            TblBersama.no_bersama.contains(f"%{search}%")
        )
        )

    total = query.count()
    records = query.offset(offset).limit(per_page).all()
    return jsonify({
        "data": [r.to_dict() for r in records],
        "page": page,
        "total_pages": (total + per_page - 1) // per_page
    }), 200

@main_bp.get('/api/nota')
@jwt_required()
def get_nota_list():
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))  # default 20 items per page
    search = str(request.args.get('search'))

    # Calculate offset
    offset = (page - 1) * per_page
    query = TblNota.query.order_by(desc(TblNota.tanggal_buat))

    # Apply filtering only if search is provided
    if len(search)>0:
        query = query.filter(or_(
                TblNota.judul_nota.contains(f"%{search}%"),
                TblNota.no_nota.contains(f"%{search}%")
            ))

    total = query.count()
    records = query.offset(offset).limit(per_page).all()

    return jsonify({
        # "tahun": tahun,
        # "judul_filter": judul,
        "data": [r.to_dict() for r in records],
        "page": page,
        # "per_page": per_page,
        # "total": total,
        "total_pages": (total + per_page - 1) // per_page
    }), 200

################### DELETE

@main_bp.delete('/api/nota/<id>')
@jwt_required()
def delete_nota(id):
    nota = TblNota.query.get_or_404(UUID(id))
    db.session.delete(nota)
    db.session.commit()
    return jsonify({
        "message": "Nota deleted successfully",
        "deleted_id": id
    }), 200

@main_bp.delete('/api/memo/<id>')
@jwt_required()
def delete_memo(id):
    memo = TblMemo.query.get_or_404(UUID(id))

    db.session.delete(memo)
    db.session.commit()

    return jsonify({
        "message": "Memo deleted successfully",
        "deleted_id": id
    }), 200

@main_bp.delete('/api/beli/<id>')
@jwt_required()
def delete_beli(id):
    item = TblBeli.query.get_or_404(UUID(id))
    db.session.delete(item)
    db.session.commit()
    return jsonify({
        "message": "Pembelian deleted successfully",
        "deleted_id": id
    }), 200

@main_bp.delete('/api/bersama/<id>')
@jwt_required()
def delete_bersama(id):
    item = TblBersama.query.get_or_404(UUID(id))
    db.session.delete(item)
    db.session.commit()
    return jsonify({
        "message": "Nota Bersama deleted successfully",
        "deleted_id": id
    }), 200

################### UPDATE

@main_bp.put('/api/nota/<id>')
@jwt_required()
def update_nota(id):
    upnota = TblNota.query.get_or_404(UUID(id))
    data = request.get_json()

    # Assign each attribute explicitly
    upnota.linknota = data.get('url', upnota.linknota)
    # upnota.penulis_nota = data.get('pic', upnota.penulis_nota)
    upnota.judul_nota = data.get('judul', upnota.judul_nota)
    # upnota.no_nota = data.get('no', upnota.no_nota)
    # upnota.tanggal_buat = data.get('tgl_update', upnota.tanggal_buat)

    db.session.commit()

    return jsonify({
        "message": "Nota updated successfully",
        "updated": upnota.to_dict()
    }), 200

@main_bp.put('/api/memo/<id>')
@jwt_required()
def update_memo(id):
    upmemo = TblMemo.query.get_or_404(UUID(id))
    data = request.get_json()

    upmemo.linkmemo = data.get('url', upmemo.linkmemo)
    # upmemo.penulis_memo = data.get('pic', upmemo.penulis_memo)
    upmemo.judul_memo = data.get('judul', upmemo.judul_memo)
    # upmemo.no_memo = data.get('no', upmemo.no_memo)
    # upmemo.tanggal_buat = data.get('tgl_update', upmemo.tanggal_buat)

    db.session.commit()

    return jsonify({
        "message": "Memo updated successfully",
        "updated": upmemo.to_dict()
    }), 200

@main_bp.put('/api/beli/<id>')
@jwt_required()
def update_beli(id):
    upmemo = TblBeli.query.get_or_404(UUID(id))
    data = request.get_json()

    # Assign each attribute explicitly
    upmemo.linkbeli = data.get('url', upmemo.linkbeli)
    # upmemo.penulis_beli = data.get('pic', upmemo.penulis_beli)
    upmemo.judul_beli = data.get('judul', upmemo.judul_beli)
    # upmemo.no_beli = data.get('no', upmemo.no_beli)
    # upmemo.tanggal_buat = data.get('tgl_update', upmemo.tanggal_buat)

    db.session.commit()

    return jsonify({
        "message": "Purchase record updated successfully",
        "updated": upmemo.to_dict()
    }), 200

@main_bp.put('/api/bersama/<id>')
@jwt_required()
def update_bersama(id):
    data = request.get_json()
    # now = date.today()

    bersama = TblBersama.query.get_or_404(UUID(id))

    # Update fields
    # bersama.penulis = data.get("penulis", bersama.penulis)
    bersama.judul = data.get("judul", bersama.judul)
    bersama.link = data.get("url", bersama.link)
    # bersama.tanggal_buat = now
    # bersama.tahun = now.year

    # # Optional: regenerate no_bersama if divisions are updated
    # divlist = ['div1', 'div2', 'div3', 'div4', 'div5']
    # list_str = "-".join([data.get(x, "").upper().replace(" ", "") for x in divlist if data.get(x)])
    # if list_str:
    #     _, no_bersama = GenerateDocNumber(model=TblBersama, prefix=f"Nota Bersama-{list_str}")
    #     bersama.no_bersama = no_bersama

    db.session.commit()

    return jsonify({
        "message": "Nota Bersama updated successfully",
        "id": bersama.id,
        "no_bersama": bersama.no_bersama
    }), 200

################### authentication

@main_bp.get('/api/me')
@jwt_required()
def auth_check():
    claims = get_jwt()
    user_id = get_jwt_identity()
    return jsonify({"authenticated": True, "user_id": user_id,"role":claims.get("role")})

@main_bp.post('/api/login')
def login():
    data = request.get_json()

    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "Missing username or password"}), 400

    entry = AllUser.query.filter_by(username=username,active=True).first_or_404()

    if not entry or not check_password_hash(entry.password, password):
        return jsonify({"error": "Invalid username or password"}), 401

    # Create JWT tokens
    access_token = create_access_token(identity=entry.id,additional_claims={"role":entry.role},expires_delta=False)
    refresh_token = create_refresh_token(identity=entry.id)

    # Build response
    resp = jsonify({
        "message": "Login successful",
        "user": {
            "username": entry.username,
            "nama": entry.nama,
            "user_id":entry.id
        }
    })

    # Set tokens in HTTP-only cookies
    set_access_cookies(resp, access_token)
    set_refresh_cookies(resp, refresh_token)

    return resp, 200



@main_bp.post('/api/signup')
@jwt_required()
def signup():
    data = request.get_json()
    # Check if username already exists
    if AllUser.query.filter_by(username=data['username']).first():
        return jsonify({"error": "Username already exists"}), 409

    # Create new user
    userbaru = AllUser(
        username=data['username'],
        nama=data['name'],
        role=str(data['role']).lower(),
        password=generate_password_hash(data['password']),
        active = True # Consider hashing this in production
    )
    db.session.add(userbaru)
    db.session.commit()

    return jsonify({"message": "User registered successfully","user_id":userbaru.id}), 201

@main_bp.post("/api/logout")
def logout():
    resp = jsonify({"msg": "logout successful"})
    unset_jwt_cookies(resp)   # clears both access + refresh cookies
    return resp, 200

@main_bp.post("/api/refresh")
@jwt_required(refresh=True)
def refresh():
    user_id = get_jwt_identity()
    new_access_token = create_access_token(identity=user_id)
    resp = jsonify({"msg": "token refreshed"})
    set_access_cookies(resp, new_access_token)  # overwrite old access cookie
    return resp, 200

################### download

@main_bp.get('/api/download')
@jwt_required()
def download_data():

    # Raw SQL query
    query = """
        SELECT * FROM tbl_nota
    """
    # Run query using SQLAlchemy engine
    df_nota = pd.read_sql_query(text(query), db.engine)

    # query = """
    #     SELECT * FROM tbl_memo
    # """
    # df_memo = pd.read_sql_query(text(query), db.engine)

    # query = """
    #     SELECT * FROM tbl_beli
    # """
    # df_beli = pd.read_sql_query(text(query), db.engine)

    # query = """
    #     SELECT * FROM tbl_bersama
    # """
    # df_bersama = pd.read_sql_query(text(query), db.engine)

    # Write to Excel in memory
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df_nota.to_excel(writer, index=False, sheet_name='Nota')
        # df_memo.to_excel(writer, index=False, sheet_name='Memo')
        # df_beli.to_excel(writer, index=False, sheet_name='Pembelian')
        # df_bersama.to_excel(writer, index=False, sheet_name='Nota_Bersama')


    output.seek(0)

    # Return as downloadable file
    return send_file(
        output,
        download_name="mameno.xlsx",
        as_attachment=True,
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
