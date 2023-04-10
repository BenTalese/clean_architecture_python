from abc import ABCMeta, abstractmethod
from dependency_injector import containers, providers
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, UUID
import uuid

# Database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///test.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={ "check_same_thread": False }
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Domain entity
class DomainEntity:
    def __init__(self, name: str):
        self.m_Name = name

# DB Model
class DBModel:
    __tablename__ = "DomainEntity"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

class IPersistence(metaclass=ABCMeta):
    @abstractmethod
    def Add(self) -> None:
        pass

class Persistence(IPersistence):
    def Add(self) -> None:
        print(1)

class Interactor():
    def __init__(self, persistence: IPersistence):
        self._persistence = persistence
    
    def handle(self):
        self._persistence.Add(self)

class Container(containers.DeclarativeContainer):
    dependency = providers.Object(Persistence)
    my_class = providers.Factory(Interactor, persistence=dependency)


container = Container()
interactor = container.my_class()

interactor.handle()