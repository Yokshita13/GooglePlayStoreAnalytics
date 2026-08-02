from dash import Dash
from preprocess import DataPreprocessor
from dashboard import create_dashboard
import os
import pandas as pd

excel_file = r"G:\New folder\googleplaystore\googleplaystore.csv.xlsx"

processor = DataPreprocessor(excel_file)

df = processor.preprocess()

reviews_file = "googleplaystore_user_reviews.csv"

if os.path.exists(reviews_file):
    reviews_df = pd.read_csv(reviews_file)
else:
    reviews_df = None

app = Dash(__name__)

app.title = "Google Play Store Analytics"

app.layout = create_dashboard(df, reviews_df)

if __name__ == "__main__":
    app.run(debug=True)