""" Upload file somewhere above the clouds """

import httpx

async def upload_image(file_path: str):
    """ Upload image to a server and return the response """

    url = "https://cloud-photobooth.buildyourdreams.live/recieve-file-dreams"

    try:
        with open(file_path, "rb") as image_file:
            files = {'image': (file_path, image_file, 'multipart/form-data')}
            async with httpx.AsyncClient() as client:
                response = await client.post(url, files=files)

        response.raise_for_status()
        return response.json()

    except httpx.RequestError as e:
        return {"error": f"Request error: {e}"}
    except httpx.HTTPStatusError as e:
        return {"error": f"HTTP error {e.response.status_code}: {e.response.text}"}
