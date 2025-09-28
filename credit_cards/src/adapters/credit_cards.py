from src.models.incoming.true_native import RegisterCreditCardResponse
from src.models.internal.created_card import CreatedCard


def create_credit_card_response_to_internal(
    response: RegisterCreditCardResponse,
) -> CreatedCard:
    return CreatedCard(
        ruv=response.RUV,
        token=response.token,
        issuer=response.issuer,
        transaction_identifier=response.transactionIdentifier,
        created_at=response.createdAt,
    )
