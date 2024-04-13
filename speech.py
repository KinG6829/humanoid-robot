import speech_recognition as sr
import requests
import pyttsx3
import datetime
import wikipedia
import nltk
from nltk.tokenize import word_tokenize
import random
import math
import json
import sys


# Initialize the text-to-speech engine
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id) 

# Initialize the speech recognition recognizer and microphone
recognizer = sr.Recognizer()
microphone = sr.Microphone()

# Initialize NLTK tokenizer
nltk.download('punkt')

# Define the chatbot model using TensorFlow
active = True  # Flag to determine if the bot is active
def chatbot(input_text):
    
    name = "alex"
    responses = {
        "alex": "Hello! How can I help you today?",
        "hi": "Hello! How can I help you today?",
        "hello": "Hello! How can I help you today?",
        "how are you": "I'm doing well, thank you for asking.",
        "how are you today": "I'm doing well, thank you for asking.",
        "tell me something about yourself": f"I'm {name}, your ai robot.",
        "who are you": f"I'm {name}, your ai robot.",
        "hu are u": f"I'm {name}, your ai robot.",
        "what is your name": f"I'm {name}.",
        "what is your age":"i dont have any physical age like you",
        "How old are you ": "i dont have any physical age like you",
        "bye": "Goodbye! Have a great day.",
        "Goodbye": "Goodbye! Have a great day.",
        "i love you": "i love too,but as a friend .",
        "i love u": "i love too,but as a friend .",
        "are you single": "i am an ai",
        "will you replace human":"no, not interested, cause they are very boaring",
        "do you replace human":"no, not interested, cause they are very boaring",
        "good bye": "Goodbye! Have a great day.",
        "thank you": "wellcome! Have a great day.",
        "thank u": "wellcome! Have a great day.",
        "thank": "wellcome! Have a great day.",
        "thanks": "wellcome! Have a great day.",
        "current time": get_time(),
        "current date": get_date(),
        "tell me a poem": get_random_poem(),
        "sing me a song": get_random_song(),
        "tell me a joke": get_random_joke(),
        "tell me a random fact":get_random_fact()
        }
    
    if "stop" in input_text.lower():
        return sleep()

    # if "no" in input_text.lower():
    #     return sleep()
    for keyword in ["good morning", "good evening", "good afternoon"]:
        if keyword in input_text.lower():
            str = "hey! "+keyword+" how can I help You today?"
            
            return str
            
    
    for keyword in ["current weather"]:
        if keyword in input_text.lower():
            return get_weather()
        
    for keyword in ["solve"]:
        if keyword in input_text.lower():
            return solve_math_problem(input_text)
        

    # for keyword in ["what is", "do you know", "who is"]:
    #    if keyword in input_text.lower():
    #     try:
    #         return responses[input_text.lower()]
    #     except KeyError:
    #         return get_wikipedia_info(input_text)
    
        
    for res in responses:
        if input_text.lower() == res :
            return responses[input_text.lower()]
        for keyword in ['search'] :
            if keyword in input_text.lower():
                return get_wikipedia_info(input_text)
        

     # If none of the keywords match, return a default response
    

      

# Function to recognize speech from microphone input   
def recognize_speech_from_mic():
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        return recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        print("Sorry, I couldn't understand that.")
        return None
    except sr.RequestError:
        print("Sorry, I couldn't request results; please check your internet connection.")
        return None

# Function to process user input using NLTK tokenizer
def process_user_input(user_input):
    tokens = word_tokenize(user_input)
    return ' '.join(tokens)


# Dictionary to store user information and context
user_data = {"sachin","bikram","surojit","suvojit"}


# Define personalized responses based on user data
personalized_responses = {
    "greet": {
        "morning": ["Good morning!", "Morning!", "Hello, good morning!"],
        "afternoon": ["Good afternoon!", "Afternoon!", "Hello, good afternoon!"],
        "evening": ["Good evening!", "Evening!", "Hello, good evening!"],
    }
}
def get_greeting_response():
    current_hour = datetime.datetime.now().hour
    if 5 <= current_hour < 12:
        return random.choice(personalized_responses["greet"]["morning"])
    elif 12 <= current_hour < 18:
        return random.choice(personalized_responses["greet"]["afternoon"])
    else:
        return random.choice(personalized_responses["greet"]["evening"])

def get_user_response(user_input):
    if any(greeting in user_input.lower() for greeting in ["good morning", "good afternoon", "good evening"]):
        return get_greeting_response()
    
    if "name" not in user_data and any(keyword in user_input.lower() for keyword in ["my name is", "i am"]):
        return get_name_response(user_input)
    return "I'm sorry, I didn't understand that."



