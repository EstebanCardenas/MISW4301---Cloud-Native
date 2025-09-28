from abc import ABC, abstractmethod

from src.models.internal.created_card import CreatedCard
from src.models.internal.credit_card_status import CreditCardStatusResponse
from src.models.internal.user import User
from src.models.out.true_native import RegisterCreditCardRequest


class HttpClient(ABC):

    @abstractmethod
    def register_credit_card(self, body: RegisterCreditCardRequest) -> CreatedCard:
        pass

    @abstractmethod
    def get_user_info(self, auth_token: str) -> User:
        pass

    @abstractmethod
    def send_notification(self, email: str, card_number: str, ruv: str) -> None:
        pass

    @abstractmethod
    def get_credit_card(self, ruv: str) -> CreditCardStatusResponse | None:
        pass
