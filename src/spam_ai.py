import os
from time import sleep
from openai import OpenAI
from src.mail import Mail
from src.logger import LOGGER
from src.constants import LOGGER_SUBJECT_MAX_LENGTH, DEFAULT_MAX_ATTRIBUTE_LENGTH, DEFAULT_OPENAI_BASE_URL

class SpamAI:
  
  def __init__(self):
    LOGGER.log('Initializing OpenAI client', 3)
    self.client = OpenAI(base_url=os.getenv('OPENAI_BASE_URL', DEFAULT_OPENAI_BASE_URL))
  
  def get_email_spam_probability(self, mail: Mail) -> int:
    # We limit every string to 100 characters to avoid long prompts and reduce costs
    max_length = int(os.getenv('MAX_ATTRIBUTE_LENGTH', DEFAULT_MAX_ATTRIBUTE_LENGTH))
    prompt = f'''
    Considering only the information provided in the email below, assign a probability score representing whether it is SPAM, cold mailing, or phishing. The score should be an integer between 0 and 10, where 0 means definitely not SPAM, cold mailing, or phishing, and 10 means definitely SPAM, cold mailing, or phishing. Provide only the integer score as your response.

    Sender: '{mail.sender[:max_length]}' <{mail.sender_email}>
    Subject: {mail.subject[:max_length]}
    Email body:
    {mail.body[:max_length]}



END OF EMAIL BODY
Provide your response as a single integer.
'''
    prob = ''
    i = 0

    # The AI is impredictable, so we will try to get the probability X times
    # And we check if it's an int, if not, we try again
    while not prob.isdigit() and i < int(os.getenv('MAX_TRIES', 3)):
      # There could be random errors, so to avoid cost of infinite retries, we will use a try/finally block
      try:
        LOGGER.log(f'Requesting AI completion for email {mail.subject[:LOGGER_SUBJECT_MAX_LENGTH]} - try {i+1}', 2)
        response = self.client.completions.create(
            model = os.getenv('AI_MODEL'),
            prompt = prompt,
            max_tokens = 2,
            temperature = 0.1,
            top_p = 1,
            n = 1,
            stream = False,
        )
        prob = response.choices[0].text.strip()
        
      except Exception as e:
        LOGGER.log(f'Error requesting AI completion for email {mail.subject[:LOGGER_SUBJECT_MAX_LENGTH]} - try {i+1}: {e}')
        sleep(10)
      finally:
        i += 1


    if (not prob.isdigit()):
      raise Exception('Cannot get email SPAM score after maximum tries')

    return int(prob)
