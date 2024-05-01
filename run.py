import base64
import gradio as gr
import io
import json
import numpy as np
import os
import re
import requests
from PIL import Image


# OpenAI API Key
api_key = "TODO - put your OpenAI key here"


# Colors Constants

# Green
# R is 106, G is 170, B is 100, Hex is 6AAA64
# H is 114, S is 41, V is 66.  Opacity - Alpha is 255.  

# Yellow
# R is 201, G is 180, B is 88, Hex is C9B458
# H is 48, S is 56, V is 78, Opacity - Alpha is 255.  

# Dark Grey
# R is 120, G is 124, B is 126, Hex is 787C7E
# H is 200, S is 4, V is 49, Opacity - Alpha is 255.  

# Light Grey (unguessed)
# R is 211, G is 214, B is 218, Hex is D3D6DA
# H is 214, S is 3, V is 85, Opacity - Alpha is 255.  


# Helper function to encode the image
def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')


# Zero-shot prompt to call OpenAI vision endpoint
def call_openai_vision_endpoint(image_path, prompt):
    # Getting the base64 string
    base64_image = encode_image(image_path)

    headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
    }

    payload = {
    "model": "gpt-4-vision-preview",
    "messages": [
        {
        "role": "user",
        "content": [
            {
            "type": "text",
            "text": prompt
            },
            {
            "type": "image_url",
            "image_url": {
                "url": f"data:image/png;base64,{base64_image}"
            }
            }
        ]
        }
    ],
    "max_tokens": 300
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    print(response.json())
    return response.json() 


# "Hello world" prompt to describe the image
def describe_image(image_path):
    ret_val = call_openai_vision_endpoint(image_path, "What’s in this image?")
    return ret_val


# Trying few-shot learning
def extract_wordle_info_few_shot(image_path):
    prompt = "Focus on the letters in colored boxes in the center of the image.  List all letters in green boxes and what column they are in within their row, list which letters are in yellow boxes and their position in the word, and list which letters are in dark grey boxes."
   
    # Getting the base64 string
    base64_image = encode_image(image_path)

    # Few-shot examples
    example1_image = encode_image("images\\Example1Step3.png")
    example5_image = encode_image("images\\Example5Step2.png")

    headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
    }

    payload = {
    "model": "gpt-4-vision-preview",
    "messages": [
        {
            "role": "system",
            #"content": "You are an AI assistant that helps people solve a game of Wordle and correctly guess a word with 5 letters.  You must provide suggestions of 5-letter words that could solve the Wordle puzzle, given the information you know.  Letters with a green background are correct and are in the correct position.  Letters with a yellow background are in the word, but not in the correct position.  Letters with a dark grey background are not in the word.  Provide some example words that could solve the puzzle, or suggest words with letters that haven't been used yet to determine if those other letters are in the word.  One strategy is to guess RATES, PHONY, CLIMB, and FUDGE, which contain a wide variety of letters with only one overlap."
            "content": "You are a Wordle AI assistant that identifies the letters already guessed in a Wordle puzzle, what color each letter is, and what character position the letter is in the 5-character word."
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": prompt
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/png;base64,{example1_image}"
                    }
                }
            ]
        },
        {
            "role": "assistant",
            "content": """In this Wordle puzzle, the green letters are:
            - Y in the 5th position
            The yellow letters are:
            - L in the 2nd position
            - B in the 5th position
            The dark grey letters are:
            - R, A, T, E, S, C, I, M, P, H, O, N
            """
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": prompt
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/png;base64,{example5_image}"
                    }
                }
            ]
        },
        {
            "role": "assistant",
            "content": """In this Wordle puzzle, the green letters are:
            - A in the 2nd position
            - N in the 3rd position
            The yellow letters are:
            - A in the 1st position
            - D in the 3rd position
            - D in the 1st position
            - C in the 4th position
            The dark grey letters are:
            - U, I, O, E
            """
        },
        {
        "role": "user",
        "content": [
            {
            "type": "text",
            "text": prompt
            },
            {
            "type": "image_url",
            "image_url": {
                "url": f"data:image/png;base64,{base64_image}"
            }
            }
        ]
        }
    ],
    "max_tokens": 300
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    print(response.json())
    return response.json()


