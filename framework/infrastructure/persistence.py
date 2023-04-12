from application.services.ipersistence import IPersistence
from application.services.itest_service import ITestService
from domain.infrastructure.generics import TEntity


class Persistence(IPersistence):
    def __init__(self, DI_test: ITestService):
        self._test = DI_test
    
    def add(self, entity: TEntity) -> None:
        self._test.add(entity)
        print("Added")

    def remove(self, entity: TEntity) -> None:
        print("Removed")

    def save_changes(self) -> None:
        print("Saved")
