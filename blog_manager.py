import os
import pandas as pd

class BlogManager:
    def __init__(self, directory="blogs"):
        self.directory = directory
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)

    def save_blog(self, topic, blog_title, content):
        """Save the blog content to a markdown file."""
        filename = f"{topic}_{blog_title.replace(' ', '_')}.md"
        filepath = os.path.join(self.directory, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return filepath

    def fetch_stats_for_md_files(self, directory=None):
        """Fetch statistics for all markdown files in the directory."""
        if directory is None:
            directory = self.directory
        stats = []
        for filename in os.listdir(directory):
            if filename.endswith(".md"):
                filepath = os.path.join(directory, filename)
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                # Extract topic and title from filename
                base = os.path.splitext(filename)[0]
                parts = base.split('_', 1)
                topic = parts[0]
                blog_title = parts[1].replace('_', ' ') if len(parts) > 1 else "Untitled"
                lines = content.count('\n') + 1
                words = len(content.split())
                characters = len(content)
                stats.append([topic, blog_title, lines, words, characters])
        return stats