def extract_wordle_info_few_shot_brackets(image_path):
    prompt = "Here is a new image.  Focus on the letters in colored boxes in the center of the image.  Find each green box and identify the letter within it and its position in the word.  Find each yellow box and identify the letter within it and its position in the word.  Find each dark grey box and identify the letter within it. "
   
    # Getting the base64 string
    base64_image = encode_image(image_path)

    # Few-shot examples
    example1_image = encode_image("images\\Example1Step3.png")
    example5_image = encode_image("images\\Example5Step2.png")

    # Color definition - to try in both system and user prompt
    colorDef = "In Wordle, green is RGB value (106, 170, 100) and green is hex value #6AAA64.  Yellow is RGB value (201, 180, 88) and yellow is hex value #C9B458.  Dark grey is RGB value (120, 124, 126) and dark grey is hex value #787C7E. "

    headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
    }

    payload = {
    "model": "gpt-4-vision-preview",
    "messages": [
        {
            "role": "system",
            #"content": "You are an AI assistant that helps people solve a game of Wordle and correctly guess a word with 5 letters.  You must provide suggestions of 5-letter words that could solve the Wordle puzzle, given the information you know.  Letters with a green background are correct and are in the correct position.  Letters with a yellow background are in the word, but not in the correct position.  Letters with a dark grey background are not in the word.  Provide some example words that could solve the puzzle, or suggest words with letters that haven't been used yet to determine if those other letters are in the word.  One strategy is to guess RATES, PHONY, CLIMB, and FUDGE, which contain a wide variety of letters with only one overlap."
            "content": "You are a Wordle AI assistant that identifies the green, yellow, and dark grey letters already guessed in a Wordle puzzle, what color each letter is, and what character position the letter is in the 5-character word. " + colorDef
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": prompt
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/png;base64,{example1_image}"
                    }
                }
            ]
        },
        {
            "role": "assistant",
            "content": """In this Wordle puzzle, the letters in green boxes are:
            - [Y] in the 5th position
            The letters in yellow boxes are:
            - [L] in the 2nd position
            - [B] in the 5th position
            The letters in dark grey boxes are:
            - [R], [A], [T], [E], [S], [C], [I], [M], [P], [H], [O], [N]
            """
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": prompt
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/png;base64,{example5_image}"
                    }
                }
            ]
        },
        {
            "role": "assistant",
            "content": """In this Wordle puzzle, the letters in green boxes are:
            - [A] in the 2nd position
            - [N] in the 3rd position
            The letters in yellow boxes are:
            - [A] in the 1st position
            - [D] in the 3rd position
            - [D] in the 1st position
            - [C] in the 4th position
            The letters in dark grey boxes are:
            - [U], [I], [O], [E]
            """
        },
        {
        "role": "user",
        "content": [
            {
            "type": "text",
            "text": prompt
            },
            {
            "type": "image_url",
            "image_url": {
                "url": f"data:image/png;base64,{base64_image}"
            }
            }
        ]
        }
    ],
    "max_tokens": 300
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    print(response.json())
    return response.json()


