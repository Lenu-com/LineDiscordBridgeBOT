from abc import ABC, abstractmethod


class ILineService(ABC):
    @abstractmethod
    async def handle_webhook(self):
        pass