
import streamlit as st
import os
import sys
from master import Master  # Import the Master for query handling

# Add root directory to sys.path if necessary
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Initialize the Master only once
master = Master()

def main():
    # Set up the page layout
    st.set_page_config(page_title="Academic Research Assistant", layout="wide")
    st.title("📚 Personal Research Paper Assistant")

    # Introductory description
    st.write("""
    Welcome to your Personal Research Paper Assistant. 
    Enter your query in the chat box to know about the most relevant research papers for you.
    """)

    # Initialize session states for chat history and fetched papers
    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = []

    if "fetched_papers" not in st.session_state:
        st.session_state["fetched_papers"] = []

    # Chat Input Section
    with st.form(key="chat_form"):
        st.write("### 💬 Chat with Research Q&A Bot")
        user_input = st.text_input("Ask about your research topics", key="user_input")
        submit_button = st.form_submit_button("Send")

    # Handle user input
    if submit_button and user_input:

        # Use Master to handle the user query
        response, papers = master.route_query(user_input)

        # Update papers in session state
        if papers:
            unique_papers = {paper['paper_number']: paper for paper in papers}  # Ensure uniqueness by paper number
            st.session_state["fetched_papers"] = list(unique_papers.values())
        
        # Update chat history based on Master's response
        if response:
            st.session_state["chat_history"].append(("Bot", response))
            st.session_state["chat_history"].append(("User", user_input))

        else:
            st.session_state["chat_history"].append(("Bot", "No relevant response found for your query."))

        # Clear the input field for new queries
        st.rerun()

    # Display chat history in reverse order (latest message on top)
    for sender, message in reversed(st.session_state["chat_history"]):
        if sender != "User":
            if isinstance(message, tuple):
                st.markdown(f"**🤖 Assistant**: {message[0]}")
            else:
                st.markdown(f"**🤖 Assistant**: {message}")
        else:
            st.markdown(f"**👤 User**: {message}")

    st.markdown("---")  # Divider line

    # Display list of fetched papers in the left sidebar
    with st.sidebar:
        st.write("### 📄 Fetched Research Papers")
        if st.session_state["fetched_papers"]:
            for paper in st.session_state["fetched_papers"]:
                # Display paper title, year, and download link
                clean_title = paper.get('title', '').replace('\n', ' ').strip()
                st.sidebar.markdown(f"**Title**: {clean_title}")
                st.sidebar.markdown(f"**Year**: {paper.get('year', 'N/A')}")
                download_link = paper.get('link')
                if download_link:
                    st.sidebar.markdown(f"[📥 Download PDF]({download_link})")
                else:
                    st.sidebar.markdown("No download link available.")
                st.sidebar.markdown("---")  # Separator between papers
        else:
            st.sidebar.write("No papers fetched yet. Please enter a query to get started.")

# Run the Streamlit app
if __name__ == "__main__":
    main()