def get_color_for_single_letter(image_path, letter):
    print("Letter is: " + letter)
    prompt = "Here is a new image.  Focus on the letters in colored boxes in the center of the image.  What color is the box behind the character \[" + letter + "\] in the image?"
    prompt2 = "Here is a new image.  Focus on the letters in colored boxes in the center of the image.  Is the color in the box behind the \[" + letter + "\] character closest to green, yellow, or dark grey?"
   
    # Getting the base64 string
    base64_image = encode_image(image_path)

    # Few-shot examples
    example1_image = encode_image("images\\Example1Step3.png")
    example5_image = encode_image("images\\Example5Step2.png")

    # Color definition - to try in both system and user prompt
    colorDef = "In Wordle, green is RGB value (106, 170, 100) and green is hex value #6AAA64.  Yellow is RGB value (201, 180, 88) and yellow is hex value #C9B458.  Dark grey is RGB value (120, 124, 126) and dark grey is hex value #787C7E. "

    headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
    }

    payload = {
    "model": "gpt-4-vision-preview",
    "messages": [
        {
            "role": "system",
            #"content": "You are an AI assistant that helps people solve a game of Wordle and correctly guess a word with 5 letters.  You must provide suggestions of 5-letter words that could solve the Wordle puzzle, given the information you know.  Letters with a green background are correct and are in the correct position.  Letters with a yellow background are in the word, but not in the correct position.  Letters with a dark grey background are not in the word.  Provide some example words that could solve the puzzle, or suggest words with letters that haven't been used yet to determine if those other letters are in the word.  One strategy is to guess RATES, PHONY, CLIMB, and FUDGE, which contain a wide variety of letters with only one overlap."
            "content": "You are a helpful assistant that can identify colors in the game of Wordle. " + colorDef
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": prompt
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/png;base64,{example1_image}"
                    }
                }
            ]
        },
        # TODO: the few shot doesn't make sense for this prompt.  I think this is wrong.  
        {
            "role": "assistant",
            "content": """In this Wordle puzzle, the letters in green boxes are:
            - [Y] in the 5th position
            The letters in yellow boxes are:
            - [L] in the 2nd position
            - [B] in the 5th position
            The letters in dark grey boxes are:
            - [R], [A], [T], [E], [S], [C], [I], [M], [P], [H], [O], [N]
            """
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": prompt
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/png;base64,{example5_image}"
                    }
                }
            ]
        },
        {
            "role": "assistant",
            "content": """In this Wordle puzzle, the letters in green boxes are:
            - [A] in the 2nd position
            - [N] in the 3rd position
            The letters in yellow boxes are:
            - [A] in the 1st position
            - [D] in the 3rd position
            - [D] in the 1st position
            - [C] in the 4th position
            The letters in dark grey boxes are:
            - [U], [I], [O], [E]
            """
        },
        {
        "role": "user",
        "content": [
            {
            "type": "text",
            "text": prompt
            },
            {
            "type": "image_url",
            "image_url": {
                "url": f"data:image/png;base64,{base64_image}"
            }
            }
        ]
        }
    ],
    "max_tokens": 100
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    print(response.json())
    return response.json() 


# Return a list of characters within square brackets from a given input string
def parse_brackets(string):
    # TODO: Bing wrote this code; probably a better way to do using regex

    # Initialize an empty list to store the letters
    letters = []
    flag = False

    # Loop through each character in the string
    for char in string:
        # If the character is an opening bracket, set a flag to True
        if char == "[":
            flag = True
        # If the character is a closing bracket, set the flag to False
        elif char == "]":
            flag = False
        # If the flag is True and the character is a letter, append it to the list
        elif flag and char.isalpha():
            letters.append(char)
            print(char)

    # Return the list of letters
    return letters


def color_wrapper(image_path):
    # Call to get the characters
    character_json = extract_wordle_info_few_shot_brackets(image_path)

    # Parse json
    character_text = character_json["choices"][0]["message"]["content"]
    print("Character text is " + character_text)

    # Parse out characters
    char_list = parse_brackets(character_text)
    #print("Character list is " + char_list)

    # Get color for each character
    summary = ""
    for letter in char_list:
        result = get_color_for_single_letter(image_path, letter)
        summary += result["choices"][0]["message"]["content"] + "\n\n"

    return summary


