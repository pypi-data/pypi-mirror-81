import typing
import zipfile
from lxml import etree as tree
from .models import Book
from .utils import slice_image
import weasyprint
import os

COVER_PATH = "OEBPS/assets/cover"
CHAPTER_BASE_TITLE = "ch"

CONTENT_PATH = "{user_path}/OEBPS"
CHAPTERS_PATH = "{user_path}/chapters"

MAIN_BOOK_DATA = ["identifier", "title", "creator", "date", "language"]


class EasyEpubException(BaseException):
    pass


class EasyEpub:
    def __init__(self, book: typing.Optional[str]):
        self.book = book
        self.parser = Parser(self.book)

    @property
    def meta(self) -> Book:
        """
        :return: returns dictionary with a book metadata.
        """
        return Book(**self.parser.get_book_meta())

    def get_cover(self, path: str) -> str:
        """
        :param path: save path for a cover image.
        :return: returns path to the saved file.
        """
        return Parser(self.book).get_book_cover(path)

    def get_content(self, path: str) -> str:
        """
        :param path: save path for content.
        :return: returns path to the saved chapters.
        """
        return Prepare(Parser(self.book).get_book_content(path)).html_to_png()


class Parser:
    def __init__(self, book: str):
        """
        :param book: string path object to
        """
        self.book = book

    def get_book_meta(self) -> typing.Dict[str, str]:
        """
        :return: returns dictionary with a book metadata.
        """
        namespaces = {
            "n": "urn:oasis:names:tc:opendocument:xmlns:container",
            "pkg": "http://www.idpf.org/2007/opf",
            "dc": "http://purl.org/dc/elements/1.1/",
        }
        opened_book = zipfile.ZipFile(self.book)
        meta = tree.fromstring(opened_book.read("META-INF/container.xml")).xpath(
            "n:rootfiles/n:rootfile/@full-path", namespaces=namespaces
        )[0]
        opened_meta = opened_book.read(meta)
        book_data = tree.fromstring(opened_meta).xpath(
            "/pkg:package/pkg:metadata", namespaces=namespaces
        )[0]

        received_data = {}
        for selected in MAIN_BOOK_DATA:
            received_data[selected] = book_data.xpath(
                f"dc:{selected}/text()", namespaces=namespaces
            )[0]
        zipfile.ZipFile.close(opened_book)

        return {
            "uid": received_data["identifier"],
            "title": received_data["title"],
            "author": received_data["creator"],
            "creation_date": received_data["date"],
            "language": received_data["language"],
        }

    def get_book_cover(self, path: str) -> str:
        """
        :param path: save path for a cover image.
        :return: returns path to the saved file.
        """
        opened_book = zipfile.ZipFile(self.book)

        book_covers = list(
            filter(lambda title: title.startswith(COVER_PATH), opened_book.namelist())
        )
        if not book_covers:
            raise EasyEpubException("Can't find a cover in this book.")

        directory_name = os.path.dirname(path)
        if directory_name:
            os.makedirs(directory_name, exist_ok=True)
        with open(path, "wb") as book:
            book.write(opened_book.read(book_covers[0]))
        opened_book.close()
        return os.path.abspath(path)

    def get_book_content(self, path: str) -> str:
        """
        :param path: save path for content.
        :return: returns path to the saved chapters.
        """
        with zipfile.ZipFile(self.book) as opened_book:
            opened_book.extractall(path)

        return os.path.abspath(path)


class Prepare:
    def __init__(self, path: str):
        self.path = path

    def html_to_png(self) -> str:
        chapters_path = CHAPTERS_PATH.format(user_path=self.path)

        os.makedirs(chapters_path, exist_ok=True)
        content_path = CONTENT_PATH.format(user_path=self.path)
        if not content_path:
            raise EasyEpubException("Book does not prepared.")

        def get_chapter_number(chapter_title_: str):
            return int(chapter_title_.strip(CHAPTER_BASE_TITLE).strip(".html"))
        try:
            chapters: typing.List[str] = sorted(
                filter(
                    lambda file: file.startswith(CHAPTER_BASE_TITLE),
                    os.listdir(content_path),
                ),
                key=get_chapter_number,
            )
        except FileNotFoundError:
            raise EasyEpubException("Directory OEBPS does not exist.")

        for chapter in chapters:
            chapter_title = chapter.strip(".html")
            chapter_dir_name = f"{chapters_path}/{chapter_title}"
            os.makedirs(chapter_dir_name, exist_ok=True)

            image = weasyprint.HTML(f"{content_path}/{chapter}").write_png()

            chapter_image_name = f"{chapter_dir_name}/{chapter_title}.png"
            with open(chapter_image_name, "wb") as chapter_image:
                chapter_image.write(image)

            slice_image(chapter_image_name)

        return chapters_path + "/"
