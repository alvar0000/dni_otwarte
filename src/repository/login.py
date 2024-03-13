from sqlalchemy.orm import Session, load_only
from .. import models


def get_user_type(db: Session, user: models.Visitor):
    user_type = (db.query(models.Visitor, models.VisitorType)
                   .join(models.VisitorType, models.Visitor.type == models.VisitorType.id)
                   .filter(models.VisitorType.id == user.type)
                   .options(load_only(models.VisitorType.name))
                   .first()
                 )

    return user_type[1].name
