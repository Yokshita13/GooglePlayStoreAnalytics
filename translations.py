CATEGORY_TRANSLATIONS = {

    # Hindi
    "Beauty": "सौंदर्य",

    # Tamil
    "Business": "வணிகம்",

    # German
    "Dating": "Partnersuche",

    # French
    "Travel & Local": "Voyages et Local",

    # Spanish
    "Productivity": "Productividad",

    # Japanese
    "Photography": "写真"
}


def translate_category(category):
    """
    Returns translated category name.
    If translation is unavailable,
    returns the original category.
    """
    return CATEGORY_TRANSLATIONS.get(category, category)


def translate_dataframe(df, column="Category"):
    """
    Creates a translated category column.
    """

    df["Category_Translated"] = df[column].apply(
        translate_category
    )

    return df
