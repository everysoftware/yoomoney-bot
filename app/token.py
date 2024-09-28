from yoomoney import Authorize

Authorize(
    client_id="",
    client_secret="",
    redirect_uri="",
    scope=[
        "account-info",
        "operation-history",
        "operation-details",
        "incoming-transfers",
        "payment-p2p",
        "payment-shop",
    ],
)
