from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from sqlalchemy.orm import DeclarativeMeta
from typing import Type


db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()

def TodayMonthToRoman():
    from datetime import date
    roman_months = {
        1: "I", 2: "II", 3: "III", 4: "IV",
        5: "V", 6: "VI", 7: "VII", 8: "VIII",
        9: "IX", 10: "X", 11: "XI", 12: "XII"
    }
    return roman_months[date.today().month]

def GenerateDocNumber(model:Type[DeclarativeMeta],prefix:str):
    from sqlalchemy import func,extract
    from datetime import date
    year= date.today().year
    max_no = db.session.query(func.max(model.no)).filter(extract('year',model.tanggal_buat)==year).scalar()
    no = 1 if max_no is None else max_no+1
    adj = "00" if no < 10 else "0" if no < 100 else ""
    roman = TodayMonthToRoman()
    return no, f"{adj}{no}/{prefix}/MTF/{roman}/{year}"

