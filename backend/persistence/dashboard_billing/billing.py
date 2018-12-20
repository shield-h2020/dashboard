

def vnsf_fee(vnsf_id, fee, support_fee):
    """
    Defines the fee to charge for a vNSF, i.e., the amount the ISP should pay to the Developer.

    :param vnsf_id: The (catalogue) vNSF ID.
    :param fee: The vNSF fee to charge to the ISP.
    :param support_fee: The support fee charge to the ISP.
    """

    # Create a document on model.billing_vnsf.

    pass


def ns_fee(ns_id, fee):
    """
    Defines the fee to charge for a NS, i.e., the amount the SecaaS Client should pay to the ISP.

    :param ns_id: The (catalogue) NS ID.
    :param fee: The NS fee to charge to the SecaaS Client.
    """

    # Create a document on model.billing_ns.

    pass


def update_ns_fee(ns_id, tenant_id, fee):
    """
    Sets the new value to be charged to the SecaaS Client for the given NS.

    A fee update requires a new record with the current price and the termination of the old price. The new record shall
    have no end date, to state that this is the current fee to charge, and the previous record should be updated to
    include an end date set to the current date.

    The billing for the old fee should also be computed as the (old) NS is considered not to be in use anymore.

    :param ns_id: The (catalogue) NS ID to be billed.
    :param tenant_id: The tenant to bill.
    :param fee: The amount to bill.
    """

    # Find the NS document for the given NS and SecaaS Client

    # Bill the tenant for the previous fee (model.billing_ns).
    # As the billing process only bills NSs still in use this operation should be done before performing the actual fee
    # update. As a bonus, this avoids dealing with this edge case during the billing process.

    # Set the end date for the document found to the current date.

    # Create a new document for the fee change. No end date is set.

    pass


def ns_usage(ns_id, tenant_id, fee, used_from, used_to=None):
    """
    Records NS usage data for billing.

    When a NS is placed in the SecaaS Client inventory its usage must be recorded so the client can be billed. Once the
    NS is removed from the inventory it should also be recorded that the client shouldn't be billed for such NS anymore.
    The fee to charge for the duration of the NS usage is the one defined at the time of the addition to the client
    catalogue.

    :param ns_id: The (catalogue) NS ID to be billed.
    :param tenant_id: The tenant to bill.
    :param fee: The amount to bill.
    :param used_from: The date when the NS was started to be available.
    :param used_to: The date when the NS stopped being available. No value means the NS is still available.
    """

    # Create a document on model.billing_ns_usage.

    pass


def bill_tenant(tenant_id=None, start_from=None):
    """
    Updates the billing data for a given tenant. The billing is done on a monthly basis so the day is irrelevant.

    Only consider NS usage after start_from date. When no start date is provided the last available billed date shall be
    used as a starting point.

    :param tenant_id: The tenant to bill.
    :param start_from: The date to start checking for NS usage.
    """

    # Find the current month.

    # Find NS usages for the given tenant (model.billing_ns_usage). Consider only the ones still in use, i.e., without
    # an end date set.

    # For each document found get the latest date for the billing (model.billing_ns.month).

    # For each elapsed month, compute the amount due using the fee defined in each NS usage record
    # (model.billing_ns_usage.fee)

    # Append a new billing document to the billing data (model.billing_ns)

    pass



