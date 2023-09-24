from cohere import Client
import logging
from typing import Any, Dict
from pydantic import Extra, root_validator
from langchain.llms.base import LLM
from langchain.utils import get_from_dict_or_env 
from dotenv import load_dotenv
import sys
import os

load_dotenv()

B_INST, E_INST = "[INST]", "[/INST]"
B_SYS, E_SYS = "<<SYS>>\n", "\n<</SYS>>\n\n"
DEFAULT_SYSTEM_PROMPT = """
You are a helpful, respectful and honest assistant. 
Always answer as helpfully as possible, while being safe. 
Your answers should not include any harmful, unethical,
racist, sexist, toxic, dangerous, or illegal content.

Please ensure your responses are socially unbiased and 
positive in nature.

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


class Coral(LLM):
    """Cohere large language models.""" 
    
    model: str = "command-nightly"
    """model endpoint to use""" 

    cohere_api_key: str = os.environ["COHERE_API_KEY"]
    """Cohere API key""" 

    temperature: float = 0.1
    """What sampling temperature to use.""" 
    
    max_tokens: int = 1024
    """The maximum number of tokens to generate in the completion.""" 
    
    client: Any

    class Config:
        extra = Extra.forbid
    
    @root_validator()
    def validate_environment(cls, values: Dict) -> Dict:
        """Validate that the API key is set."""
        api_key = get_from_dict_or_env(
            values, "cohere_api_key", "COHERE_API_KEY"
        )
        values["cohere_api_key"] = api_key
        values['client'] =  Client(api_key)
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
        """Call to Cohere endpoint."""
        
        response = self.client.chat( 
            message=get_prompt(prompt),
            model=self.model,
            temperature=self.temperature,
            prompt_truncation='auto',
            max_tokens=self.max_tokens,
            stream=False,
            citation_quality='accurate',
            connectors=[{"id": "web-search"}]
        )
        
        return response.text

if __name__ == "__main__":
    try:
        assistant = Coral()

        while True:
            prompt = input('\n[Prompt]# ')
            response = assistant(get_prompt(prompt))
            print(response)
    except KeyboardInterrupt:
        sys.exit(1)