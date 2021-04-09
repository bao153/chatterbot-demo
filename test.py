import psutil as psu
from datetime import timedelta
from sys import argv
from time import time
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

# Get name of current program
NAME = argv[0]

# Function to write memory and cpu usage of current program
def process_info():
  for proc in psu.process_iter(['pid', 'name', 'create_time', 'cmdline', 'cpu_percent', 'cpu_times', 'num_threads', 'memory_percent']):
      if "python" in proc.info["name"] and (cl := proc.info["cmdline"]) is not None and len(cl) > 0 and NAME in cl[-1]:
        info = {
          "PID": proc.info["pid"],
          "Uptime": timedelta(seconds=time() - proc.info["create_time"]),
          "CPU in use": f"{proc.info['cpu_percent']}%",
          "Time on CPU": timedelta(seconds=proc.info["cpu_times"].system + proc.info["cpu_times"].user),
          "Num of threads": proc.info["num_threads"],
          "Memory in use": f"{(mem := proc.info['memory_percent']):.3f}%",
          "Memory usage": f"{psu.virtual_memory().total * (mem/100)/(1024**3):,.3f}GB"
        }
        print("\n\n   PROCESS INFO\n\n" + "\n".join([f"{key}: {value}" for key, value in info.items()]) + "\n\n")


# Initialize the Chatterbot
chatbot = ChatBot("MyChatbot")

# Initialize the trainer for Chatterbot
trainer = ChatterBotCorpusTrainer(chatbot)

# Arrays of strings for introducing the demo
intro = ["Chatterbot Demo",
         "="*30 + "Intro" + "="*30,
         "As you know, chatbots reside all over the Internet. In League of Legends, you can see them tasked with warning and censoring bad words that players might spout out in moments of frustration.",
         "They can also help simulate an interaction between you and a human operator or even efficiently provide quick fixes to problems that people encounter on a frequent basis.",
         "Facebook integrates a prime example of this: sometimes when you enter a relatively popular business page, a chatbot suddenly appears from the right bottom corner and asks if you need help with anything.",
         "Chatbots like those are likely to have been programmed to remember textual data including past conversations about certain topics of interest.",
         "In this demo, you will get to interact with Ironman as a chat that has been trained on his quotes. Have fun!",
         "="*30 + "Demo" + "="*30]

# Enable terminal interaction between user and demo
for i, sentence in enumerate(intro):
    while True:
        if (i == 0):
          inp = input("Enter to read more >")
          print(sentence)
          break
        else: 
          inp = input()
          print(sentence)
          break
    
inp = input("Enter to talk to Ironman >")

# Train the Chatterbot on the Ironman conversation corpus
trainer.train("./data/Ironman.json")

# Initiate conversation between user and Ironman,
# then output usage of current program after each answer
while True:
    try:
        user_input = input("Ask a question: ")
        bot_response = chatbot.get_response(user_input)
        print(bot_response)
        process_info()
        if ("bye" in user_input.lower()):
          break

    except (KeyboardInterrupt, EOFError, SystemExit):
        break

