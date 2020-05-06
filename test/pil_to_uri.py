# I want access to how plotly converts a PIL.Image to something that can be
# ultimately embedded in HTML, so I'm seeing if I can use it directly here.

import PIL.Image
import plotly
from plotly.utils import ImageUriValidator
import pdb

imgf = PIL.Image.open("assets/Keymaker.jpg")
uri=ImageUriValidator.pil_image_to_uri(imgf)
pdb.set_trace()