def call_wordle_dense_captioning_openai_vision_endpoint_take5(image_path):
    prompt = "Here is a new image.  Please follow the instructions: \n 1. Tell me the size of the input image; \n 2. Focus on the letters in colored boxes in the center of the image (not the virtual keyboard). Localize each colored box containing a letter in the center of the image using bounding box;  \n 3. Identify each colored box as green, yellow, or dark grey.  \n 4. Identify the letter or character in each box. \n 5. Identify each character's position in the word. \n"
   
    # Getting the base64 string
    base64_image = encode_image(image_path)

    # Few-shot examples
    example1_image = encode_image("images\\Example1Step3.png")
    example5_image = encode_image("images\\Example5Step2.png")

    # Color definition - to try in both system and user prompt
    colorDef = "In Wordle, green is RGB value (106, 170, 100) and green is hex value #6AAA64.  Yellow is RGB value (201, 180, 88) and yellow is hex value #C9B458.  Dark grey is RGB value (120, 124, 126) and dark grey is hex value #787C7E. "

    headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
    }

    payload = {
    "model": "gpt-4-vision-preview",
    "messages": [
        {
            "role": "system",
            "content": "You are a Wordle AI assistant that identifies the green, yellow, and dark grey letters already guessed in a Wordle puzzle, what color each letter is, and what character position the letter is in the 5-character word. " + colorDef
        },
        {
        "role": "user",
        "content": [
            {
            "type": "text",
            "text": prompt
            },
            {
            "type": "image_url",
            "image_url": {
                "url": f"data:image/png;base64,{base64_image}"
            }
            }
        ]
        }
    ],
    "max_tokens": 300
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    print(response.json())
    return response.json()


def call_wordle_base64_color_def_openai_vision_endpoint_take6(image_path):
    prompt = "Here is a new image.  Please follow the instructions: \n 1. Focus on the letters in colored boxes in the center of the image (not the virtual keyboard). Localize each colored box containing a letter in the center of the image using bounding box;  \n 3. Identify each colored box as green, yellow, or dark grey.  \n 4. Identify the letter or character in each box. \n 5. Identify each character's position in the word. \n"
   
    # Getting the base64 string
    base64_image = encode_image(image_path)

    # Few-shot examples
    example1_image = encode_image("images\\Example1Step3.png")
    example5_image = encode_image("images\\Example5Step2.png")

    # Color definition - to try in both system and user prompt
    colorDef = "In Wordle, green is RGB value (106, 170, 100), green is hex value #6AAA64, and green is base64 encoded as aqqk.  Yellow is RGB value (201, 180, 88), yellow is hex value #C9B458, and yellow is base64 encoded as y7RY.  Dark grey is RGB value (120, 124, 126), dark grey is hex value #787C7E, and dark grey is base64 encoded as eHx6. "

    headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
    }

    payload = {
    "model": "gpt-4-vision-preview",
    "messages": [
        {
            "role": "system",
            "content": "You are a Wordle AI assistant that identifies the green, yellow, and dark grey letters already guessed in a Wordle puzzle, what color each letter is, and what character position the letter is in the 5-character word. " + colorDef
        },
        {
        "role": "user",
        "content": [
            {
            "type": "text",
            "text": prompt
            },
            {
            "type": "image_url",
            "image_url": {
                "url": f"data:image/png;base64,{base64_image}"
            }
            }
        ]
        }
    ],
    "max_tokens": 500
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    print(response.json())
    return response.json()


# Few-shot version 
def call_wordle_base64_color_def_openai_vision_endpoint_take7(image_path):
    # TODO: try color def in user prompt?  
    # TODO: try asking for the color last, not second
    prompt = "Here is a new image.  Please follow the instructions: \n 1. Focus on the letters in colored boxes in the center of the image (not the virtual keyboard). \n 2. Identify each colored box as green, yellow, or dark grey.  \n 3. Identify the letter or character in each box. \n 4. Identify each character's position in the word. \n"
   
    # Getting the base64 string
    base64_image = encode_image(image_path)

    # Few-shot examples
    example1_image = encode_image("images\\Example1Step3.png")
    example5_image = encode_image("images\\Example5Step2.png")

    # Color definition - to try in both system and user prompt
    colorDef = "In Wordle, green is RGB value (106, 170, 100), green is hex value #6AAA64, and green is base64 encoded as aqqk.  Yellow is RGB value (201, 180, 88), yellow is hex value #C9B458, and yellow is base64 encoded as y7RY.  Dark grey is RGB value (120, 124, 126), dark grey is hex value #787C7E, and dark grey is base64 encoded as eHx6. "

    headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
    }

    payload = {
    "model": "gpt-4-vision-preview",
    "messages": [
        {
            "role": "system",
            "content": "You are a Wordle AI assistant that identifies the green, yellow, and dark grey letters already guessed in a Wordle puzzle, what color each letter is, and what character position the letter is in the 5-character word. " + colorDef
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": prompt
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/png;base64,{example1_image}"
                    }
                }
            ]
        },
        {
            "role": "assistant",
            "content": """In this Wordle puzzle, the letters are:
            - Dark grey [R] in position 1
            - Dark grey [A] in position 2
            - Dark grey [T] in position 3
            - Dark grey [E] in position 4
            - Dark grey [S] in position 5
            - Dark grey [C] in position 1
            - Yellow [L] in position 2
            - Dark grey [I] in position 3
            - Dark grey [M] in position 4
            - Yellow [B] in position 5
            - Dark grey [P] in position 1
            - Dark grey [H] in position 2
            - Dark grey [O] in position 3
            - Dark grey [N] in position 4
            - Green [Y] in position 5
            """
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": prompt
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/png;base64,{example5_image}"
                    }
                }
            ]
        },
        {
            "role": "assistant",
            "content": """In this Wordle puzzle, the letters are:
            - Yellow [A] in position 1
            - Dark grey [U] in position 2
            - Yellow [D] in position 3
            - Dark grey [I] in position 4
            - Dark grey [O] in position 5
            - Yellow [D] in position 1
            - Green [A] in position 2
            - Green [N] in position 3
            - Yellow [C] in position 4
            - Dark grey [E] in position 5
            """
        },

        {
        "role": "user",
        "content": [
            {
            "type": "text",
            "text": prompt
            },
            {
            "type": "image_url",
            "image_url": {
                "url": f"data:image/png;base64,{base64_image}"
            }
            }
        ]
        }
    ],
    "max_tokens": 500
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    print(response.json())
    return response.json() 


