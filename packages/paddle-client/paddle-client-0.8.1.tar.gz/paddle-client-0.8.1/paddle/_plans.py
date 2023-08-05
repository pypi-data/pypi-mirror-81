import logging
from typing import List
from urllib.parse import urljoin

from .types import PaddleJsonType

log = logging.getLogger(__name__)


def list_plans(self, plan: int = None) -> List[dict]:
    """
    `List Plans Paddle docs <https://developer.paddle.com/api-reference/subscription-api/plans/listplans>`_
    """  # NOQA: E501
    url = urljoin(self.vendors_v2, 'subscription/plans')

    if plan:
        return self.post(url=url, json={'plan': plan})

    return self.post(url=url)


def get_plan(self, plan: int) -> dict:
    """
    `List Plans Paddle docs <https://developer.paddle.com/api-reference/subscription-api/plans/listplans>`_

    There is no Get Plan endpoint in Paddle's API but list plans does support
    sending through a plan ID. This is a helper method to get a single plan
    where the plan parameter is required.
    """  # NOQA: E501
    return self.list_plans(plan=plan)[0]


def create_plan(
    self,
    plan_name: str,
    plan_trial_days: int,
    plan_length: int,
    plan_type: str,
    main_currency_code: str = 'USD',
    initial_price_usd: float = None,
    initial_price_gbp: float = None,
    initial_price_eur: float = None,
    recurring_price_usd: float = None,
    recurring_price_gbp: float = None,
    recurring_price_eur: float = None,
) -> dict:
    """
    `Create Plan Paddle docs <https://developer.paddle.com/api-reference/subscription-api/plans/createplan>`_

    In the docs all of the price variables are noted as strings except for USD
    which is a number. This is probably an error in the docs.
    """  # NOQA: E501
    url = urljoin(self.vendors_v2, 'subscription/plans_create')

    plan_types = ['day', 'week', 'month', 'year']
    if plan_type not in plan_types:
        raise ValueError('plan_type must be one of {0}'.format(', '.join(plan_types)))  # NOQA: E501
    main_currency_codes = ['USD', 'GBP', 'EUR']
    if main_currency_code not in main_currency_codes:
        raise ValueError('main_currency_code must be one of {0}'.format(', '.join(main_currency_codes)))  # NOQA: E501

    if main_currency_code == 'USD' and initial_price_usd is None:
        raise ValueError('main_currency_code is USD so initial_price_usd must be set')  # NOQA: E501
    if main_currency_code == 'GBP' and initial_price_gbp is None:
        raise ValueError('main_currency_code is GBP so initial_price_gbp must be set')  # NOQA: E501
    if main_currency_code == 'EUR' and initial_price_eur is None:
        raise ValueError('main_currency_code is EUR so initial_price_eur must be set')  # NOQA: E501
    if main_currency_code == 'USD' and recurring_price_usd is None:
        raise ValueError('main_currency_code is USD so recurring_price_usd must be set')  # NOQA: E501
    if main_currency_code == 'GBP' and recurring_price_gbp is None:
        raise ValueError('main_currency_code is GBP so recurring_price_gbp must be set')  # NOQA: E501
    if main_currency_code == 'EUR' and recurring_price_eur is None:
        raise ValueError('main_currency_code is EUR so recurring_price_eur must be set')  # NOQA: E501

    json = {
        'plan_name': plan_name,
        'plan_trial_days': plan_trial_days,
        'plan_length': plan_length,
        'plan_type': plan_type,
        'main_currency_code': main_currency_code,
        'initial_price_usd': initial_price_usd,
        'initial_price_gbp': initial_price_gbp,
        'initial_price_eur': initial_price_eur,
        'recurring_price_usd': recurring_price_usd,
        'recurring_price_gbp': recurring_price_gbp,
        'recurring_price_eur': recurring_price_eur,
    }  # type: PaddleJsonType
    return self.post(url=url, json=json)
