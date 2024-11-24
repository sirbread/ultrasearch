import asyncio
import aiohttp

async def async_download_image(url, filename="images/temp_image.jpg"):
    """Downloads an image asynchronously and saves it locally."""
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                with open(filename, 'wb') as file:
                    while chunk := await response.content.read(1024):
                        file.write(chunk)
                return filename
            else:
                raise Exception(f"Failed to download image. HTTP Status: {response.status}")

# Example usage
if __name__ == "__main__":
    url = "https://upload.wikimedia.org/wikipedia/en/a/a9/Example.jpg"
    asyncio.run(async_download_image(url))
