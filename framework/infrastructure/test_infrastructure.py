from application.services.itest_service import ITestService
from domain.infrastructure.generics import TEntity


class TestInfrastructure(ITestService):
    def add(self, entity: TEntity) -> None:
        print("Added")

    def remove(self, entity: TEntity) -> None:
        print("Removed")

    def save_changes(self) -> None:
        print("Saved")
