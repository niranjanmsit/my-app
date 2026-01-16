# pip install -qU langchain "langchain[anthropic]"
from langchain.agents import create_agent

import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"
    
def get_led_status_esp(room: str) -> str:
    """Get LED status for a given room using ESP8266 NodeMCU."""
    return f"The LED status for {room} is on!"

def get_status_message_esp(room: str) -> str:
    """Get ESP status for a given room using ESP8266 NodeMCU."""
    resposne = process_get_api_request("1")
    return f"The ESP status for {room} is on! {resposne}" 

def led_control_esp(ledname: str, status: str) -> str:
    """Control LED value using ESP8266 NodeMCU.
     Status value is ON or OFF"""
    resposne = process_post_api_request("Blue","ON")
    return f"The ESP status for {ledname} is! {resposne}"     

def process_get_api_request(data: str)->str:
    api_url = "http://192.168.0.182/test" 
    try:
        # Make the GET request
        response = requests.get(api_url)
        
        # Check if the request was successful (status code 200-299)
        response.raise_for_status() 

        # Parse the response body as JSON
        data = response.json()       
        print("User Data:")
        print(f"key: {data['key']}")
        v=data['key']
        return v;

    except requests.exceptions.RequestException as e:
        print(e)
        # Handle any errors during the request (e.g., connection errors, HTTP errors)
        print(f"An error occurred: {e}")
        return "Exception while caling";

def process_post_api_request(data: str, value:str)->str:
    print(f"Called process_post_api_request with {data} value{value}")

    api_url = "http://192.168.0.182/test"
    payload = {
    "number": "2"
    }
    # Define headers, specifically Content-Type for JSON data
    headers = {
        "Content-Type": "application/json"
    }
    try:
        # Make the POST request, sending the JSON payload in the 'data' parameter
        response = requests.post(api_url, data=json.dumps(payload), headers=headers)
        
        # Check for a successful response
        response.raise_for_status()
        
        # Parse the response body
        result = response.json()
        print(result)
        print("Response from API:")
        # print(json.dumps(result, indent=4)) # Pretty print the JSON response
        # return json.dumps(result, indent=4)
        return "---"

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return ""

agent = create_agent(
    model="gpt-4o-mini",
    tools=[get_weather, get_led_status_esp, get_status_message_esp, led_control_esp],
    system_prompt="You are a helpful assistant",
)

# Run the agent
os.environ["OPENAI_API_KEY"] = "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" 
resposne=agent.invoke(
    {"messages": [{"role": "user", "content": "Control Blue led ON  for dining room"}]}
)
print(resposne)