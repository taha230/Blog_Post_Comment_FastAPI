from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base, Session

# Step 1️⃣: Create FastAPI app
app = FastAPI(title="Blog Comment CRUD API")

# Step 2️⃣: Database setup (SQLite)
SQLALCHEMY_DATABASE_URL = "sqlite:///./database.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Step 3️⃣: Database model
class Comment(Base):
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True)
    blog_id = Column(Integer, index=True)
    text = Column(String)

# Create tables
Base.metadata.create_all(bind=engine)

# Step 4️⃣: Pydantic schemas
class CommentBase(BaseModel):
    username: str
    blog_id: int
    text: str

class CommentCreate(CommentBase):
    pass

class CommentUpdate(BaseModel):
    username: str | None = None
    text: str | None = None

class CommentOut(CommentBase):
    id: int
    class Config:
        orm_mode = True

# Step 5️⃣: DB dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ✅ Create Comment
@app.post("/comments/", response_model=CommentOut)
def create_comment(comment: CommentCreate, db: Session = Depends(get_db)):
    db_comment = Comment(**comment.dict())
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment

# ✅ Read All Comments (optionally filtered)
@app.get("/comments/", response_model=list[CommentOut])
def read_comments(blog_id: int | None = None, db: Session = Depends(get_db)):
    query = db.query(Comment)
    if blog_id:
        query = query.filter(Comment.blog_id == blog_id)
    return query.all()

# ✅ Read Single Comment by ID
@app.get("/comments/{comment_id}", response_model=CommentOut)
def read_comment(comment_id: int, db: Session = Depends(get_db)):
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    return comment

# ✅ Update Comment
@app.put("/comments/{comment_id}", response_model=CommentOut)
def update_comment(comment_id: int, update_data: CommentUpdate, db: Session = Depends(get_db)):
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")

    update_dict = update_data.dict(exclude_unset=True)
    for key, value in update_dict.items():
        setattr(comment, key, value)

    db.commit()
    db.refresh(comment)
    return comment

# ✅ Delete Comment
@app.delete("/comments/{comment_id}")
def delete_comment(comment_id: int, db: Session = Depends(get_db)):
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")

    db.delete(comment)
    db.commit()
    return {"message": f"Comment with id {comment_id} has been deleted"}
