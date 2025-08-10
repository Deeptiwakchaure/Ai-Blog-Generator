def format_func(row):
    """Format the topic and blog title for display in selectbox."""
    return f"{row['Topic']} - {row['Blog Title']}"