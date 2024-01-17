"""
OpenAI API Experiments

This uses GTP4-V and GTP4 to OCR images from a local folder
and post process them into JSON

12 December 2023

On Windows
Then in the Terminal type
    "setx OPENAI_API_KEY <the openai key>"
FYI: To see all system environment variables,
        go to the DOS COMMAND PROMPT and type "set"

.venv\Scripts\activate
"""
import os
from timutils import *
# pip install openai
# pip install requests
from openai import OpenAI
import base64
import requests

my_api_key = os.environ["OPENAI_API_KEY"]
client = OpenAI(api_key=my_api_key)

# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

request = "Please read this hebarium sheet and extract collector and collector number, date, family, genus, species, altitude, latitude, longitude, location, country, description, language and the barcode number which begins with the letter 'K'"

image_folder = ".\\SourceImages\\"
file_list = os.listdir(image_folder)

print("####################################### START OUTPUT ######################################")
show_json(file_list)

for image_file_name in file_list:

  try:

    image_path = image_folder + image_file_name

    # Getting the base64 string
    base64_image = encode_image(image_path)

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {my_api_key}"
    }

    payload = {
        "model": "gpt-4-vision-preview",
        "messages": [
          {
            "role": "user",
            "content": [
              {"type": "text", "text": request},
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

    ocr_output = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

    print("\n########################## OCR OUTPUT " + image_path + " ##########################\n")
    input_to_json = ocr_output.json()['choices'][0]['message']['content']
    print(input_to_json)

    # Now convert to JSON
    json_output = client.chat.completions.create(
        model="gpt-4", 

        messages=[
            {"role": "system", "content": "First, delete all occurances of '\n  '. Format this as JSON where 'Collector', 'Collector number', 'Date', 'Family', 'Genus', 'Species','Altitude', 'Location', 'Latitude', 'Longitude', 'Country', 'Description' and 'Barcode number' are keys"},
            {"role": "user", "content": str(input_to_json)}
            ]
    )

    print("\n##################### JSON " + image_path + " ###############################\n")

    print(json_output.choices[0].message.content)
    print("#######################################################################################")
    print("#######################################################################################\n")
    
  except Exception as ex:
      print("Exception:", ex)

print("####################################### END OUTPUT ######################################")










