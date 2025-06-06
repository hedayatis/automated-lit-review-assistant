import pandas as pd
import matplotlib.pyplot as plt

# Load your CSV
df = pd.read_csv('literature_review_final.csv')

# Make sure Year is treated as a string (or int)
df['Year'] = df['Year'].astype(str)

# Count number of papers per (Year, Journal)
grouped = df.groupby(['Year', 'Journal/Book Title']).size().reset_index(name='Count')

# Pivot so that rows are Years, columns are Journals, values are Counts
pivot = grouped.pivot(index='Year', columns='Journal/Book Title', values='Count').fillna(0)

# Sort by Year (so bars appear in chronological order)
pivot = pivot.sort_index()

# Plot a stacked bar chart
ax = pivot.plot(
    kind='bar',
    stacked=True,
    figsize=(10, 6)
)
ax.set_xlabel('Year')
ax.set_ylabel('Number of Papers')
ax.set_title('Count of Papers per Journal by Year')

# Place legend outside the plot
plt.legend(title='Journal', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()
