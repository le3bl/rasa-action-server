import requests
import json
from bs4 import BeautifulSoup

class GPT:
    def __init__(self, apikey):
        self._apikey = apikey

        self._instructions = "Using the following information, generate a user story. The response should be in the formation of a User Story JSON object."

        self._story = "story: add 60/12 to education completed section of the status letter,,as state staff, i want works to include 60/12 information in the education awarded section of the status letter so as to inform the applicant of qualifying education information.acceptance criteria:1. ensure that works includes a 60/12 entry in the education awarded section of the status letter when it is checked in the applicant record. see attachment for illustration.2. ensure that works locates the 60/12 entry just above the location where eec entry/entries should be if present in the education completed section of the status letter.3. ensure that works does not include a 60/12 entry in the education awarded section of the status letter if the 60/12 option is not selected in the applicant record. note: works will check all 60/12 options in the applicant record or none of them. 4. ensure that works lists the 60/12 entry in the education completed section of the status letter as illustrated in the attachment"

        self._data = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {"role": "user", "content": f"{self._instructions}\n{self._story}"}
            ],
            "temperature": 0.5
        }
            
        self._headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {apikey}"
        }

        self._gpturi = 'https://api.openai.com/v1/chat/completions'

    def _make_req(self):
        response = requests.post(self._gpturi, data=json.dumps(self._data), headers=self._headers)
        return response.json()
    
    def answer_question(self, str):
        self._data = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {"role": "user", "content": f"answer the following quest. if you are unable simple respond with 'unable to respond':\n {str}"}
            ],
            "temperature": 0.5
        }
        return self._make_req()

    def get_keywords(self, str):
        self._data = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {"role": "user", "content": f"extract the 5 most important keywords from the following text and return only a comma delimited list of those keywords:\n {str}"}
            ],
            "temperature": 0.5
        }
        return self._make_req()
    
    def answer_contextual_question(self, question, context):

        instructions = "You are an applicant answering a QUESTION from a hiring manager. Only use information from your RESUME. If no data is provided in RESUME then respond saying you do not have experience with it but you are open to learning. The hiring manager has not seen your RESUME, so avoid referencing it in your responses.\n"
        prompt = f"{instructions}\nRESUME: {context}"

        data = {
            "model": "gpt-4",
            "messages": [
                {"role": "system", "content": f"{prompt}"},
                {"role": "user", "content": f"QUESTION: {question}"}
            ],
            "temperature": 0.2
        }
        self._data = data
        response = self._make_req()
        with open('/app/actions/log.txt', 'a') as log:
            for choice in response["choices"]:
                log.write(f'CHOICE: {choice}\n')
        return response