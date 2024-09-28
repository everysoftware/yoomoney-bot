import random
import string

from yoomoney import Quickpay, Client

from app.config import settings


def get_quick_pay() -> Quickpay:
    alphabet = string.ascii_lowercase + string.digits
    state = "".join(random.sample(alphabet, 10))
    quick_pay = Quickpay(
        receiver=settings.pay_receiver,
        quickpay_form="shop",
        targets="Test",
        paymentType="SB",
        sum=2,
        label=state,
    )
    return quick_pay


def check_quick_pay(pay_state: str) -> bool:
    client = Client(settings.pay_token)
    history = client.operation_history(label=pay_state)
    return history.operations and history.operations[-1].status == "success"  # type: ignore[no-any-return]