def build_prompt(letter):
    return "Here is a new image.  Focus on the letters in colored boxes in the center of the image.  Find and focus on the colored box containing the letter [" + letter + "].  Is the color in this box behind the [" + letter + "] character closest to green, yellow, or dark grey?"


def get_colors_take8(image_path, letter):
    print("Letter is: " + letter)
    #prompt = "Here is a new image.  Focus on the letters in colored boxes in the center of the image.  What color is the box behind the character \[" + letter + "\] in the image?"
    #prompt2 = "Here is a new image.  Focus on the letters in colored boxes in the center of the image.  Find and focus on the colored box containing the letter [" + letter + "].  Is the color in this box behind the [" + letter + "] character closest to green, yellow, or dark grey?"
    prompt2 = build_prompt(letter)
    single_char_prompt = "Here is one single colored box.  Is the color in the box behind the [U] character closest to green, yellow, or dark grey?"

    # Getting the base64 string
    base64_image = encode_image(image_path)

    # Few-shot examples
    green_image = encode_image("images\\Green.png")
    yellow_image = encode_image("images\\Yellow.png")
    dark_grey_image = encode_image("images\\DarkGrey.png")
    example1_image = encode_image("images\\Example1Step3.png")
    

    # Color definition - to try in both system and user prompt
    colorDef = "In Wordle, green is RGB value (106, 170, 100) and green is hex value #6AAA64.  Yellow is RGB value (201, 180, 88) and yellow is hex value #C9B458.  Dark grey is RGB value (120, 124, 126) and dark grey is hex value #787C7E. "

    headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
    }

    payload = {
    "model": "gpt-4-vision-preview",
    "messages": [
        {
            "role": "system",
            #"content": "You are an AI assistant that helps people solve a game of Wordle and correctly guess a word with 5 letters.  You must provide suggestions of 5-letter words that could solve the Wordle puzzle, given the information you know.  Letters with a green background are correct and are in the correct position.  Letters with a yellow background are in the word, but not in the correct position.  Letters with a dark grey background are not in the word.  Provide some example words that could solve the puzzle, or suggest words with letters that haven't been used yet to determine if those other letters are in the word.  One strategy is to guess RATES, PHONY, CLIMB, and FUDGE, which contain a wide variety of letters with only one overlap."
            "content": "You are a helpful assistant that can identify colors in the game of Wordle. " + colorDef
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": single_char_prompt
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/png;base64,{green_image}"
                    }
                }
            ]
        },
        {
            "role": "assistant",
            "content": "The colored box for the [U] is green"
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": single_char_prompt
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/png;base64,{yellow_image}"
                    }
                }
            ]
        },
        {
            "role": "assistant",
            "content": "The colored box for the [U] is yellow"
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": single_char_prompt
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/png;base64,{dark_grey_image}"
                    }
                }
            ]
        },
        {
            "role": "assistant",
            "content": "The colored box for the [U] is dark grey"
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": build_prompt("B")
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/png;base64,{example1_image}"
                    }
                }
            ]
        },
        {
            "role": "assistant",
            "content": "The colored box for the [B] is yellow"
        },
        {
        "role": "user",
        "content": [
            {
            "type": "text",
            "text": prompt2
            },
            {
            "type": "image_url",
            "image_url": {
                "url": f"data:image/png;base64,{base64_image}"
            }
            }
        ]
        }
    ],
    "max_tokens": 100
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    print(response.json())
    return response.json() 


