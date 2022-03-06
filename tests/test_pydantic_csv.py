import datetime
from os import path

from pydantic import BaseModel

from pydantic_csv.typed_csv import TypedCsv


def test_valid_csv():
    class ValidCsv(BaseModel):
        number: int
        word: str
        date: datetime.date

    valid_csv = TypedCsv(ValidCsv)
    test_file_path = path.dirname(path.abspath(__file__))
    csv_path = path.join(test_file_path, "csv", "valid_csv.csv")
    valid_csv.load(csv_path)

    assert valid_csv.is_valid
