from fastapi import FastAPI
from pydantic import BaseModel
import plotly.express as px
import pandas as pd
import json
from plotly.utils import PlotlyJSONEncoder 

app = FastAPI()

commits_df = pd.read_csv('C:/Users/sk/OneDrive/Desktop/Analytics_dashboard/data_colllection/commits.csv')
issues_df = pd.read_csv('C:/Users/sk/OneDrive/Desktop/Analytics_dashboard/data_colllection/issues.csv')
pull_requests_df = pd.read_csv('C:/Users/sk/OneDrive/Desktop/Analytics_dashboard/data_colllection/pull_requests.csv')
reviews_df = pd.read_csv('C:/Users/sk/OneDrive/Desktop/Analytics_dashboard/data_colllection/reviews.csv')

# Convert date columns to datetime
commits_df['Date'] = pd.to_datetime(commits_df['Date'])
reviews_df['Submitted At'] = pd.to_datetime(reviews_df['Submitted At'])
pull_requests_df['Created At'] = pd.to_datetime(pull_requests_df['Created At'])
issues_df['Created At'] = pd.to_datetime(issues_df['Created At'])

# Define request model
class Query(BaseModel):
    question: str

# Define response model for visualizations (plot URLs)
@app.post("/query")
async def handle_query(query: Query):
    question = query.question.lower()

    if "commit statistics" in question:
        authors_df = commits_df['Author'].value_counts().reset_index()
        authors_df.columns = ['Author', 'Number of Commits']
        fig = px.bar(authors_df, x='Author', y='Number of Commits', title='Number of Commits by Author')
        graph_json = json.dumps(fig, cls=PlotlyJSONEncoder)
        return {"graph": graph_json}

    elif "reviews per author" in question:
        reviews_per_author = reviews_df['Review Author'].value_counts().reset_index()
        reviews_per_author.columns = ['Review Author', 'Number of Reviews']
        fig = px.bar(reviews_per_author, x='Review Author', y='Number of Reviews', title='Reviews per Author')
        graph_json = json.dumps(fig, cls=PlotlyJSONEncoder)
        return {"graph": graph_json}

    else:
        return {"message": "Sorry, I didn't understand the query."}
