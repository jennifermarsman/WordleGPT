# WordleGPT
Using the visual capabilities of GPT to solve Wordle

## Overview
This project attempts to solve a Wordle puzzle by suggesting potential next words, given a screenshot of the game.  

## Setup
This project requires access to an OpenAI resource to run the GPT-4 model with vision capabilities.  Find an API key at https://platform.openai.com/api-keys and update the "api_key" variable in the run.py file.  

Finally, use the following commands in a python environment (such as an Anaconda prompt window) to set up your environment.  This creates and activates an environment and installs the required packages.  For subsequent runs after the initial install, you will only need to activate the environment and then run the python script.  

### First run
```
conda create --name wordle python=3.9 -y
conda activate wordle

pip install -r requirements.txt
python run.py
```

### Subsequent runs
```
conda activate wordle
python run.py
```

If you are debugging, you could consider using the command "gradio run.py" instead of "python run.py" for easy reloading of your code.  See https://www.gradio.app/guides/developing-faster-with-reload-mode for more information.  

## Acknowledgements
The list of possible Wordle words (in wordle_words.txt) was obtained from https://github.com/tabatkins/wordle-list.  