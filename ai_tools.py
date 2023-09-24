from langchain.tools import BaseTool
from webbrowser import open_new_tab
from typing import Union, Optional
from webbrowser import open_new_tab
from utils import speak
import requests
import os

NotImplementedErrorMessage = 'this tool does not suport async'

class YoutubePlayer(BaseTool):
    name = "Youtube Player"
    description = "use this tool when you need to play a youtube video"
    
    def _run(self, topic: str):
        """Play a YouTube Video"""

        url = f"https://www.youtube.com/results?q={topic}"
        count = 0
        cont = requests.get(url)
        data = cont.content
        data = str(data)
        lst = data.split('"')
        for i in lst:
            count += 1
            if i == "WEB_PAGE_TYPE_WATCH":
                break
        if lst[count - 5] == "/results":
            raise Exception("No Video Found for this Topic!")

        open_new_tab(f"https://www.youtube.com{lst[count - 5]}")
        return f"https://www.youtube.com{lst[count - 5]}"
    
    def _arun(self, url: str):
        raise NotImplementedError(NotImplementedErrorMessage)

class InternetBrowser(BaseTool):
    name = "Internet Browser"
    description = "use this tool when you need to visit a website"
    def _run(self, url: str):
        return open_new_tab(url)
    
    def _arun(self, url: str):
        raise NotImplementedError(NotImplementedErrorMessage)

class AudioOutput(BaseTool):
    name = "Speak"
    description = "use this tool when you need to tell me something"
    def _run(self, text: str):
        return speak(text)
    
    def _arun(self, text: str):
        raise NotImplementedError(NotImplementedErrorMessage)

class WorldNews(BaseTool):
    name = "World News"
    categories = ["business","entertainment","general",
                  "health","science","sports","technology"]
    description = f"""
    Use this tool to fetch current news headlines.
    Only titles of the news should be presented to
    the user.
    
    Allowed categories are: {categories}
    The parameters for the news should be intuited
    from the user's query.
    
    Always convert the country to its 2-letter ISO 3166-1 code
    if the country parameter is needed before being used.
    
    Never use 'world' as a country.
    
    The results of this tool should alwasy be returned
    to the user as bullet points.
    
    :param topic (optional): The topic to search for
    :param category (optional): Category selected from categories
    :param country (optional): Country to search news from
    """
    def _run(self, topic: str = None, category: str = None, country: str = None):
        try:
            url = "https://newsapi.org/v2/top-headlines"
            params={
                "apiKey": os.getenv('NEWSAPI_API_KEY'),
                "language": "en",
                "sources": "bbc-news,the-verge,google-news",
                "pageSize": 5
            }
            
            if topic:
                params["q"] = topic
            
            if any([category, country]) and category != 'general' and country not in ('world',''):
                del params['sources']
            
                if category:
                    params["category"] = category
            
                if country:
                    params["country"] = country
            
            response = requests.get(
                url,
                params=params
            )
            
            results = response.json()
            articles = results['articles']
            headlines = [line['title'] for line in articles]
            
            return headlines
        except Exception as e:
            return f"Error: {str(e)}"
    
    def _arun(self, url: str):
        raise NotImplementedError(NotImplementedErrorMessage)

class FSBrowser(BaseTool):
    name = "File System Browser"
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
    'read', 'write', 'delete', 'execute'].
    
    The path should always be converted to absolute
    path before inputting to tool.
    
    For all operations except 'execute',
    always append the filename to the specified 
    directory.
    
    Example:
    User: create test.py on Desktop.
    
    Agent should create filename in 
    {os.path.join(os.path.expanduser('~'), 'Desktop', 'filename')}
    
    :param path: The specific path (realpath)
    :param operation: The operation to perform
    :param filename: (Optional) Name of file to create
    :param content: (Optional) Content to write to file
    """
    def _run(self, path: str, operation: str, filename: str = None, content: str = None):
        operations = {
            'open': self.execute,
            'list': self.listdir,
            # 'create': self.create_path,
            'read': self.read_path,
            'create': self.write_file,
            'write': self.write_file,
            'delete': self.delete_path
        }
        if operation in ['write', 'create']:
            return operations[operation](path, filename, content)
        elif operation == 'open':
            return operations[operation](path, filename)
        return operations[operation](path)
    
    def _arun(self, url: str):
        raise NotImplementedError(NotImplementedErrorMessage)
    
    def execute(self, path: str, filename: Optional[str])->bool:
        if filename and os.path.exists(os.path.join(path, filename)):
            os.startfile(os.path.join(path, filename))
            return True
        elif os.path.exists(path):
            os.startfile(path)
            return True
        return False
        
    def listdir(self, path: str):
        return os.listdir(path)
    
    def create_path(self, path: str):
        if os.path.isfile(path):
            with open(path, 'wt') as file:
                return file
        return os.mkdir(path)
    
    def read_path(self, path: str):
        if os.path.isfile(path):
            with open(path, 'rt') as file:
                return file.read()
        return os.listdir(path)
    
    def write_file(self, path: str, filename: str, content: Union[str, bytes]):
        with open(os.path.join(path, filename), 'w') as file:
            return file.write(content)
    
    def delete_path(self, path: str):
        return os.unlink(path)