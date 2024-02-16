# SpamBusterAI
Welcome the SpamBusterAI. This project allows you to use any OpenAI compatible AI to analyse every email you receive and mark them as SPAM depending on a SPAM Score.

Your inbox can finally be cleaned of those horrible cold mailing emails your current Anti-SPAM does not detect.

This script can be run in Docker. It's privacy friendly as you can use local AI running on your computer.

Every email is just handled once, you don't have to worry.

Table of contents:
- [Installation](#installation)
- [Configuration](#configuration)



# Installation

### With docker

Download the docker-compose.yaml file:

`curl -O https://raw.githubusercontent.com/Lelenaic/SpamBusterAI/main/docker-compose.yaml`

Or

`wget https://raw.githubusercontent.com/Lelenaic/SpamBusterAI/main/docker-compose.yaml`

Then create a .env file, and fill it from the configuration section below.

Finally, start the container : `docker-compose up -d`


### Without docker
Prerequisites:
- Python 3.9+

Clone this repository and install pip dependencies:
```
git clone https://github.com/Lelenaic/SpamBusterAI
cd SpamBusterAI

python -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
```

Then create a .env file, and fill it from the configuration section below.

Finally, start the main file : `python app.py`


# Configuration

Here's the .env.example with the documentation. Please read it carefully as some parameters can greatly improve the cost.

```
# The IMAP server username (usually your email address)
EMAIL=
# The IMAP server password (password or app password if you have 2FA)
PASSWORD=
# The IMAP server IP/hostname
HOST=
# The IMAP server Port (143 or 993 for SS/TLS)
PORT=
# Set this to false if you use port 143
TLS=true

# Which AI to use. If you wanna use ChatGPT, remove this line or set it to https://api.openai.com/v1
# Otherwise, you can set any OpenAI API compatible AI (Mistral or others)
# You can use a local AI for a privacy friendly alternative
OPENAI_BASE_URL=

# The API key, even if you're using a local AI, you need to put something here, it cannot be empty
# If you're on local AI or open AI, just leave it to "none"
OPENAI_API_KEY=none

# Which model to use? If you're on local AI, don't put the extension (.gguf or others)
AI_MODEL=

# AI is impredictable, so when we ask it the SPAM score between 0 and 10, sometimes it answers something else.
# So, if it doesn't answer a SPAM score, we can retry the same request to get only the score.
# This parameter adjusts the number of tries to get the score if the AI is hallucinating
MAX_TRIES=3

# The SPAM score is between 0 and 10 (0 = it's not a SPAM and 10 = it's a SPAM)
# The email is marked as SPAM when it's SPAM score reaches this threshold
# You can adjust the threshold if you want it to be more agressive or not
# The lower you set this number, the more likely your emails will be considered as SPAM
SPAM_THRESHOLD=8

# This is the length of the subject, sender name and email body to keep. So if you set this parameter to 100, we'll send the first 100 caracters of the email subject
# sender name and body to the AI. This parameter is important as the highest it goes, the slower and more expensive the AI will be (and the probability of hallucinations too).
# Just change this parameter if you're not satisfied of the results
MAX_ATTRIBUTE_LENGTH=100

# The log level, the higher it is, the more information there will be (can be 0 to 4)
LOG_LEVEL=1

# The run interval in seconds
# 300 means that the script will check for SPAM in your emails every 300 seconds
RUN_INTERVAL=300
```
