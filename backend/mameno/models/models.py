from mameno.extension import db
from sqlalchemy.orm import Mapped,mapped_column,relationship
from sqlalchemy import Integer, String, Text, Date,Boolean
from uuid import uuid4,UUID

class AllUser(db.Model):
    id: Mapped[UUID] = mapped_column(default=uuid4,primary_key=True)
    username: Mapped[str] = mapped_column(String(20), unique=True)
    nama: Mapped[str] = mapped_column(Text)
    role: Mapped[str] = mapped_column(String(10))
    active:Mapped[bool] = mapped_column(Boolean)
    password: Mapped[str] = mapped_column(String(162))

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "nama": self.nama,
            "role":self.role,
            "active":self.active
        }


class TblNota(db.Model):
    id: Mapped[UUID] = mapped_column(default=uuid4,primary_key=True)
    # penulis_nota: Mapped[str] = mapped_column(Text)
    judul_nota: Mapped[str] = mapped_column(Text)
    tanggal_buat: Mapped[Date] = mapped_column(Date)
    # tahun_nota: Mapped[int] = mapped_column(Integer)
    no: Mapped[int] = mapped_column(Integer)
    no_nota: Mapped[str] = mapped_column(Text)
    linknota: Mapped[str] = mapped_column(Text,nullable=True)

    user_id:Mapped[UUID] = mapped_column(db.ForeignKey(AllUser.id))
    user = relationship("AllUser") ## enogh for back ref

    def to_dict(self):
        return {
            "id": self.id,
            "penulis_nota": self.user.nama,
            "judul_nota": self.judul_nota,
            "tanggal_buat": self.tanggal_buat,
            # "tahun_nota": self.tahun_nota,
            "no": self.no,
            "no_nota": self.no_nota,
            "link_nota": self.linknota
        }


class TblMemo(db.Model):
    id: Mapped[UUID] = mapped_column(default=uuid4,primary_key=True)
    # penulis_memo: Mapped[str] = mapped_column(Text)
    judul_memo: Mapped[str] = mapped_column(Text)
    tanggal_buat: Mapped[Date] = mapped_column(Date)
    # tahun_memo: Mapped[int] = mapped_column(Integer)
    no: Mapped[int] = mapped_column(Integer)
    no_memo: Mapped[str] = mapped_column(Text)
    linkmemo: Mapped[str] = mapped_column(Text,nullable=True)

    user_id:Mapped[UUID] = mapped_column(db.ForeignKey(AllUser.id))
    user = relationship("AllUser") ## enogh for back ref

    def to_dict(self):
        return {
            "id": self.id,
            "penulis_memo": self.user.nama,
            "judul_memo": self.judul_memo,
            "tanggal_buat": self.tanggal_buat,
            # "tahun_memo": self.tahun_memo,
            "no": self.no,
            "no_memo": self.no_memo,
            "link_memo": self.linkmemo
        }


class TblBeli(db.Model):
    id: Mapped[UUID] = mapped_column(default=uuid4,primary_key=True)
    # penulis_beli: Mapped[str] = mapped_column(Text)
    judul_beli: Mapped[str] = mapped_column(Text)
    tanggal_buat: Mapped[Date] = mapped_column(Date)
    # tahun_beli: Mapped[int] = mapped_column(Integer)
    no: Mapped[int] = mapped_column(Integer)
    no_beli: Mapped[str] = mapped_column(Text)
    linkbeli: Mapped[str] = mapped_column(Text,nullable=True)

    user_id:Mapped[UUID] = mapped_column(db.ForeignKey(AllUser.id))
    user = relationship("AllUser") ## enogh for back ref

    def to_dict(self):
        return {
            "id": self.id,
            "penulis_beli": self.user.nama,
            "judul_beli": self.judul_beli,
            "tanggal_buat": self.tanggal_buat,
            # "tahun_beli": self.tahun_beli,
            "no": self.no,
            "no_beli": self.no_beli,
            "link_beli": self.linkbeli
        }


