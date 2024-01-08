from app.application.services.line_service import LineService
from app.application.services.interfaces.i_line_service import ILineService


class LineServiceFactory:
    @staticmethod
    def create() -> ILineService:
        return LineService()