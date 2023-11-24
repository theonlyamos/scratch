from dotenv import load_dotenv
from spiral.agents import AIAssistant

from langchain.tools import (
    FileSearchTool,
    ReadFileTool,
    WriteFileTool,
    CopyFileTool,
    DeleteFileTool,
    ListDirectoryTool
)
from ai_tools import (
    InternetBrowser,
    YoutubePlayer,
    FSBrowser,
    AudioOutput,
    WorldNews
)

from threading import Thread
from speech import speak
import logging

load_dotenv()

class Assistant(AIAssistant):
    """
    This is an ai assitant agent created
    with spiral.
    """

    def chat(self, prompt: str, output_type='stdout'):
        try:
            # full_prompt = self.generate_prompt(prompt)
                # print(full_prompt['output'])
            # response = self.llm(full_prompt['output']) # type: ignore
            response = self.llm(prompt) # type: ignore
            # self.memory.append({'AI Assistant': response})
            
            result = self.process_response(response)
            # print(result)
            if output_type == 'audio':
                speak_thread = Thread(target=speak, args=(result,))
                speak_thread.daemon = True
                speak_thread.start()
            return result
                
        except Exception as e:
            logging.exception(e)
            # logging.error(str(e))
            
    # def add_tool(self, tool: Tool):
    #     self.tools.append(tool())
