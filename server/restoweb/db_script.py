from restoweb import db
from restoweb import models
from datetime import time

db.drop_all()
db.create_all()

restos = [
    models.Resto(
        name="Resto De Brug",
        zip_code="9000",
        city="Gent",
        address="Sint-Pietersnieuwstraat 45",
        campus="Campus Ufo"
    ),
    models.Resto(
        name="Resto Campus Sterre",
        zip_code="9000",
        city="Gent",
        address="Krijgslaan 281",
        campus="Campus Sterre",
        description="De resto bevindt zich in gebouw S5."
    ),
    models.Resto(
        name="Resto Kantienberg",
        zip_code="9000",
        city="Gent",
        address="Stalhof 45",
        description="De resto bevindt zich op het gelijkvloers van Home Canterbury."
    )
]

schedules = [
    models.Schedules(
        time_open=time(hour=11, minute=15),
        time_closed=time(hour=14, minute=0)
    )
]

for resto in restos:
    db.session.add(resto)

db.session.commit()