def get_name_response(user_input):
    # Extract the user's name from the input
    name = extract_name(user_input)
    if name:
        if "name" in user_data and user_data["name"] == name:
            return "Welcome back!"
        else:
            user_data["name"] = name
            return random.choice(personalized_responses["name"]["response"]).format(name=name)
    else:
        return random.choice(personalized_responses["name"]["ask"])
   
def extract_name(user_input):
    # Use a simple keyword-based approach to extract the name
    if "my name is" in user_input.lower():
        name_index = user_input.lower().index("my name is") + len("my name is")
        name = user_input[name_index:].strip()
        return name
    elif "i am" in user_input.lower():
        name_index = user_input.lower().index("i am") + len("i am")
        name = user_input[name_index:].strip()
        return name
    else:
        return None

# Function to fetch information from Wikipedia
def get_wikipedia_info(query):
    try:
        result = wikipedia.summary(query, sentences=2)
    except wikipedia.exceptions.DisambiguationError as e:
        result = f"Did you mean: {', '.join(e.options)}"
    except wikipedia.exceptions.PageError:
        result = "Sorry, I couldn't find any information on that topic."
    return result



def get_weather():
    try:
        response = requests.get("https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/malda?unitGroup=metric&key=38Y8C6RUFAGJWJ2ZMCBP9X2FV&contentType=json")
        if response.status_code == 200:
            data = response.json()
            weather_data = data["days"][0]  # Assuming the first day's data is relevant
            weather_date = weather_data["datetime"]
            weather_temp_max = weather_data["tempmax"]
            weather_temp_min = weather_data["tempmin"]
            weather_conditions = weather_data["conditions"]
            return f"Weather for {weather_date} - Max Temp: {weather_temp_max}°C, Min Temp: {weather_temp_min}°C, Conditions: {weather_conditions}"
        else:
            return "Failed to fetch weather information."
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return "Failed to fetch weather information."



def get_time():
    current_time = datetime.datetime.now().strftime("%H:%M")
    return f"The current time is {current_time}."
def get_date():
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    return f"The current date is {current_date}."



def solve_math_problem(input_text):
    try:
        # Extract the mathematical expression after the word "solve"
        expression = input_text.split("solve")[1].strip()
        # Replace words with mathematical symbols
        expression = expression.replace("plus", "+")
        expression = expression.replace("minus", "-")
        expression = expression.replace("multiply", "*")
        expression = expression.replace("divide", "/")
        expression = expression.replace("x", "*") 
        expression = expression.replace("power", "**")  
        expression = expression.replace("exponential", "math.exp")  
        expression = expression.replace("root", "math.sqrt")  
        expression = expression.replace("cube root", "math.pow")  
        result = eval(expression)
        return f"The result of {expression} is {result}."
    except Exception as e:
        return f"Error: {e}"

    
def get_random_joke():
    response = requests.get("https://v2.jokeapi.dev/joke/Any")
    if response.status_code == 200:
        data = response.json()
        if data["type"] == "single":
            return data["joke"]
        else:
            return data["setup"] + "\n" + data["delivery"]
    else:
        return "Failed to fetch joke."

def get_random_song():
    response = requests.get("https://api.deezer.com/chart/0/tracks")
    if response.status_code == 200:
        data = response.json()
        track = random.choice(data["data"])
        return f"{track['title']} by {track['artist']['name']}"
    else:
        return "Failed to fetch song."

def get_random_poem():
    response = requests.get("https://poemist.herokuapp.com/randompoem")
    if response.status_code == 200:
        data = response.json()
        return f"{data['title']} by {data['poet']['name']}\n\n{data['content']}"
    else:
        return "Failed to fetch poem."
    
def get_random_fact():
    response = requests.get("http://numbersapi.com/random/trivia")
    if response.status_code == 200:
        return response.text
    else:
        return "Failed to fetch fact."




# Function to wake up the chatbot
def wake_up():
    
    active = True
    return "I'm awake and ready to chat!"

# Function to put the chatbot to sleep
def sleep():
    
    active = False
    return "I'm going to sleep now. Call me when you need me!"

first_time = True
is_awake = False
while True:
    
    print("Listening...")
    user_input = recognize_speech_from_mic()
    print("User input:", user_input)

    
        
    if user_input:
        
            
        
        if "wake up" in user_input.lower():
            is_awake = True
            print("Waking up...")
            response = wake_up()
            print("Bot:", response)
            engine.say(response)
            if first_time:
                res = get_greeting_response()
                engine.say(res)
                first_time = False
            engine.runAndWait()
        
        elif user_input.lower() != "weak up" and is_awake == False:
            
            str = "I am sleeping now."
            print(str)
            # engine.say(str)
        elif user_input.strip().lower() == "exit":
            print("Exiting...")
            break
        else:
            
            if is_awake:
                processed_input = process_user_input(user_input)
                response = chatbot(processed_input)
                print("Bot:", response)
                
                engine.say(response)
                engine.runAndWait()
