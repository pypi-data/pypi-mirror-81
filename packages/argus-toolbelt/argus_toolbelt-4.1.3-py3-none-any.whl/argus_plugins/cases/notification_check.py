from collections import OrderedDict
from datetime import datetime

from requests.exceptions import ConnectionError

from argus_api.api.cases.v2.case import (
    advanced_case_search,
    list_case_history,
    list_transaction_notifications,
)
from argus_api.exceptions.http import ArgusException

from argus_cli.utils.formatting import get_data_formatter, FORMATS
from argus_cli.helpers.log import log
from argus_cli.helpers.retry import retry
from argus_cli.plugin import register_command
from argus_plugins import argus_cli_module
from argus_plugins.cases.utils import get_customer_id

RETRY_ON = (ConnectionError, ArgusException, TimeoutError)


def customer_is_notified(case_id: int, transaction_id: str, max_retries: int = 0):
    """Checks if the any of the contacts are NOT a mnemonic email."""
    notifications = retry(
        list_transaction_notifications,
        args=[case_id, transaction_id],
        exception_classes=RETRY_ON,
        max_retries=max_retries,
    )["data"]

    return any(
        notification["contact"].split("@")[-1] != "mnemonic.no"
        for notification in notifications
    )


def non_notified_transactions(case: dict, start: int, end: int, max_retries: int = 0):
    """Returns all transactions where the customer wasn't notified and it wasn't an internal comment."""

    transactions = retry(
        list_case_history,
        args=[case["id"]],
        kwargs={
            "operation": ["createCase", "addCaseComment", "updateCase", "publishCase"],
            "startTimestamp": start,
            "endTimestamp": end,
        },
        exception_classes=RETRY_ON,
        max_retries=max_retries,
    )["data"]

    for transaction in transactions:
        is_internal = "INTERNAL" in transaction.get("object", {}).get("flags", [])
        skipped_notification = "SKIP_NOTIFICATION" in transaction.get("flags", [])

        if is_internal or skipped_notification:
            # In the case that the comment is internal or is marked as a comment that should be skipped:
            # Ignore the given transaction.
            continue
        elif not customer_is_notified(
            case["id"], transaction["id"], max_retries=max_retries
        ):
            yield transaction


@register_command(extending="cases", module=argus_cli_module)
def notification_check(
    start: datetime,
    end: datetime,
    exclude_customer: get_customer_id = [],
    format: FORMATS = "csv",
    max_retries: int = 0,
):
    """Outputs all cases where the customer didn't get a notification

    :param start: The start of the search
    :param end:  The end of the search
    :param list exclude_customer: Customer (shortname) to exclude from the search. Mnemonic is automatically excluded
    :param format: How the output will be formatted.
    :param max_retries: Maximum number of times to retry if a connection error occurs.
    """
    log.warning(
        "This one-off script is going to be moved after ARGUS-11915 is completed!"
    )

    startTimestamp = int(start.timestamp() * 1000)
    endTimestamp = int(end.timestamp() * 1000)

    log.info("Fetching cases...")

    cases = retry(
        advanced_case_search,
        kwargs={
            "startTimestamp": startTimestamp,
            "endTimestamp": endTimestamp,
            "subCriteria": [
                {
                    "exclude": True,
                    "customerID": [customer for customer in (exclude_customer + [1])],
                }
            ],
            "limit": 0,
        },
        exception_classes=RETRY_ON,
        max_retries=max_retries,
    )["data"]

    log.info("Fetched {} cases".format(len(cases)))

    non_notified = []
    for case in cases:
        log.info("Checking case #{}".format(case["id"]))

        nnt = retry(
            non_notified_transactions,
            args=(case, startTimestamp, endTimestamp),
            exception_classes=RETRY_ON,
            kwargs={"max_retries": max_retries},
            max_retries=max_retries,
        )
        for transaction in nnt:
            non_notified.append(
                {
                    "Case ID": "[{id}|https://argusweb.mnemonic.no/spa/case/view/{id}]".format(
                        id=case["id"]
                    ),
                    "Customer": case["customer"]["shortName"],
                    "Transaction Time": datetime.fromtimestamp(
                        transaction["timestamp"] / 1000
                    ).isoformat(sep=" "),
                    "User": transaction["user"]["userName"],
                    "Operation": transaction["operation"],
                    "Sub-Changes": [
                        change["field"] for change in transaction.get("changes", [])
                    ],
                }
            )

    print(get_data_formatter(format)(non_notified))
