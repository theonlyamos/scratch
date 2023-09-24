from cohere import Client

co = Client('TEgcxD2YAAkfcAEz9E1nHpEF7k8p7TKw5Yi6zowM') 
chat_history = []

if __name__ == "__main__":
    while True:
        message = input("\nEnter Query$ ")
        response = co.chat( 
            model='command-nightly',
            message= message,
            temperature=0.1,
            chat_history=chat_history,
            prompt_truncation='auto',
            stream=False,
            citation_quality='accurate',
            connectors=[{"id": "web-search"}]
        )
        chat_history.append({'user_name': 'User', 'message': message})
        chat_history.append({'user_name': 'ChatBot', 'message': response.text})
        print(response.text)