import uuid
import imageio
import numpy as np
from PIL import Image
from io import BytesIO
from uuidtoimage.generate import Generate
from ipfsclient.ipfs import Ipfs


client = Ipfs()  # defaults to http://127.0.0.1:5001/api/v0
client.mkdir("CDN")

def add_uuid_images(data):
    """Parses data and adds IPFS links to images.

    For each UUID found in the data, generate an image and add it to IPFS.
    Then, add the IPFS link to the data.
    """

    uuids = [data["metadata"]["loan"]] + [schedule["paymentId"] for schedule in data["repaymentSchedule"]]

    for uuid_string in uuids:
        my_uuid = uuid.UUID(uuid_string)
        width, height = 100, 100

        image = Generate.generate_image(width, height, my_uuid)

        # Convert array to Image
        img = Image.fromarray(image.astype('uint8'))

        # Convert Image to Bytes
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)

        # Add Image to IPFS
        filename = f"{uuid_string}.png"
        cid = client.add(f"CDN/{filename}", buffer.read())

        # Add IPFS link to data
        ipfs_link = f"ipfs://{cid}"
        if uuid_string == data["metadata"]["loan"]:
            data["metadata"]["loanImageLink"] = ipfs_link
        else:
            for schedule in data["repaymentSchedule"]:
                if schedule["paymentId"] == uuid_string:
                    schedule["imageLink"] = ipfs_link
                    break

    return data