def color_wrapper_2(image_path):
    # Call to get the characters
    character_json = call_wordle_base64_color_def_openai_vision_endpoint_take7(image_path)

    # Parse json
    character_text = character_json["choices"][0]["message"]["content"]
    print("Character text is " + character_text)

    # Parse out characters
    char_list = parse_brackets(character_text)
    #print("Character list is " + char_list)

    # Get color for each character
    summary = ""
    for letter in char_list:
        result = get_colors_take8(image_path, letter)
        summary += result["choices"][0]["message"]["content"] + "\n\n"

    return summary


def slice_image(image, rows, cols):
  # Load the image and get its dimensions
  img = Image.open(image)
  width, height = img.size

  # Calculate the size of each tile
  tile_width = width // cols
  tile_height = height // rows

  # Create a list to store the sliced images
  tiles = []

  # Loop through the rows and columns and crop the image
  for i in range(rows):
    for j in range(cols):
      # Define the bounding box for each tile
      left = j * tile_width
      upper = i * tile_height
      right = (j + 1) * tile_width
      lower = (i + 1) * tile_height
      box = (left, upper, right, lower)

      # Crop the image and append it to the list
      tile = img.crop(box)
      #tiles.append(tile)
      #output_file = os.path.join("images", f"tile_{i}.jpg")
      output_file = f"tile_{i}_{j}.png"
      
      # Save the tile as a PNG image
      tile.save(output_file, "PNG")
      tiles.append(output_file)

  # Return the list of sliced images
  return tiles


def get_character_and_color(single_char_image_path):
    #prompt = "Here is a new image.  Focus on the letters in colored boxes in the center of the image.  What color is the box behind the character \[" + letter + "\] in the image?"
    #prompt2 = "Here is a new image.  Focus on the letters in colored boxes in the center of the image.  Find and focus on the colored box containing the letter [" + letter + "].  Is the color in this box behind the [" + letter + "] character closest to green, yellow, or dark grey?"
    #prompt2 = build_prompt(letter)
    single_char_prompt = "Here is one single colored box from Wordle.  What letter is in the box?  Is the color in the box (behind this letter) closest to green, yellow, dark grey, or empty?  Respond in the format: [letter], color"

    # Getting the base64 string
    base64_image = encode_image(single_char_image_path)

    # Few-shot examples
    green_image = encode_image("images\\Green.png")
    yellow_image = encode_image("images\\Yellow.png")
    dark_grey_image = encode_image("images\\DarkGrey.png")
    empty_image = encode_image("images\\Empty.png")
    

    # Color definition - to try in both system and user prompt
    colorDef = "In Wordle, green is RGB value (106, 170, 100) and green is hex value #6AAA64.  Yellow is RGB value (201, 180, 88) and yellow is hex value #C9B458.  Dark grey is RGB value (120, 124, 126) and dark grey is hex value #787C7E. "

    headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
    }

    payload = {
    "model": "gpt-4-vision-preview",
    "messages": [
        {
            "role": "system",
            "content": "You are a helpful assistant that can identify colors in the game of Wordle. " + colorDef
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": single_char_prompt
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/png;base64,{green_image}"
                    }
                }
            ]
        },
        {
            "role": "assistant",
            "content": "[U], green"
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": single_char_prompt
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/png;base64,{yellow_image}"
                    }
                }
            ]
        },
        {
            "role": "assistant",
            "content": "[U], yellow"
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": single_char_prompt
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/png;base64,{dark_grey_image}"
                    }
                }
            ]
        },
        {
            "role": "assistant",
            "content": "[U], dark grey"
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": single_char_prompt
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/png;base64,{empty_image}"
                    }
                }
            ]
        },
        {
            "role": "assistant",
            "content": "Empty"
        },
        {
        "role": "user",
        "content": [
            {
            "type": "text",
            "text": single_char_prompt
            },
            {
            "type": "image_url",
            "image_url": {
                "url": f"data:image/png;base64,{base64_image}"
            }
            }
        ]
        }
    ],
    "max_tokens": 100
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    print(response.json())
    return response.json() 


