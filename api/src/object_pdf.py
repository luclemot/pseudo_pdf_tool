import os
import easyocr
import fitz
from typing import List


from api.src.utils import response_to_str, pdf_to_image, pseudo, pseudo_geo

from transformers import AutoTokenizer, AutoModelForTokenClassification

tokenizer = AutoTokenizer.from_pretrained("Jean-Baptiste/camembert-ner")
model = AutoModelForTokenClassification.from_pretrained("Jean-Baptiste/camembert-ner")

from transformers import pipeline

nlp = pipeline("ner", model=model, tokenizer=tokenizer, aggregation_strategy="simple")

language = "fr"
reader_ocr = easyocr.Reader([language])


class Pseudo_pdf:
    """
    Pseudo_pdf class :
    used to pseudonymize a pdf document by removing all names and or locations and replacing them with initials (resp. a blank space).
    This class has the pdf file as attribute but is not a modified pdf format.
    """

    def __init__(
        self, path_to_pdf: str, output_path: str, as_image: bool, params: dict
    ):
        """
        This class is initialized with a path to the pdf file and a path to to save the pseudonymized version pdf, and a bool.
        Having as_image as True leads to a better performance in terms of pseudonymization but takes longer to run.

        Attributes :

        path_to_pdf : path to the pdf file
        output_path : path to save the protected file
        params : dict to indicate which of people and or locations need to be pseudonymized
        as_image : bool. True if the ocr is done on a converted image file, false if the pymupdf is used to read the pdf text.
        list_pages : a list of Pseudo_page objects representing the pages from the pdf
        file : the pdf file
        """
        self.path_to_pdf = path_to_pdf
        self.output_path = output_path
        self.as_image = as_image
        self.params = params
        self.list_pages: List[Pseudo_page] = []
        self.file = fitz.open(path_to_pdf)

        self.load_content()
        self.run_ner()

    def load_content(self):
        """
        Loads the content feature of the object by applying the following steps :
        - If as_image is true, each page from the pdf is temporarily saved as a jpeg file
        and each one of these images is added to the list_pages attribute as a Pseudo_page object.
        Then the content of the page is updated.
        - Otherwise, the pymupdf module is used to update the content of each page."""
        output_str = ""
        if self.as_image:
            image_paths = pdf_to_image(self.path_to_pdf)

            for i in range(len(image_paths)):
                image_path = image_paths[i]
                self.list_pages.append(
                    Pseudo_page(
                        as_image=self.as_image, page=self.file[i], image_path=image_path
                    )
                )
                output_str += self.list_pages[i].content
        else:
            output_str = chr(12).join([page.get_text() for page in self.file])
            for i in range(len(self.file)):
                self.list_pages.append(
                    Pseudo_page(as_image=self.as_image, page=self.file[i])
                )

        self.content = output_str

    def run_ner(self):
        """
        Runs the Named Entity Recognition on the content using the CamemBert NER."""
        self.ner = nlp(self.content)

    def load_file_save(self):
        """
        Cleans the file, pseudonymizes each page and saves output file.
        It works as follows :
        - By cleaning each page from the pdf,
        - for each page in list_pages, use the pseudo_all method of Pseudo_page class.
        Then, if the PDFhas a true as_image, delete the jpeg temporary pages.
        Then, this method saves tehe pseudonymized version of the PDF in the output_path.
        """
        fitz.TOOLS.set_small_glyph_heights(True)
        for i, page in enumerate(self.file):
            page.clean_contents()
        for i, page in enumerate(self.list_pages):
            page.pseudo_all(self.ner, self.params)
            if self.as_image:
                os.remove(page.image_path)

        self.file.save(self.output_path)


class Pseudo_page:
    """
    Pseudo_page class used to represent a page from a Pseudo_pdf object's pdf file.
    """

    def __init__(self, as_image: bool, page, image_path: str = None):
        """
        The init is different based on the as_image boolean.
        If True, the ocr reader processes the image and adds the content and structure to the page's attributes.

        Attributes :

        content : the text present in the pdf
        structure : the pdf structure if as_image is true
        image_path : the path to the jpeg file is as_image is true
        page : the pdf page
        """
        if as_image:
            response = reader_ocr.readtext(image_path, detail=True)
            output_str = response_to_str(response)

            self.content: str = output_str
            self.structure = response

            self.image_path = image_path
        self.page = page

    def find_posi(self, name: str):
        """Given a name, this returns all the locations where the exact name is found."""
        posi = self.page.search_for(" " + name)
        res = []
        for rect in posi:
            text = self.page.get_textbox(rect)
            clean_text = " ".join(text.split())
            if name in clean_text:
                res.append(rect)
        return res

    def create_box_pseudo(self, rect: fitz.rect_like, pseudo_name: str):
        """Redacts the text found in the rectangle and replaces it with pseudo_name."""
        red = (1, 0, 0)
        white = (1, 1, 1)
        self.page.add_redact_annot(rect, fill=white)
        self.page.apply_redactions()
        self.page.insert_textbox(
            rect,
            pseudo_name,
            color=red,
            fontsize=10,
            fontname="Times-Roman",
            align=0,
        )
        pass

    def pseudo_all(self, file_ners: dict, params: dict):
        """
        Pseudonymizes all NERs within the file."""
        for i, ner in enumerate(file_ners):
            if ner["entity_group"] * params["PER"] == "PER":
                name = ner["word"]
                if len(name) > 1:
                    pseudo_name = pseudo(name)
                    positions = self.find_posi(name)
                    for i, posi in enumerate(positions):
                        self.create_box_pseudo(posi, pseudo_name)
            if ner["entity_group"] * params["LOC"] == "LOC":
                geo = ner["word"]
                if len(geo) > 1:
                    pseudo_loc = pseudo_geo(geo)
                    positions = self.find_posi(geo)
                    for i, posi in enumerate(positions):
                        self.create_box_pseudo(posi, pseudo_loc)


if __name__ == "__main__":
    temp = Pseudo_pdf(
        "data/example.pdf", "data/Output_trial.pdf", False, {"PER": True, "LOC": True}
    )
    temp.load_file_save()
