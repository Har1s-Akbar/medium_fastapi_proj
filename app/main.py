from fastapi import FastAPI, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from .databse import get_db
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models
from .databse import engine
from .schemas import Products
while True:
    try:
        conn = psycopg2.connect(host='localhost', database='ecommerce', user='postgres',
                                password='admin', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print('Database succesfully connected')
        break
    except Exception as error:
        print('connection failed')
        print('error:', error)
        time.sleep(3)

app = FastAPI()

models.Base.metadata.create_all(bind= engine)

@app.get("/")
def posts():
    return {"message": "this is working"}

@app.post("/product")
def create(product: Products,db: Session = Depends(get_db)):
    new_product = models.Product(**product.dict())
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product

@app.get("/product")
def get(db: Session = Depends(get_db)):
    all_products = db.query(models.Product).all()
    return all_products

@app.delete("/delete/{id}")
def delete(id:int ,db: Session = Depends(get_db), status_code = status.HTTP_204_NO_CONTENT):
    delete_post = db.query(models.Product).filter(models.Product.id == id)
    if delete_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"product with such id does not exist")
    else:
        delete_post.delete(synchronize_session=False)
        db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/update/{id}")
def update(id: int, product:Products, db:Session = Depends(get_db)):
    updated_post = db.query(models.Product).filter(models.Product.id == id)
    updated_post.first()
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with such id: {id} does not exist')
    else:
        updated_post.update(product.dict(), synchronize_session=False)
        db.commit()
    return updated_post.first()
