AIRPORT_DISTANCE = {
    ('BOM', 'DEL'): 1148,
    ('DEL', 'BLR'): 1740,
    ('BLR', 'HYD'): 500,
    ('BOM', 'BLR'): 842,
}


def normalize_sap(row):
    """
    SAP Fuel / Procurement Data
    Example:
    quantity=300
    unit=Gallons
    """

    quantity = float(row["quantity"])
    unit = row["unit"]

    # Convert Gallons to Litres
    if unit.lower() == "gallons":
        quantity = quantity * 3.785
        unit = "L"

    return {
        "value": quantity,
        "unit": unit,
        "scope": "SCOPE1",
        "category": "Fuel"
    }


def normalize_utility(row):
    """
    Utility Electricity Data
    """

    kwh = float(row["kwh"])

    return {
        "value": kwh,
        "unit": "kWh",
        "scope": "SCOPE2",
        "category": "Electricity"
    }


def normalize_travel(row):
    """
    Travel Data
    """

    from_airport = row["from_airport"]
    to_airport = row["to_airport"]

    distance = AIRPORT_DISTANCE.get(
        (from_airport, to_airport),
        1000
    )

    return {
        "value": distance,
        "unit": "km",
        "scope": "SCOPE3",
        "category": "Travel"
    }


def validate_record(value):
    """
    Basic validation
    """

    errors = []

    if value < 0:
        errors.append("Negative values are not allowed")

    if value > 100000:
        errors.append("Suspiciously high value")

    return errors