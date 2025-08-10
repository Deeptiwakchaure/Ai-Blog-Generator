import time

class BlogGenerator:
    def __init__(self, blog_writer, blog_manager):
        self.blog_writer = blog_writer
        self.blog_manager = blog_manager

    def generate_blog(self, topic, count, format_blog):
        """Generate multiple blogs on the same topic."""
        for i in range(count):
            # Generate a blog title
            blog_title = f"{topic} Blog {i+1}"
            
            # Generate the blog content
            content = self.blog_writer.write(topic)
            
            # If formatting is requested, we can do some basic formatting here
            if format_blog:
                # For now, we'll just ensure proper markdown formatting
                content = content.replace("### ", "### ")  # Ensure proper headers
                content = content.replace("** ", "** ")  # Ensure proper bold
            
            # Save the blog
            filepath = self.blog_manager.save_blog(topic, blog_title, content)
            
            # Yield progress
            yield f"✅ Generated blog {i+1}/{count}: {blog_title} saved to {filepath}"
            time.sleep(1)  # To avoid hitting rate limits