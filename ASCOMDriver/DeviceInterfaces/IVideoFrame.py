from abc import ABC, abstractmethod
from typing import Any


class IVideoFrame(ABC):
    """
    Python translation of ASCOM IVideoFrame (Video V2).
    """

    @property
    @abstractmethod
    def ImageArray(self) -> Any:
        """
        Pixel array: 1D, 2D, or 3D depending on sensor type.
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def PreviewBitmap(self) -> bytes:
        """
        Preview bitmap (byte array).
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def FrameNumber(self) -> int:
        """
        Frame number of the current video frame.
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def ExposureDuration(self) -> float:
        """
        Actual exposure duration in seconds.
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def ExposureStartTime(self) -> str:
        """
        FITS-standard timestamp CCYY-MM-DDThh:mm:ss[.sss...]
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def ImageMetadata(self) -> list[dict]:
        """
        List of metadata entries: [{"Key": "...", "Value": "..."}]
        """
        raise NotImplementedError
