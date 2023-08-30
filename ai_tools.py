from langchain.tools import BaseTool
from pywhatkit import playonyt
from webbrowser import open_new_tab
from typing import Union
import pyttsx3
import os

NotImplementedErrorMessage = 'this tool does not suport async'

class YoutubePlayer(BaseTool):
    name = "Youtube Player"
    description = "use this tool when you need to play a youtube video"
    def _run(self, url: str):
        return playonyt(url)
    
    def _arun(self, url: str):
        raise NotImplementedError(NotImplementedErrorMessage)

class InternetBrowser(BaseTool):
    name = "Internet Browsser"
    description = "use this tool when you need to visit a website"
    def _run(self, url: str):
        return open_new_tab(url)
    
    def _arun(self, url: str):
        raise NotImplementedError(NotImplementedErrorMessage)

class AudioOutput(BaseTool):
    name = "Speak"
    description = "use this tool when you need to tell me something"
    def _run(self, text: str):
        speech_engine = pyttsx3.init()
        speech_engine.say(text)
        speech_engine.runAndWait()
        
        return True
    
    def _arun(self, text: str):
        raise NotImplementedError(NotImplementedErrorMessage)

class FSBrowser(BaseTool):
    name = "File System Browsser"
    description = f"""use this tool when you need to perform
    file system operations like listing of directories,
    opening a file, creating a file, updating a file,
    reading from a file or deleting a file.
    
    This tool is for file reads and file writes
    actions.
    
    {os.sys.platform} is the platform.
    {os.path.expanduser('~')} is the home path.
    
    The operation to perform should be in this 
    list:- ['open', 'list', 'create', 
    'read', 'write', 'delete'].
    
    The path should always be converted to absolute
    path before inputting to tool.
    
    :param path: The specific path (realpath)
    :param operation: The operation to perform
    :param filename: (Optional) Name of file to create
    :param content: (Optional) Content to write to file
    """
    def _run(self, path: str, operation: str, filename: str = None, content: str = None):
        operations = {
            'open': self.execute,
            'list': self.listdir,
            'create': self.create_path,
            'read': self.read_path,
            'write': self.write_file,
            'delete': self.delete_path
        }
        if operation == 'write':
            return operations[operation](path, filename, content)
        return operations[operation](path)
    
    def _arun(self, url: str):
        raise NotImplementedError(NotImplementedErrorMessage)
    
    def execute(self, path: str):
        return os.startfile(path)
        
    def listdir(self, path: str):
        return os.listdir(path)
    
    def create_path(self, path: str):
        if os.path.isfile(path):
            with open(path, 'wb') as file:
                return file
        return os.mkdir(path)
    
    def read_path(self, path: str):
        if os.path.isfile(path):
            with open(path, 'rt') as file:
                return file.read()
        return os.listdir(path)
    
    def write_file(self, path: str, filename, content: Union[str, bytes]):
        if os.path.isfile(path):
            with open(os.path.join(path, filename), 'wb') as file:
                return file.write(content)
        return os.mkdir(path)
    
    def delete_path(self, path: str):
        return os.unlink(path)