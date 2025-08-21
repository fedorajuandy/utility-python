""" Upload file somewhere above the clouds """

import os
import json
import httpx
from dotenv import load_dotenv


load_dotenv()
URL_UPLOAD = os.getenv("URL_UPLOAD")


async def upload_image(file_path: str):
    """ Upload image to a server and return the response """

    if not URL_UPLOAD:
        print("No URL found in environment variable.")
        return json.dumps({
            "status": 404,
            "message": "URL not found.",
        })

    if not os.path.exists(file_path):
        print(f"Folder {file_path} not found.")
        return json.dumps({
            "status": 404,
            "message": "File not found."
        })

    try:
        with open(file_path, "rb") as image_file:
            files = {
                'image': (file_path, image_file, 'multipart/form-data')
            }

            async with httpx.AsyncClient() as client:
                response = await client.post(URL_UPLOAD, files=files)

        response.raise_for_status()

        print(f"Succesfully upload file to {URL_UPLOAD} with response: {response.json()}.")
        return json.dumps({
            "status": 201,
            "message": "File uploaded.",
            "response": response.json()
        })
    except httpx.RequestError as e:
        print(f"Request error: {e}.")
        return json.dumps({
            "status": 500,
            "message": "Request error.",
            "error": e
        })
    except httpx.HTTPStatusError as e:
        print(f"Request error: {e}.")
        return json.dumps({
            "status": e.response.status_code,
            "message": "HTTP error.",
            "error": e.response.text
        })
