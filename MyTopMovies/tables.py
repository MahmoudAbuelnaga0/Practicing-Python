from sqlalchemy import Column, String, Integer, Float
from sqlalchemy.orm import declarative_base

Base = declarative_base()
class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key= True)
    title = Column(String, nullable= False)
    year = Column(Integer, nullable= False)
    description = Column(String, nullable= False)
    rating = Column(Float)
    review = Column(String)
    img_url = Column(String)

    def __repr__(self) -> str:
        return f"Movie(title= {self.title})"