from enum import Enum


class FileType(str, Enum):
    PDF = "PDF"
    DOCX = "DOCX"
    TXT = "TXT"
    CSV = "CSV"
    JSON = "JSON"
    PNG = "PNG"
    JPG = "JPG"
    MD = "MD"
    HTML = "HTML"
