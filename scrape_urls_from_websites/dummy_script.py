import pandas as pd

df = pd.read_csv('article_links.csv')

filtered_df = df[df['Status'] == 'Article']

filtered_urls = filtered_df[['Website', 'URL']]

filtered_urls.to_csv('fact_checked_article_links.csv', index=False)

print(f"Saved {len(filtered_urls)} article links to 'fact_checked_article_links.csv'.")
