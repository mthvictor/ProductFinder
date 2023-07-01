from os import environ
from base64 import b64encode
from google.cloud import vision
from sys import argv

environ["GOOGLE_APPLICATION_CREDENTIALS"] = "credentials.json"


def find_similar_image_url(image_path):
    client = vision.ImageAnnotatorClient()

    with open(image_path, 'rb') as image_file:
        content = b64encode(image_file.read()).decode('UTF-8')

    image = vision.Image(content=content)
    response = client.web_detection(image=image)
    pages = response.web_detection.pages_with_matching_images

    urls = [(page.url, page.score) for page in pages]
    urls.sort(key=lambda x: x[1], reverse=True)

    return urls[0][0]


if __name__ == '__main__':
    if len(argv) != 2:
        print("Usage: python product_finder.py image_path")
        exit(1)
    print("Product URL: " + find_similar_image_url(argv[1]))
