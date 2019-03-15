from restoweb import db
from restoweb import models

db.drop_all()
db.create_all()

db.session.add(models.Resto(
        name="Resto De Brug",
        zip_code="9000",
        city="Gent",
        address="Sint-Pietersnieuwstraat 45",
        campus="Campus Ufo"
    )
)

db.session.add(models.Resto(
        name="Resto Campus Sterre",
        zip_code="9000",
        city="Gent",
        address="Krijgslaan 281",
        campus="Campus Sterre",
        description="De resto bevindt zich in gebouw S5."
    )
)

db.session.add(models.Resto(
        name="Resto Kantienberg",
        zip_code="9000",
        city="Gent",
        address="Stalhof 45",
        description="De resto bevindt zich op het gelijkvloers van Home Canterbury."
    )
)

db.session.commit()
