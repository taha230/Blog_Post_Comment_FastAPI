
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base, Session

# Step 1️⃣: Create FastAPI app
app = FastAPI(title="Blog Comment API")

# Step 2️⃣: Database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./database.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Step 3️⃣: Define database model
class Comment(Base):
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True)
    blog_id = Column(Integer, index=True)
    text = Column(String)

# Create the database tables
Base.metadata.create_all(bind=engine)

# Step 4️⃣: Pydantic schema for request/response
class CommentCreate(BaseModel):
    username: str
    blog_id: int
    text: str

class CommentOut(BaseModel):
    id: int
    username: str
    blog_id: int
    text: str

    class Config:
        orm_mode = True

# Step 5️⃣: Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Step 6️⃣: POST - create a comment
@app.post("/comments/", response_model=CommentOut)
def create_comment(comment: CommentCreate, db: Session = Depends(get_db)):
    db_comment = Comment(**comment.dict())
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment

# Step 7️⃣: GET - list all comments (optional filter by blog_id)
@app.get("/comments/", response_model=list[CommentOut])
def list_comments(blog_id: int | None = None, db: Session = Depends(get_db)):
    query = db.query(Comment)
    if blog_id:
        query = query.filter(Comment.blog_id == blog_id)
    return query.all()

# Step 8️⃣: GET - get single comment by ID
@app.get("/comments/{comment_id}", response_model=CommentOut)
def get_comment(comment_id: int, db: Session = Depends(get_db)):
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    return comment
