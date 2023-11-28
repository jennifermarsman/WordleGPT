import base64
import gradio as gr
import json
import requests

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


# OpenAI API Key
api_key = "TODO - put your OpenAI key here"

# Function to encode the image
def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

# Path to your image
image_path = "C:\Code\WordleWithGPT\images\Example3Step4.png"

def call_openai_vision_endpoint():
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
            "text": "What’s in this image?"
            },
            {
            "type": "image_url",
            "image_url": {
                "url": f"data:image/jpeg;base64,{base64_image}"
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

'''
def call_openai_vision_endpoint(prompt):
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
                "url": f"data:image/jpeg;base64,{base64_image}"
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
'''

def call_wordle_to_get_colors_openai_vision_endpoint(image_path):
    print("Image path is" + image_path)
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
                        "url": f"data:image/jpeg;base64,{example1_image}"
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
                        "url": f"data:image/jpeg;base64,{example5_image}"
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
                "url": f"data:image/jpeg;base64,{base64_image}"
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


def call_wordle_to_get_colors_openai_vision_endpoint_take2(image_path):
    prompt = "Focus on the letters in colored boxes in the center of the image.  List each letter, its position in the word, and the hexadecimal code of the color of the box it's in, and the closest color to that hex value."  
   
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
                        "url": f"data:image/jpeg;base64,{example1_image}"
                    }
                }
            ]
        },
        {
            "role": "assistant",   #TODO: Jen start here
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
                        "url": f"data:image/jpeg;base64,{example5_image}"
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
                "url": f"data:image/jpeg;base64,{base64_image}"
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


def call_wordle_to_get_colors_openai_vision_endpoint_take3(image_path):
    prompt = "Here is a new image.  Focus on the letters in colored boxes in the center of the image.  Find each green box and identify the letter within it and its position in the word.  Find each yellow box and identify the letter within it and its position in the word.  Find each dark grey box and identify the letter within it. "
   
    # Getting the base64 string
    base64_image = encode_image(image_path)

    # Few-shot examples
    example1_image = encode_image("images\\Example1Step3.png")
    example5_image = encode_image("images\\Example5Step2.png")

    # TODO: switch order of text and image?  

    # Green
    # R is 106, G is 170, B is 100, Hex is 6AAA64
    # H is 114, S is 41, V is 66.  Opacity - Alpha is 255.  

    # Yellow
    # R is 201, G is 180, B is 88, Hex is C9B458
    # H is 48, S is 56, V is 78, Opacity - Alpha is 255.  

    # Dark Grey
    # R is 120, G is 124, B is 126, Hex is 787C7E
    # H is 200, S is 4, V is 49, Opacity - Alpha is 255.  

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
                        "url": f"data:image/jpeg;base64,{example1_image}"
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
                        "url": f"data:image/jpeg;base64,{example5_image}"
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
                "url": f"data:image/jpeg;base64,{base64_image}"
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


def get_colors_openai_vision_endpoint_take4(image_path, letter):
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
                        "url": f"data:image/jpeg;base64,{example1_image}"
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
                        "url": f"data:image/jpeg;base64,{example5_image}"
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
                "url": f"data:image/jpeg;base64,{base64_image}"
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


# TODO: Bing wrote this code; probably a better way to do using regex
# Define a function that takes a string as an argument
def parse_brackets(string):
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
    character_json = call_wordle_to_get_colors_openai_vision_endpoint_take3(image_path)

    # Parse json
    character_text = character_json["choices"][0]["message"]["content"]
    print("Character text is " + character_text)

    # Parse out characters
    char_list = parse_brackets(character_text)
    #print("Character list is " + char_list)

    # Get color for each character
    summary = ""
    for letter in char_list:
        result = get_colors_openai_vision_endpoint_take4(image_path, letter)
        summary += result["choices"][0]["message"]["content"] + "\n\n"

    return summary

#{'id': 'chatcmpl-8Nnx8nBQyiZ9dqgKM2nI8aNoGaJED', 'object': 'chat.completion', 'created': 1700684254, 'model': 'gpt-4-1106-vision-preview', 'usage': {'prompt_tokens': 3900, 'completion_tokens': 54, 'total_tokens': 3954}, 'choices': [{'message': {'role': 'assistant', 'content': 'In this Wordle puzzle, the letters in green boxes are:\n- [S] in the 4th position\n\nThere are no yellow boxes in this attempt.\n\nThe letters in dark grey boxes are:\n- [R], [A], [T], [E]'}, 'finish_details': {'type': 'stop', 'stop': '<|fim_suffix|>'}, 'index': 0}]}


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
                "url": f"data:image/jpeg;base64,{base64_image}"
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
                "url": f"data:image/jpeg;base64,{base64_image}"
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



def call_wordle_base64_color_def_openai_vision_endpoint_take7(image_path):
    # TODO: add few shot back
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
                        "url": f"data:image/jpeg;base64,{example1_image}"
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
                        "url": f"data:image/jpeg;base64,{example5_image}"
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
                "url": f"data:image/jpeg;base64,{base64_image}"
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


#wordleSystemPrompt = "You are an AI assistant that helps people solve a game of Wordle and correctly guess a word with 5 letters.  You must provide suggestions of 5-letter words that could solve the Wordle puzzle, given the information you know.  Letters with a green background are correct and are in the correct position.  Letters with a yellow background are in the word, but not in the correct position.  Letters with a dark grey background are not in the word.  Provide some example words that could solve the puzzle, or suggest words with letters that haven't been used yet to determine if those other letters are in the word.  One strategy is to guess RATES, PHONY, CLIMB, and FUDGE, which contain a wide variety of letters with only one overlap. \n"
wordleAssistantPrompt = "First, focus on the letters in colored boxes in the center of the image.  List all letters in green boxes and what column they are in within their row, list which letters are in yellow boxes, and list which letters are in dark grey boxes.  \n\nThen state what we know about these letters, given the rules: Letters with a green background are correct and are in the correct position.  Letters with a yellow background are in the word, but not in the correct position.  Letters with a dark grey background are not in the word.\n\n Finally, given this information, state possible five-letter words that could solve this Wordle puzzle.  If you have 2 or less yellow or green letters, try guessing a new word with different letters to get more information. \n\n"
        
wordlePrompt = "Focus on the letters in colored boxes in the center of the image.  List all letters in green boxes and what column they are in within their row, list which letters are in yellow boxes and their position in the word, and list which letters are in dark grey boxes."
# In the image displaying a Wordle game, the following details are observed:\n\nLetters in green boxes and their column within their row:\n- U in the second column of the fourth row.\n- E in the fifth column of the fourth row.\n\nLetters in yellow boxes and their position in the word:\n- R in the first position of the first word.\n- L in the third position of the second word.\n- H in the second position of the third word.\n\nLetters in dark grey boxes:\n- A, T, S from the first word.\n- C, I, M, B from the second word.\n- P, H, O, N, Y from the third word.\n- F, D, G from the fourth word.\n\nThe green letters indicate correct letters in the correct position, the yellow letters are correct but in the wrong position, and the dark grey letters are not in the word at all.

wordlePrompt = "Focus on the letters in colored boxes in the center of the image.  List all letters in green boxes and what column they are in within their row, list which letters are in yellow boxes and their position in the word, and list which letters are in dark grey boxes."
# In the image displaying a Wordle game, the following details are observed:\n\nLetters in green boxes and their column within their row:\n- U in the second column of the fourth row.\n- E in the fifth column of the fourth row.\n\nLetters in yellow boxes and their position in the word:\n- R in the first position of the first word.\n- L in the third position of the second word.\n- H in the second position of the third word.\n\nLetters in dark grey boxes:\n- A, T, S from the first word.\n- C, I, M, B from the second word.\n- P, H, O, N, Y from the third word.\n- F, D, G from the fourth word.\n\nThe green letters indicate correct letters in the correct position, the yellow letters are correct but in the wrong position, and the dark grey letters are not in the word at all.


#call_openai_vision_endpoint()
#call_openai_vision_endpoint(wordlePrompt)
# Commenting out below for now
#call_wordle_to_get_colors_openai_vision_endpoint("images\\Example2Step3.png")



# UI using Gradio
with gr.Blocks(css=".gradio-label {color: red}") as demo:
    with gr.Row():
        with gr.Column():
            wordlePic = gr.Image(value=None, sources=["upload", "clipboard"], type="filepath", show_label=False, interactive=True, show_download_button=False)
        with gr.Column():
            txtModelOutput = gr.Textbox(label = "AI-generated output", lines=10)

    wordlePic.upload(fn=call_wordle_base64_color_def_openai_vision_endpoint_take7, inputs=wordlePic, outputs=txtModelOutput)
    #wordlePic.upload(fn=color_wrapper, inputs=wordlePic, outputs=txtModelOutput)
    #wordlePic.upload(fn=call_wordle_dense_captioning_openai_vision_endpoint_take5, inputs=wordlePic, outputs=txtModelOutput)

demo.launch()
