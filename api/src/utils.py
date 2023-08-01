from wand.image import Image


def pseudo(name: str) -> str:
    """
    input : name, a str
    output : pseudo_name, a peunonymized string of name"""
    pseudo_name = ""
    for x in name.split():
        pseudo_name += " " + x[0]
    return pseudo_name


def pseudo_geo(geo: str) -> str:
    """
    intput : geo, a str
    output : the pseudonymized version of geo, here an empty string"""
    return ""


def response_to_str(obj) -> str:
    """
    intput : obj, a pdf response structure
    output : the stirng contained in response structure"""
    str = ""
    for i, x in enumerate(obj):
        str += x[1] + " "
    return str


def pdf_to_image(f) -> list:
    """
    intput : f, a pdf file
    output : list of paths to jpeg files representing pages in pdf file"""
    L = []
    with Image(filename=f, resolution=200) as source:
        for i, image in enumerate(source.sequence):
            newfilename = f.removesuffix(".pdf") + str(i + 1) + ".jpeg"
            Image(image).save(filename=newfilename)
            L.append(newfilename)
    return L


def coordinates_from_points(position: list) -> list:
    """
    input : position in easyocr format, list
    output : list of 4 coordinates for a rectangle"""
    return [
        position[0][0] / 2.8,
        position[0][1] / 2.8,
        position[2][0] / 2.8,
        position[2][1] / 2.8,
    ]
