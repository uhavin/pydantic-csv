"""Typed csv classes."""
import csv
from typing import Any, Dict, List, Optional, Type

from pydantic import BaseModel, ValidationError


class TypedCsv:
    """Wrapper around a csv file."""

    raw_data: Dict[str, Any]
    error: Optional[ValidationError] = None

    _has_loaded: bool = False
    _data_collection_model: Type[BaseModel]
    _data_collection: Type[BaseModel]

    def __init__(self, data_model: Type[BaseModel]):
        class DataListModel(BaseModel):
            data: List[data_model]  # type: ignore

        self._data_collection_model = DataListModel

    def load(self, file: str, explicit_error: bool = False):
        """Load a csv file into a list of the given Pydantic model instances.

        Parameters
        ----------
        file : str
            Path to the file name.
        explicit_error : bool
            Explicitly raise an error if invalid data encountered.
        """
        with open(file) as csv_file:
            self._raw_data = [line for line in csv.DictReader(csv_file)]

        try:
            self._data_collection = self._data_collection_model(data=self._raw_data)
        except ValidationError as e:
            self.error = e

            if explicit_error:
                raise e

        self._has_loaded = True

    @property
    def data(self) -> Type[BaseModel]:
        """Return the pydantic data collection.

        Returns
        -------
        Type[BaseModel]
            A pydantic collection of the given base_model.
        """
        return self._data_collection.data

    @property
    def is_valid(self) -> bool:
        """Check for valid data."""
        return self._has_loaded and self.error is None
