import streamlit as st
import pandas as pd
import os
from blog_generator import BlogGenerator
from blog_manager import BlogManager
from blog_writer import BlogWriter
from utils import format_func

# ===== EMBED YOUR API KEY HERE =====
HUGGINGFACE_API_TOKEN = "your_api"  # Replace with your token
# ==================================

st.set_page_config(
    page_title="AutoBlog: AI Blog Generator",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="auto",
    menu_items=None,
)
st.title("AI Blog Generator ✨")
st.subheader("Create hundreds of blogs using Hugging Face models")

# Initialize session state
if 'selected_model' not in st.session_state:
    st.session_state.selected_model = "microsoft/Phi-3-mini-4k-instruct"

generate_tab, blogs_tab = st.tabs(["Generate", "Blogs"])

with generate_tab:
    general_tab_container = st.container(border=True)
    
    # Model Selection
    model_options = {
        "Phi-3 (Recommended)": "microsoft/Phi-3-mini-4k-instruct",
        "Mistral-7B": "mistralai/Mistral-7B-Instruct-v0.2",
        "Zephyr-7B": "HuggingFaceH4/zephyr-7b-beta",
        "Llama-3-8B": "meta-llama/Meta-Llama-3-8B-Instruct",
        "Custom": "custom"
    }
    
    selected_model_name = general_tab_container.selectbox(
        "Select Hugging Face Model",
        options=list(model_options.keys()),
        help="Choose which model to use for generation"
    )
    
    if selected_model_name == "Custom":
        custom_model = general_tab_container.text_input(
            "Enter custom model name",
            help="Full model name from Hugging Face Hub (e.g., 'username/model-name')"
        )
        st.session_state.selected_model = custom_model
    else:
        st.session_state.selected_model = model_options[selected_model_name]
    
    # Model Recommendations
    with general_tab_container:
        st.markdown("**Recommended Models:**")
        st.markdown("- **Phi-3**: Very fast, good quality, best for most topics")
        st.markdown("- **Mistral-7B**: Good balance of speed and quality")
        st.markdown("- **Llama-3**: Highest quality, but slower")
    
    # Blog Parameters
    topic_input = general_tab_container.text_input(
        "Enter the topic for the blog",
        help="Keep the topic short and simple.",
        placeholder="eg. Next.js",
    )
    blog_count_input = general_tab_container.slider(
        "Number of blogs to generate",
        min_value=1,
        max_value=5,  # Reduced for API limits
        value=1
    )
    format_blog = general_tab_container.checkbox(
        "Format blog",
        help=(
            "Generated blog may be poorly formatted. Enable this to format the markdown properly. "
            "However, this may take longer, and the length of the blog may change."
        ),
    )
    
    # API Status Check (using embedded token)
    try:
        from huggingface_hub import InferenceClient
        client = InferenceClient(token=HUGGINGFACE_API_TOKEN)
        
        # Test with a simple chat completion
        test_messages = [{"role": "user", "content": "Hello"}]
        response = client.chat_completion(test_messages, max_tokens=5)
        
        st.success("✅ Connected to Hugging Face API")
        st.info(f"Using model: {st.session_state.selected_model}")
        
        # Get model info
        try:
            model_client = InferenceClient(model=st.session_state.selected_model, token=HUGGINGFACE_API_TOKEN)
            model_info = model_client.get_model_info()
            
            with st.expander("Model Information"):
                st.write(f"**Model:** {model_info.model_id}")
                st.write(f"**Task:** {model_info.pipeline_tag}")
                st.write(f"**Library:** {model_info.library_name}")
                st.write(f"**Likes:** {model_info.likes}")
                st.write(f"**Tags:** {', '.join(model_info.tags[:5])}")
                
        except Exception as e:
            st.warning(f"Could not fetch model info: {str(e)}")
            
    except Exception as e:
        st.error(f"⚠️ API Connection Error: {str(e)}")
        st.info("Try selecting a different model")
    
    button = general_tab_container.button("Generate")
    if button:
        if topic_input and blog_count_input:
            with st.status("Generating Blogs..."):
                blog_writer = BlogWriter(
                    model_name=st.session_state.selected_model,
                    api_token=HUGGINGFACE_API_TOKEN  # Use embedded token
                )
                blog_manager = BlogManager()
                blog_generator = BlogGenerator(blog_writer, blog_manager)
                
                for log in blog_generator.generate_blog(
                    topic_input, blog_count_input, format_blog
                ):
                    st.markdown(log)
        else:
            st.warning("Please enter a topic and number of blogs to generate")

with blogs_tab:
    # Read all the files inside the blogs folder
    blog_manager = BlogManager()
    generated_blogs = blog_manager.fetch_stats_for_md_files()
    if generated_blogs:
        df = pd.DataFrame(
            generated_blogs, columns=["Topic", "Blog Title", "Lines", "Words", "Characters"]
        )
        st.dataframe(df)
        select_box = st.selectbox(
            "Select a blog",
            df[["Topic", "Blog Title"]].apply(format_func, axis=1).tolist(),
            index=None,
            placeholder="Choose a blog from the dropdown to view it.",
        )
        if select_box is not None:
            container = st.container(border=True)
            # The select_box value is in the format "Topic - Blog Title"
            topic, blog_title = select_box.split(' - ', 1)
            filename = f"{topic}_{blog_title.replace(' ', '_')}.md"
            filepath = os.path.join(blog_manager.directory, filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                blog_content = f.read()
                container.markdown(blog_content)
    else:
        st.info("No blogs generated yet. Go to the 'Generate' tab to create some.")