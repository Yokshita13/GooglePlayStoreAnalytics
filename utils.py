from datetime import datetime
import pytz
import pandas as pd
import numpy as np

# ======================================================
# CHECK IST TIME
# ======================================================

def check_time(start_hour, end_hour):
    """
    Returns True if current IST time is between
    start_hour and end_hour.
    """

    india = pytz.timezone("Asia/Kolkata")

    current_time = datetime.now(india)

    return start_hour <= current_time.hour < end_hour


# ======================================================
# CONVERT APP SIZE TO MB
# ======================================================

def convert_size(size):

    if pd.isna(size):
        return np.nan

    size = str(size)

    if size == "Varies with device":
        return np.nan

    if size.endswith("M"):
        return float(size.replace("M", ""))

    if size.endswith("k"):
        return float(size.replace("k", "")) / 1024

    return np.nan


# ======================================================
# CLEAN INSTALLS
# ======================================================

def clean_installs(installs):

    installs = str(installs)

    installs = installs.replace(",", "")

    installs = installs.replace("+", "")

    try:
        return int(installs)
    except:
        return np.nan


# ======================================================
# CLEAN PRICE
# ======================================================

def clean_price(price):

    price = str(price)

    price = price.replace("$", "")

    try:
        return float(price)
    except:
        return 0


# ======================================================
# CALCULATE REVENUE
# ======================================================

def calculate_revenue(price, installs):

    if pd.isna(price) or pd.isna(installs):
        return 0

    return price * installs


# ======================================================
# CATEGORY TRANSLATIONS
# ======================================================

def translate_category(category):

    translation = {

        "Beauty": "सौंदर्य",

        "Business": "வணிகம்",

        "Dating": "Dating (Deutsch)",

        "Travel & Local": "Voyage et Local",

        "Productivity": "Productividad",

        "Photography": "写真"

    }

    return translation.get(category, category)


# ======================================================
# APP NAME VALIDATION
# ======================================================

def has_numbers(text):

    return any(char.isdigit() for char in str(text))


def contains_letter_s(text):

    return "S" in str(text).upper()


def app_length_valid(text):

    return len(str(text)) <= 30


# ======================================================
# MONTH ORDER
# ======================================================

MONTH_ORDER = [

    "January",

    "February",

    "March",

    "April",

    "May",

    "June",

    "July",

    "August",

    "September",

    "October",

    "November",

    "December"

]