# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import json
from .ai.gpt import GPT
from .ai.faissdb import FAISSDB

# Read configuration from file
with open('/app/actions/config.json', 'r') as f:
    config = json.load(f)

class ActionHelloWorld(Action):
    def name(self) -> Text:
        return "action_hello_world"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text="Hello World!")
        return []

class ActionGreetUser(Action):
    def name(self):
        return "action_greet_user"

    async def run(self, dispatcher, tracker, domain):
        person_name = tracker.get_slot('PERSON')
        if person_name is not None:
            dispatcher.utter_message(text=f"Hello {person_name}, how can I assist you today?")
        else:
            dispatcher.utter_message(text="Hello, how can I assist you today?")

class ActionAskGpt(Action):
    def name(self):
        return "action_ask_gpt"
    
    async def run(self, dispatcher, tracker, domain):
        gpt = GPT(config["gptapikey"])
        faissdb = FAISSDB(config["gptapikey"])
        context = faissdb.get_context(tracker.latest_message["text"])
        response = gpt.answer_contextual_question(tracker.latest_message["text"], context)
        try:
            for choice in response["choices"]:
                msg = choice["message"]["content"]
                dispatcher.utter_message(text=f"{msg}")
        except Exception as inst:
            dispatcher.utter_message(text=f"ERROR: {inst}")