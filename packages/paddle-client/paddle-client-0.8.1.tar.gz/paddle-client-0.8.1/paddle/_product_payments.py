import logging
from typing import Union
from urllib.parse import urljoin

from .types import PaddleJsonType

log = logging.getLogger(__name__)


def refund_product_payment(
    self,
    order_id: Union[str, int],
    amount: float = None,
    reason: str = None
) -> dict:
    """
    `Refund Product Payment Paddle docs <https://developer.paddle.com/api-reference/product-api/payments/refundpayment>`_
    """  # NOQA: E501
    url = urljoin(self.vendors_v2, 'payment/refund')

    json = {
        'order_id': order_id,
        'amount': amount,
        'reason': reason,
    }  # type: PaddleJsonType
    return self.post(url=url, json=json)
