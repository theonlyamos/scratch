# Note: CLARIFAI_PAT must be set as env variable.
from clarifai.client.model import Model
from typing import Any, Dict
from pydantic import Extra,  root_validator 
from langchain.callbacks.manager import CallbackManagerForLLMRun
from langchain.llms.base import LLM
from langchain.utils import get_from_dict_or_env 
from dotenv import load_dotenv
import os

load_dotenv()

B_INST, E_INST = "[INST]", "[/INST]"
B_SYS, E_SYS = "<<SYS>>\n", "\n<</SYS>>\n\n"
DEFAULT_SYSTEM_PROMPT = """
You are a helpful, respectful and honest assistant. 
Always answer as helpfully as possible, while being safe. .


If a question does not make any sense, or is not factually coherent, 
explain why instead of answering something not corrent.

Always check your answer against the current results from the
current search tool.
Always return the most updated and correct answer.
If you do not come up with any answer, just tell me you don't know.

Never share false information
"""

def get_prompt(instruction, new_system_prompt=DEFAULT_SYSTEM_PROMPT ):
    SYSTEM_PROMPT = B_SYS + new_system_prompt + E_SYS
    prompt_template = B_INST + SYSTEM_PROMPT + instruction + E_INST
    
    return prompt_template

class ClarifaiClaudeV2(LLM):
    """Clarifai large language models.""" 
    
    model: str = "claude-v2"
    """model endpoint to use""" 

    clarifai_personal_access_token: str = os.environ["CLARIFAI_PAT"]
    """Clarifai API key""" 
    
    class Config:
        extra = Extra.forbid
    
    @root_validator()
    def validate_environment(cls, values: Dict) -> Dict:
        """Validate that the API key is set."""
        personal_access_token = get_from_dict_or_env(
            values, "clarifai_pat", "CLARIFAI_PAT"
        )
        values["clarifai_pat"] = personal_access_token
        return values
    
    @property
    def _llm_type(self) -> str:
        """Return type of LLM."""
        return self.model

    def _call(
        self,
        prompt: str,
        **kkwargs: Any,
    ) -> str:
        """Call to Clarifai endpoint."""
        try:
            instance = Model(user_id="anthropic", app_id="completion", model_id=self.model)
            
            response = instance.predict_by_bytes(get_prompt(prompt).encode('utf-8'), 'text')
            print(response)
            text = response.outputs[0].data.text.raw
            
            return text
        except Exception as e:
            return str(e)

class ClarifaiClaudeInstant(LLM):
    """Clarifai large language models.""" 
    
    model: str = "claude-instant-1_2"
    """model endpoint to use""" 

    clarifai_personal_access_token: str = os.environ["CLARIFAI_PAT"]
    """Clarifai API key""" 
    
    class Config:
        extra = Extra.forbid
    
    @root_validator()
    def validate_environment(cls, values: Dict) -> Dict:
        """Validate that the API key is set."""
        personal_access_token = get_from_dict_or_env(
            values, "clarifai_pat", "CLARIFAI_PAT"
        )
        values["clarifai_pat"] = personal_access_token
        return values
    
    @property
    def _llm_type(self) -> str:
        """Return type of LLM."""
        return self.model

    def _call(
        self,
        prompt: str,
        **kkwargs: Any,
    ) -> str:
        """Call to Clarifai endpoint."""
        try:
            instance = Model(user_id="anthropic", app_id="completion", model_id=self.model)
            
            response = instance.predict_by_bytes(get_prompt(prompt).encode('utf-8'), 'text')
            print(response)
            text = response.outputs[0].data.text.raw
            
            return text
        except Exception as e:
            return str(e)

class ClarifaiLlama2(LLM):
    """Clarifai large language models.""" 
    
    model: str = "llama2-70b-chat"
    """model endpoint to use""" 

    clarifai_personal_access_token: str = os.environ["CLARIFAI_PAT"]
    """Clarifai API key""" 
    
    class Config:
        extra = Extra.forbid
    
    @root_validator()
    def validate_environment(cls, values: Dict) -> Dict:
        """Validate that the API key is set."""
        personal_access_token = get_from_dict_or_env(
            values, "clarifai_pat", "CLARIFAI_PAT"
        )
        values["clarifai_pat"] = personal_access_token
        return values
    
    @property
    def _llm_type(self) -> str:
        """Return type of LLM."""
        return self.model

    def _call(
        self,
        prompt: str,
        **kkwargs: Any,
    ) -> str:
        """Call to Clarifai endpoint."""
        try:
            instance = Model(user_id="meta", app_id="Llama-2", model_id=self.model)
            
            response = instance.predict_by_bytes(get_prompt(prompt).encode('utf-8'), 'text')
            text = response.outputs[0].data.text.raw
            
            return text
        except Exception as e:
            return str(e)

if __name__ == "__main__":
    assistant = ClarifaiLlama2()
    while True:
        text = input("Enter query>> ")
        if text == 'exit':
            break
        response = assistant(get_prompt(text))
        print(response )