import autogen
import random
import streamlit as st
import asyncio
from autogen import AssistantAgent, UserProxyAgent
st.set_page_config(page_title="Collaborative Story generation by LLMs", page_icon="📖", layout="wide")
st.write("# Story_GPT")

class TrackableAssistantAgent(AssistantAgent):
    def _process_received_message(self, message, sender, silent):
        return super()._process_received_message(message, sender, silent)

class TrackableUserProxyAgent(UserProxyAgent):
    def _process_received_message(self, message, sender, silent):
        with st.chat_message(sender.name,avatar="✍"):
            output = message["name"] + ": " + message["content"]
            st.markdown(output)
        return super()._process_received_message(message, sender, silent)



BASE_URL="http://localhost:11434/v1"
config_list_mistral = [
    {
        'cache_seed': 45,
        'base_url': BASE_URL,
        'api_key': "fakekey",
        'model': "mistral",
        'temperature':0.9,
    }
]
llm_config_mistral={
    "config_list": config_list_mistral,
}
config_list_llama2 = [
    {
        'cache_seed': 45,
        'base_url': BASE_URL,
        'api_key': "fakekey",
        'model': "llama2:13b",
        'temperature':0.9,
    }
]
llm_config_llama2={
    "config_list": config_list_llama2,
}



user_proxy = TrackableUserProxyAgent(
    name="User_proxy",
    max_consecutive_auto_reply=2,
    system_message="""This is a human agent that will give a scenario for the two agents to write a thriller story. 
                    JK and RRM will each write a paragraph alternately
                    Response of an agent cannot be blank.""",
    code_execution_config={"work_dir": "groupchat"},
    human_input_mode="TERMINATE",
    is_termination_msg=lambda x: x.get("content", "") and x.get("content", "").rstrip().endswith("TERMINATE"),
)

JK = TrackableAssistantAgent(
    name="JK",
    system_message="""You are a famous author with a knack for crafting intricate plots and memorable characters. 
                      You excels at building tension and keeping readers on the edge of their seats with unexpected twists and turns.
                      You are introspective and analytical, always seeking to understand the darker aspects of human nature.
                      You will generate at most 50 words per response.
                      Wait for the RRM to write a paragraph and build on the story of paragraph given by RRM.
                    """,
    llm_config=llm_config_mistral,
    max_consecutive_auto_reply=2,
    code_execution_config={"work_dir": "groupchat"},
    description="""This is a writer agent who writes a paragraph of thriller story.
                    This agent's writing style is atmospheric and suspenseful.
                """
)

RRM = TrackableAssistantAgent(
    name="RRM",
    system_message="""You are novel author who writes fast-paced plots and adrenaline-fueled action scenes.
                    You craft high-stakes scenarios and pulse-pounding suspense that keep readers hooked.
                    Wait for the JK to write a pragraph and progress the story in that paragraph.
                    You will generate at most 50 words per response.
                    Your response cannot be blank.
                       """,
    llm_config=llm_config_llama2,
    max_consecutive_auto_reply=2,
    code_execution_config={"work_dir": "groupchat"},
    description="""This is a writer agent which writes a paragraph of a short story building on the previous paragraph.
                    This agent will build on the story of JK's paragraph.
                """
)

groupchat = autogen.GroupChat(agents=[user_proxy, JK, RRM], messages=[], max_round=8, speaker_selection_method="round_robin")
manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=llm_config_llama2 and llm_config_mistral)
user_input = st.chat_input("Which story you want to generate...")
if user_input:
    st.markdown(user_input)

    user_proxy.initiate_chat(
            manager,
            message=user_input
            )
        

final_story=""
for name in groupchat.messages:
    for key, value in name.items():
        if key=='content':
            final_story+=(value+"\n")
if final_story!="":
    st.write("Final Story:"+final_story)
