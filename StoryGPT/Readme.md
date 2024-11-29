# StoryGPT
The `story_gpt.py` script contains an implementation of a collaborative story generator using a multi-agent system. Let me explain the key aspects of this implementation in more detail.
Agents
The script defines three agents:

- TrackableUserProxyAgent: This agent represents the human user who provides the initial story prompt and receives the collaboratively generated story.
- TrackableAssistantAgent: This agent, named "JK", is responsible for generating suspenseful and atmospheric thriller story paragraphs.
- TrackableAssistantAgent: This agent, named "RRM", is responsible for generating fast-paced and action-packed story paragraphs that build on the previous paragraphs.

Each agent has a specific system message that defines its role and writing style within the collaborative story generation process.
Configuration
The script sets up two LLM configurations, one for the `mistral` model and one for the `llama2:13b` model. These configurations are used to initialize the language models for the respective agents.
Streamlit Interface
The script uses the Streamlit library to create a user-friendly web interface for the story generation process. Users can enter a story prompt, and the collaborative story is displayed as it is generated.
Story Generation
The story generation is managed by the `GroupChat` and `GroupChatManager` classes from the autogen library. The agents take turns generating story paragraphs, building on the previous ones, until the maximum number of rounds is reached.
To use the story generator:
```
# Ensure you have Python and the required dependencies installed.
pip install -r requirements.txt
# Run story_gpt.py to initiate the story generation process.
streamlit run story_gpt.py
# Enter a story prompt in the Streamlit interface.
