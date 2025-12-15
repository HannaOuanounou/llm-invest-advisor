
import os
from dotenv import load_dotenv
from groq import Groq
import test_data

# Load environment variables from .env file
load_dotenv()
GROQ_API_KEY = os.getenv('GROQ_API_KEY')    

client=Groq()


def analyze_stock(ticker):
    stock_data = test_data.getStock(ticker)
    # Define the list of messages for the conversation.
    # The 'user' role is where you provide your main prompt.
    messages = [
        {
            "role": "user",
            "content": "Can you provide a brief analysis of the following stock data" + str(stock_data)+"and suggest whether it is a good investment? Here is the data: ",
        }
    ]

    # Send the request to the Groq API
    chat_completion = client.chat.completions.create(
        messages=messages,
        model="llama-3.3-70b-versatile", # Choose a model (e.g., llama-3.1-8b-instant, llama-3.1-70b-versatile)
    )

    # Print the content of the model's response
    return chat_completion.choices[0].message.content


if __name__ == "__main__":
    print(analyze_stock("AAPL"))    
    #print(analyze_stock("MSFT"))

