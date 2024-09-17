from metrics.calc import author_commit_statistics,user_interactions,commits_df,reviews_df,weekly_commit_statistics,reviews_per_author,pull_requests_df,issues_df,unique_messages
import pandas as pd
import plotly.express as px

def handle_query(query):
    query = query.lower()
    
    if 'commit statistics' in query:
        authors_df = author_commit_statistics(commits_df)
        fig = px.bar(authors_df, x='Author', y='Number of Commits', title='Number of Commits by Author')
        fig.show()
        return authors_df

    elif 'weekly commits' in query:
        weekly_commits_df = weekly_commit_statistics(commits_df)
        fig = px.line(weekly_commits_df, x='Date', y='Number of Commits', color='Author', title='Weekly Commits by Author')
        fig.show()
        return weekly_commits_df

    elif 'unique messages' in query:
        unique_messages_df = unique_messages(commits_df)
        fig = px.pie(unique_messages_df, names='Author', values='Number of Unique Messages', title='Unique Commit Messages by Author')
        fig.show()
        return unique_messages_df

    elif 'reviews per author' in query:
        reviews_per_author_df = reviews_per_author(reviews_df)
        fig = px.bar(reviews_per_author_df, x='Review Author', y='Number of Reviews', title='Number of Reviews by Author')
        fig.show()
        return reviews_per_author_df

    elif 'user interactions' in query:
        interaction_summary = user_interactions(commits_df, reviews_df, pull_requests_df, issues_df)
        interaction_df = pd.DataFrame(list(interaction_summary.items()), columns=['Interaction Type', 'Number of Users'])
        fig = px.bar(interaction_df, x='Interaction Type', y='Number of Users', title='User Interactions Across Activities')
        fig.show()
        return interaction_summary

    else:
        return "Sorry, I didn't understand the query. Please try asking about commit statistics, weekly commits, unique messages, reviews per author, or user interactions."

# Example queries
print(handle_query("Show commit statistics"))
print(handle_query("What are the weekly commits?"))
print(handle_query("List unique commit messages"))
print(handle_query("How many reviews per author?"))
print(handle_query("User interactions analysis"))