def chunking_wrapper(image_path):
    # Call to break up the image
    tile_list = slice_image(image_path, 6, 5)

    # Get color for each character
    summary = ""
    for tile in tile_list:
        result = get_character_and_color(tile)
        
        # Handle error condition like API key not set
        if "error" in result:
            error_summary = "ERROR: "
            if result["error"]["code"] == "invalid_api_key":
                error_summary = error_summary + "PLEASE SET YOUR API KEY.  Open the run.py file and set the api_key variable. \n\n"
            error_summary = error_summary + json.dumps(result)
            print(error_summary)
            return error_summary
        
        # Normal path
        line_result = result["choices"][0]["message"]["content"] + "\n"
        print(line_result)
        
        # Optimization to break out of the for loop when we hit the empty tiles
        if "empty" in line_result.lower():
            break

        # Append to summary
        summary += line_result
        
    return summary


def call_model_to_get_next_word(single_char_image_path):
    #prompt = "Here is a new image.  Focus on the letters in colored boxes in the center of the image.  What color is the box behind the character \[" + letter + "\] in the image?"
    #prompt2 = "Here is a new image.  Focus on the letters in colored boxes in the center of the image.  Find and focus on the colored box containing the letter [" + letter + "].  Is the color in this box behind the [" + letter + "] character closest to green, yellow, or dark grey?"
    #prompt2 = build_prompt(letter)
    single_char_prompt = "Here is one single colored box from Wordle.  What letter is in the box?  Is the color in the box (behind this letter) closest to green, yellow, dark grey, or empty?  Respond in the format: [letter], color"

    # Getting the base64 string
    base64_image = encode_image(single_char_image_path)

    # Few-shot examples
    green_image = encode_image("images\\Green.png")
    yellow_image = encode_image("images\\Yellow.png")
    dark_grey_image = encode_image("images\\DarkGrey.png")
    empty_image = encode_image("images\\Empty.png")
    

    # Color definition - to try in both system and user prompt
    colorDef = "In Wordle, green is RGB value (106, 170, 100) and green is hex value #6AAA64.  Yellow is RGB value (201, 180, 88) and yellow is hex value #C9B458.  Dark grey is RGB value (120, 124, 126) and dark grey is hex value #787C7E. "

    headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
    }

    payload = {
    "model": "gpt-4-vision-preview",
    "messages": [
        {
            "role": "system",
            "content": "You are a helpful assistant that can identify colors in the game of Wordle. " + colorDef
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": single_char_prompt
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/png;base64,{green_image}"
                    }
                }
            ]
        },
        {
            "role": "assistant",
            "content": "[U], green"
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": single_char_prompt
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/png;base64,{yellow_image}"
                    }
                }
            ]
        },
        {
            "role": "assistant",
            "content": "[U], yellow"
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": single_char_prompt
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/png;base64,{dark_grey_image}"
                    }
                }
            ]
        },
        {
            "role": "assistant",
            "content": "[U], dark grey"
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": single_char_prompt
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/png;base64,{empty_image}"
                    }
                }
            ]
        },
        {
            "role": "assistant",
            "content": "Empty"
        },
        {
        "role": "user",
        "content": [
            {
            "type": "text",
            "text": single_char_prompt
            },
            {
            "type": "image_url",
            "image_url": {
                "url": f"data:image/png;base64,{base64_image}"
            }
            }
        ]
        }
    ],
    "max_tokens": 100
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    print(response.json())
    return response.json() 


