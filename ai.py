from dotenv import load_dotenv
from langchain.llms import Cohere
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.agents import Tool
from langchain.agents import AgentType
from langchain.utilities import SerpAPIWrapper
from langchain.agents import initialize_agent
from langchain.memory import ConversationBufferMemory
from langchain.prompts.chat import (
    MessagesPlaceholder,
)
from ai_tools import (
    InternetBrowser,
    YoutubePlayer,
    FSBrowser,
    AudioOutput
)

load_dotenv()

class AIAssistant():
    """
    This is an ai assitant agent created
    with lanchain.
    """
    
    def __init__(self) -> None:
        self.initialize()
    
    def initialize(self):
        self.llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0613", max_tokens=1000)
        # self.llm = Cohere(model="command-nightly", temperature=0)

        search = SerpAPIWrapper()
        self.tools = [
            Tool(
                name = "Current Search",
                func=search.run,
                description="useful for when you need to answer questions about current events or the current state of the world"
            ),
            Tool(
                name = "Youtube Search",
                func=search.run,
                description="useful for when you want to search on youtube"
            ),
            YoutubePlayer(),
            InternetBrowser(),
            FSBrowser(),
            AudioOutput()
        ]
        
        self.chat_history = MessagesPlaceholder(variable_name="chat_history")
        self.memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
        
        self.agent_chain = initialize_agent(
            self.tools, 
            self.llm, 
            agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION, 
            verbose=False, 
            memory=self.memory,
            max_iterations=3,
            early_stopping_method='generate',
            agent_kwargs = {
                "memory_prompts": [self.chat_history],
                "input_variables": ["input", "agent_scratchpad", "chat_history"]
            }
        )
    
    def chat(self, prompt: str):
        result = self.agent_chain.run(input=prompt)
        print(result)
    
    def add_tool(self, tool: Tool):
        self.tools.append(tool())

if __name__ == "__main__":
    assistant = AIAssistant()