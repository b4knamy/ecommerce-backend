def get_related_and_valid_orders(value: str) -> str:
    """
      check value and return a valid order.
    """

    if value == "higher":
        return "-rating"

    elif value == "lower":
        return "rating"

    elif value == "older":
        return "created_at"

    elif value == "image":
        return "-has_images"

    else:
        return "-created_at"
