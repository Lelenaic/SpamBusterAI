# SpamBusterAI
Welcome the SpamBusterAI. This project allows you to use any OpenAI compatible AI to analyse every email you receive and mark them as SPAM depending on a SPAM Score.

Your inbox can finally be cleaned of those horrible cold mailing emails your current Anti-SPAM does not detect.

This app works well in Docker. It's privacy friendly as you can use local AI running on your computer.

Every email is just handled once, even if you restart the app (to avoid extra costs).

You can run it locally or on a cloud server (if you wanna use a local AI, you'll need a GPU or an AVX compatible CPU)

Table of contents:
- [Installation](#installation)
- [Configuration](#configuration)
- [Using SpamBusterAI with local AI on CPU/GPU](#using-local-ai-on-cpugpu)
- [Use a custom local AI model](#use-a-custom-local-ai-model)
- [Troubleshooting](#troubleshooting)



# Installation

### With docker

Download the docker-compose.yaml file:

```
curl -O https://raw.githubusercontent.com/Lelenaic/SpamBusterAI/main/docker-compose.yaml
```

Or

```
wget https://raw.githubusercontent.com/Lelenaic/SpamBusterAI/main/docker-compose.yaml
```

Then create a .env file, and fill it from the configuration section below.


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

# If you planned to use local AI on GPU, set your GPU brand here (nvidia or amd)
GPU_TYPE=
```

Then you can start SpamBusterAI:

**If you wanna use local AI, do not start SpamBusterAI, [follow the local AI tuto](#using-local-ai-on-cpugpu) first.**

Finally, start the main file:
```
# With docker
docker-compose up -d spambusterai

# Without docker
python app.py
```

# Using local AI on CPU/GPU

SpamBusterAI comes with [GPT4ALL API](https://github.com/nomic-ai/gpt4all) in the same docker-compose file. GPT4ALL allows an AI to run locally on CPU or GPU.

I've added a Makefile to make it simple.

First of all, we need to initialize GPT4ALL: `make init`

Then, in your .env, make some changes:
```
OPENAI_BASE_URL=http://gpt4all:4891/v1

# Set the model you wanna use here. It can only be a GPT4ALL model.
# To use a custom model, see the "Use a custom local AI model" section
AI_MODEL=mistral-7b-openorca.Q4_0
```
 

Then, you can run `make cpu` to run inference on your CPU or `make gpu` for the GPU version.
You'll need to wait for the model to be downloaded. Depending on your bandwith, it can take some time.

Check if the model is fully downloaded:
```
docker compose logs -f gpt4all
```

If there is an error, check your .env configuration and see the [Troubleshooting](#troubleshooting) section. 

If the model is downloaded and the GPT4ALL API server in up, you can start SpamBusterAI.


# Use a custom local AI model
If you wanna use a custom model (not provided by GPT4ALL), you can juste download a GGUF file in the ./models folder.

Then in your .env, change the `AI_MODEL` value to the file name without the `.gguf` extension.

### Example with Microsoft Phi 2 model

1. Download the model from : https://huggingface.co/TheBloke/phi-2-GGUF/blob/main/phi-2.Q4_K_M.gguf in the models folder

2. Be sure the file `phi-2.Q4_K_M.gguf` is in the models folder.

3. Change the .env variable `AI_MODEL` to `phi-2.Q4_K_M` (remove the file extension .gguf)

4. `make cpu` or `make gpu` to restart the GPT4ALL container with the new model


# Troubleshooting

### Local AI does not start

If your local model does not start, check the error logs :
```
docker compose logs -f gpt4all
```

If you see this error:
```
LLModel ERROR: CPU does not support AVX
```

You cannot run an AI on your CPU. Try the GPU version if you have one.


### Mac ARM

If you're on Mac ARM, you cannot use the docker local AI.
You'll need to download GPT4ALL from the official website, and activate the API.

1. Download it from: https://gpt4all.io/installers/gpt4all-installer-darwin.dmg
2. Got in the settings in "Application" and check the "Enable API server" box
3. In your .env, set `OPENAI_BASE_URL` to `http://host.docker.internal:4891/v1`
4. Restart SpamBusterAI
