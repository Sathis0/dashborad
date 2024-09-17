import plotly.express as px
import pandas as pd
from metrics.calc import author_commit_statistics,commits_df,reviews_df,reviews_per_author_df,reviews_per_author,pull_requests_df,issues_df
authors_df = author_commit_statistics(commits_df)

# Create an interactive bar chart
fig = px.bar(authors_df, x='Author', y='Number of Commits', title='Number of Commits by Author')
fig.update_layout(xaxis_title='Author', yaxis_title='Number of Commits')
fig.show() 


def weekly_commit_statistics(df):
    weekly_commits = df.groupby(['Author', pd.Grouper(freq='W')]).size().reset_index(name='Number of Commits')
    return weekly_commits

weekly_commits_df = weekly_commit_statistics(commits_df)

# Create an interactive line chart
fig = px.line(weekly_commits_df, x='Date', y='Number of Commits', color='Author',
              title='Weekly Commits by Author',
              markers=True,  # Add markers to the lines
              line_shape='linear')  # Set line shape to linear

# Customize layout for better appearance
fig.update_layout(
    xaxis_title='Date',
    yaxis_title='Number of Commits',
    title={'text': 'Weekly Commits by Author', 'x': 0.5, 'xanchor': 'center'},
    legend_title='Author',
    plot_bgcolor='rgba(240, 240, 240, 0.95)',  # Light gray background for the plot area
    paper_bgcolor='rgba(255, 255, 255, 0.95)',  # Slightly off-white background for the paper area
    xaxis=dict(
        showgrid=True,  # Show gridlines
        gridcolor='rgba(200, 200, 200, 0.5)',  # Light gray gridlines
        tickangle=-45,  # Rotate x-axis labels for better readability
    ),
    yaxis=dict(
        showgrid=True,  # Show gridlines
        gridcolor='rgba(200, 200, 200, 0.5)',  # Light gray gridlines
    ),
    margin=dict(l=40, r=40, t=40, b=40)  # Adjust margins
)

fig.update_traces(
    marker=dict(size=8),  # Size of markers
    line=dict(width=2)    # Width of the lines
)

fig.show()
# Function to get unique commit messages by author
def unique_messages(df):
    unique_messages_by_author = df.groupby('Author')['Message'].apply(lambda x: pd.Series(x).unique()).reset_index()
    unique_messages_by_author['Message'] = unique_messages_by_author['Message'].apply(lambda x: ' | '.join(x))
    return unique_messages_by_author

unique_messages_df = unique_messages(commits_df)

# For simplicity, let's count unique messages
unique_messages_count = unique_messages_df['Message'].apply(lambda x: len(x.split(' | '))).reset_index()
unique_messages_count.columns = ['Author', 'Number of Unique Messages']

# Create an interactive pie chart
fig = px.pie(unique_messages_count, names='Author', values='Number of Unique Messages',
             title='Unique Commit Messages by Author')
fig.show()
# Function to get reviews per author
def reviews_per_author(reviews_df):
    reviews_per_author = reviews_df['Review Author'].value_counts().reset_index()
    reviews_per_author.columns = ['Review Author', 'Number of Reviews']
    return reviews_per_author

reviews_per_author_df = reviews_per_author(reviews_df)

# Create an interactive bar chart
fig = px.bar(reviews_per_author_df, x='Review Author', y='Number of Reviews', title='Number of Reviews by Author')
fig.update_layout(xaxis_title='Review Author', yaxis_title='Number of Reviews')
fig.show()
# Function to get user interactions
def user_interactions(commits_df, reviews_df, pull_requests_df, issues_df):
    review_authors = reviews_df['Review Author'].unique()
    commit_authors = commits_df['Author'].unique()
    issue_authors = issues_df['Author'].unique()
    pull_request_authors = pull_requests_df['Author'].unique()

    set_commit_authors = set(commit_authors)
    set_review_authors = set(review_authors)
    set_pull_request_authors = set(pull_request_authors)
    set_issue_authors = set(issue_authors)

    # Find common users between different activities
    interaction_counts = {
        'Committed and Reviewed': len(set_commit_authors.intersection(set_review_authors)),
        'Committed and PRs': len(set_commit_authors.intersection(set_pull_request_authors)),
        'Reviewed and PRs': len(set_review_authors.intersection(set_pull_request_authors)),
        'Committed and Issues': len(set_commit_authors.intersection(set_issue_authors)),
        'Reviewed and Issues': len(set_review_authors.intersection(set_issue_authors)),
        'PRs and Issues': len(set_pull_request_authors.intersection(set_issue_authors)),
        'All Activities': len(set_commit_authors.intersection(set_review_authors).intersection(set_pull_request_authors).intersection(set_issue_authors))
    }

    return interaction_counts

# Generate interaction summary
interaction_summary = user_interactions(commits_df, reviews_df, pull_requests_df, issues_df)
interaction_df = pd.DataFrame(list(interaction_summary.items()), columns=['Interaction Type', 'Number of Users'])

# Create an interactive bar chart
fig = px.bar(interaction_df, x='Interaction Type', y='Number of Users',
             title='User Interactions Across Activities',
             color='Number of Users',  # Use a color scale based on the number of users
             color_continuous_scale='Viridis')  # Choose a color scale

# Add text labels on the bars
fig.update_traces(texttemplate='%{y}', textposition='outside', marker=dict(line=dict(width=1, color='DarkSlateGrey')))

# Customize layout for better appearance
fig.update_layout(
    xaxis_title='Interaction Type',
    yaxis_title='Number of Users',
    title={'text': 'User Interactions Across Activities', 'x': 0.5, 'xanchor': 'center'},
    plot_bgcolor='rgba(240, 240, 240, 0.95)',  # Light gray background for the plot area
    paper_bgcolor='rgba(255, 255, 255, 0.95)',  # Slightly off-white background for the paper area
    xaxis=dict(
        tickangle=-45,  # Rotate x-axis labels for better readability
        title_font=dict(size=14, color='rgb(107, 107, 107)'),  # Font size and color for x-axis title
        tickfont=dict(size=12, color='rgb(107, 107, 107)'),  # Font size and color for x-axis labels
    ),
    yaxis=dict(
        title_font=dict(size=14, color='rgb(107, 107, 107)'),  # Font size and color for y-axis title
        tickfont=dict(size=12, color='rgb(107, 107, 107)'),  # Font size and color for y-axis labels
    ),
    margin=dict(l=60, r=30, t=40, b=80)  # Adjust margins to make room for labels
)

fig.show()