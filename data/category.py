import sqlalchemy
from .db_session import SqlAlchemyBase
   
   
class Category(SqlAlchemyBase):
    __tablename__ = 'category'
    association_table = sqlalchemy.Table(
    'association',
    SqlAlchemyBase.metadata,
    sqlalchemy.Column('jobs', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('jobs.id')),
    sqlalchemy.Column('category', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('category.id'))
    )
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, 
                           autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)