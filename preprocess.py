import pandas as pd
import numpy as np


class DataPreprocessor:

    def __init__(self, file_path):
        self.file_path = file_path
        self.df = None

    # -----------------------------
    # LOAD DATA
    # -----------------------------
    def load_data(self):
        self.df = pd.read_excel(self.file_path)
        print("Dataset Loaded Successfully")
        print("Shape:", self.df.shape)

    # -----------------------------
    # REMOVE DUPLICATES
    # -----------------------------
    def remove_duplicates(self):
        self.df.drop_duplicates(inplace=True)

    # -----------------------------
    # HANDLE MISSING VALUES
    # -----------------------------
    def handle_missing_values(self):
        self.df = self.df[self.df["Rating"].notna()]
        self.df = self.df[self.df["Installs"].notna()]
        self.df = self.df[self.df["Size"].notna()]

    # -----------------------------
    # CLEAN INSTALLS
    # -----------------------------
    def clean_installs(self):

        self.df["Installs"] = (
            self.df["Installs"]
            .astype(str)
            .str.replace(",", "", regex=False)
            .str.replace("+", "", regex=False)
        )

        self.df["Installs"] = pd.to_numeric(
            self.df["Installs"],
            errors="coerce"
        )

    # -----------------------------
    # CLEAN PRICE
    # -----------------------------
    def clean_price(self):

        self.df["Price"] = (
            self.df["Price"]
            .astype(str)
            .str.replace("$", "", regex=False)
        )

        self.df["Price"] = pd.to_numeric(
            self.df["Price"],
            errors="coerce"
        )

    # -----------------------------
    # CLEAN SIZE
    # -----------------------------
    def convert_size(self, value):

        if pd.isna(value):
            return np.nan

        value = str(value)

        if "M" in value:
            return float(value.replace("M", ""))

        if "k" in value:
            return float(value.replace("k", "")) / 1024

        return np.nan

    def clean_size(self):
        self.df["Size_MB"] = self.df["Size"].apply(self.convert_size)

    # -----------------------------
    # CLEAN REVIEWS
    # -----------------------------
    def clean_reviews(self):

        self.df["Reviews"] = pd.to_numeric(
            self.df["Reviews"],
            errors="coerce"
        )

    # -----------------------------
    # CLEAN RATING
    # -----------------------------
    def clean_rating(self):

        self.df["Rating"] = pd.to_numeric(
            self.df["Rating"],
            errors="coerce"
        )

    # -----------------------------
    # LAST UPDATED
    # -----------------------------
    def clean_date(self):

        self.df["Last Updated"] = pd.to_datetime(
            self.df["Last Updated"],
            errors="coerce"
        )

        self.df["Year"] = self.df["Last Updated"].dt.year
        self.df["Month"] = self.df["Last Updated"].dt.month_name()
        self.df["Month_Number"] = self.df["Last Updated"].dt.month

    # -----------------------------
    # ANDROID VERSION
    # -----------------------------
    def clean_android_version(self):

        self.df["Android Version Numeric"] = (
            self.df["Android Ver"]
            .astype(str)
            .str.extract(r"(\d+\.\d+)")
        )

        self.df["Android Version Numeric"] = pd.to_numeric(
            self.df["Android Version Numeric"],
            errors="coerce"
        )

    # -----------------------------
    # REVENUE
    # -----------------------------
    def calculate_revenue(self):

        self.df["Revenue"] = (
            self.df["Price"] *
            self.df["Installs"]
        )

    # -----------------------------
    # CATEGORY TRANSLATIONS
    # -----------------------------
    def translate_categories(self):

        self.df["Category_Translated"] = self.df["Category"]

        self.df.loc[
            self.df["Category"] == "Beauty",
            "Category_Translated"
        ] = "सौंदर्य"

        self.df.loc[
            self.df["Category"] == "Business",
            "Category_Translated"
        ] = "வணிகம்"

        self.df.loc[
            self.df["Category"] == "Dating",
            "Category_Translated"
        ] = "Dating (Deutsch)"

        self.df.loc[
            self.df["Category"] == "Travel & Local",
            "Category_Translated"
        ] = "Voyage et Local"

        self.df.loc[
            self.df["Category"] == "Productivity",
            "Category_Translated"
        ] = "Productividad"

        self.df.loc[
            self.df["Category"] == "Photography",
            "Category_Translated"
        ] = "写真"

    # -----------------------------
    # RUN ALL
    # -----------------------------
    def preprocess(self):

        self.load_data()

        self.remove_duplicates()

        self.handle_missing_values()

        self.clean_installs()

        self.clean_price()

        self.clean_size()

        self.clean_reviews()

        self.clean_rating()

        self.clean_date()

        self.clean_android_version()

        self.calculate_revenue()

        self.translate_categories()

        print("\nData Cleaning Completed")

        print(self.df.head())

        return self.df