def wrapper_4(image_path):
    summary = chunking_wrapper(image_path)

    if summary.startswith("ERROR"):
        return summary
    
    #print("Don't forget you are hardcoding rn")
    '''
    summary = """[R], dark grey
[A], dark grey
[T], dark grey
[E], dark grey
[S], dark grey
[C], dark grey
[L], yellow
[I], dark grey
[M], dark grey
[B], yellow
[P], dark grey
[H], dark grey
[O], dark grey
[N], dark grey
[Y], green"""
'''


    print("Summary")
    print(summary)
    lines = io.StringIO(summary)
    print("Lines")
    print(lines)

    # Create an empty structured array for the 5 positions in the word
    dtype = [('index', int), ('list', object)]
    position_no = np.empty(5, dtype=dtype)   
    # Assign custom index values and dynamic lists to each row
    position_no['index'] = [0, 1, 2, 3, 4]
    position_no['list'] = [[],[],[],[],[]]

    position_yes = np.array([".", ".", ".", ".","."])
    dark_grey = []
    yellow = []
    position = 0

    # Parse each line (and this is making assumption of them being in order, which the model seems to do consistently)
    for line in lines.readlines():
        print("line is " + line)
        # Use regular expressions to find the letter and the color
       
        # Extract letter/character
        match = re.search(r"\[(.*?)\]", line)
        if match:
            letter = match.group(1)
        else:
            print("No letter match found")

        # Extract color
        match = re.search(r",\s*(.*)", line)
        if match:
            color = match.group(1)
        else:
            print("No color match found")
        
        # Confirm we did it for debugging 
        print("letter is " + letter)
        print ("color is " + color)

        letter = letter.lower()

        if color == "green":
            position_yes[position] = letter
        elif color == "yellow":
            position_no["list"][position].append(letter)
            yellow.append(letter)
        elif color == "dark grey":
            dark_grey.append(letter)

        position += 1
        if position > 4: 
            position = 0

        
    # Debug check after for loop
    print("Position yes")
    print (position_yes)
    print("Position no")
    print (position_no)    
    print("Yellow")
    print (yellow)    
    print("Dark Grey")
    print (dark_grey)

    # Build regular expression to get words that would work
    my_reg_ex = ""
    green_letter_count = 0
    not_in_all = "".join(dark_grey)
    for position in range(0, 5):
        print("Position is " + str(position))
        if position_yes[position] != ".":  # we have a green letter for this position
            my_reg_ex += "[" + position_yes[position] + "]"
            green_letter_count += 1
        else:
            my_reg_ex += r"[^"
            if len(position_no["list"][position]) > 0:
                my_reg_ex += "".join(position_no["list"][position])
            if dark_grey != []:
                my_reg_ex += not_in_all
            if my_reg_ex == "[^":
                my_reg_ex = "[a-z]"
                print("This should never happen.")
            else:
                my_reg_ex += "]"
        print("RegEx is " + my_reg_ex)

    # Exit early if we are done
    if green_letter_count == 5:
        return "You won!  The word is " + my_reg_ex.replace("[", "").replace("]", "").upper()

    # Run regular expression on Wordle list
    with open("wordle_words.txt", "r") as f:
        # Read the file content as a string
        text = f.read()

        # Find all the matches of the regex in the text
        matches = re.findall("[a-z][a-z][a-z][a-z][a-z]", text)     # match on lower-case 5-letter words first
        matches2 = list(filter(lambda m: re.findall(my_reg_ex, m), matches)) # then exclude based on color specifics

    # Confirm all yellow letters are present
    valid_words = []
    yellow_set = set(yellow)

    # Iterate over the matches
    for match in matches2:
        # Convert the match to a set
        match_set = set(match)

        # Check if the yellow list is a subset of the match set
        if yellow_set.issubset(match_set):
            valid_words.append(match)

    # Return appropriate options
    return "Some valid words to guess are: " + " ".join(valid_words).upper()



# UI using Gradio
with gr.Blocks() as demo:
    with gr.Row():
        with gr.Column():
            wordlePic = gr.Image(value=None, sources=["upload", "clipboard"], type="filepath", show_label=False, interactive=True, show_download_button=False)
        with gr.Column():
            txtModelOutput = gr.Textbox(label = "AI-generated output", lines=10)

    #wordlePic.upload(fn=describe_image, inputs=wordlePic, outputs=txtModelOutput)
    #wordlePic.upload(fn=extract_wordle_info_few_shot, inputs=wordlePic, outputs=txtModelOutput)
    #wordlePic.upload(fn=extract_wordle_info_few_shot_brackets, inputs=wordlePic, outputs=txtModelOutput)
    #wordlePic.upload(fn=color_wrapper, inputs=wordlePic, outputs=txtModelOutput)
    #wordlePic.upload(fn=call_wordle_dense_captioning_openai_vision_endpoint_take5, inputs=wordlePic, outputs=txtModelOutput)
    #wordlePic.upload(fn=chunking_wrapper, inputs=wordlePic, outputs=txtModelOutput)
    #wordlePic.upload(fn=call_wordle_base64_color_def_openai_vision_endpoint_take7, inputs=wordlePic, outputs=txtModelOutput)
    wordlePic.upload(fn=wrapper_4, inputs=wordlePic, outputs=txtModelOutput)
    
demo.launch()
