from sqlmodel import Session, create_engine, SQLModel

DATABASE_URL  = "sqlite:///./todo.db"

engine = create_engine(DATABASE_URL, echo=True)

def get_session():
    with Session(engine) as session:
        yield session
    
def init_db():
    SQLModel.metadata.create_all(engine)