class TblBersama(db.Model):
    id: Mapped[UUID] = mapped_column(default=uuid4,primary_key=True)
    # penulis: Mapped[str] = mapped_column(Text)
    judul: Mapped[str] = mapped_column(Text)
    tanggal_buat: Mapped[Date] = mapped_column(Date)
    # tahun: Mapped[int] = mapped_column(Integer)
    no: Mapped[int] = mapped_column(Integer)
    no_bersama: Mapped[str] = mapped_column(Text)
    link: Mapped[str] = mapped_column(Text,nullable=True)

    user_id:Mapped[UUID] = mapped_column(db.ForeignKey(AllUser.id))
    user = relationship("AllUser") ## enogh for back ref

    def to_dict(self):
        return {
            "id": self.id,
            "penulis": self.user.nama,
            "judul": self.judul,
            "tanggal_buat": self.tanggal_buat,
            # "tahun": self.tahun,
            "no": self.no,
            "no_bersama": self.no_bersama,
            "link": self.link
        }




# class DbSppi(db.Model):
#     id: Mapped[int] = mapped_column(primary_key=True)
#     nip: Mapped[str] = mapped_column(String(10))
#     nama: Mapped[str] = mapped_column(String(30))
#     reg: Mapped[str] = mapped_column(String(20))
#     cabang: Mapped[str] = mapped_column(String(30))
#     jabatan: Mapped[str] = mapped_column(String(20))
#     predikat: Mapped[str] = mapped_column(String(20))
#     status: Mapped[str] = mapped_column(String(20))
#     act_date: Mapped[Date] = mapped_column(Date)
#     next_date: Mapped[Date] = mapped_column(Date)
#     exp_date: Mapped[Date] = mapped_column(Date)

#     def to_dict(self):
#         return {
#             "id": self.id,
#             "nip": self.nip,
#             "nama": self.nama,
#             "reg": self.reg,
#             "cabang": self.cabang,
#             "jabatan": self.jabatan,
#             "predikat": self.predikat,
#             "status": self.status,
#             "act_date": self.act_date,
#             "next_date": self.next_date,
#             "exp_date": self.exp_date
#         }


# class DbComp(db.Model):
#     id: Mapped[int] = mapped_column(primary_key=True)
#     no_agr: Mapped[str] = mapped_column(String(20), unique=True)
#     nama: Mapped[str] = mapped_column(String(20))
#     area_cg: Mapped[str] = mapped_column(String(20))
#     cg_name: Mapped[str] = mapped_column(String(20))
#     class_comp: Mapped[str] = mapped_column(String(20))
#     agent_notes: Mapped[str] = mapped_column(Text)
#     input_date: Mapped[Date] = mapped_column(Date)
#     status: Mapped[str] = mapped_column(String(20))
#     last_update_date: Mapped[Date] = mapped_column(Date)

#     followups: Mapped[list["DbFuComp"]] = relationship(back_populates="comp", cascade="all, delete-orphan")


#     def to_dict(self):
#         return {
#             "id": self.id,
#             "no_agr": self.no_agr,
#             "nama": self.nama,
#             "area_cg": self.area_cg,
#             "cg_name": self.cg_name,
#             "class_comp": self.class_comp,
#             "agent_notes": self.agent_notes,
#             "input_date": self.input_date,
#             "status": self.status,
#             "last_update_date": self.last_update_date
#         }

# class DbFuComp(db.Model):
#     id: Mapped[int] = mapped_column(primary_key=True)
#     idcomp: Mapped[int] = mapped_column(db.ForeignKey("db_comp.id"))
#     # idcomp: Mapped[int] = mapped_column(Integer)
#     fupic: Mapped[str] = mapped_column(String(25))
#     fudate: Mapped[Date] = mapped_column(Date)
#     notes: Mapped[str] = mapped_column(Text)
#     status: Mapped[str] = mapped_column(String(20))

#     def to_dict(self):
#         return {
#             "id": self.id,
#             "idcomp": self.idcomp,
#             "fupic": self.fupic,
#             "fudate": self.fudate,
#             "notes": self.notes,
#             "status": self.status
#         }