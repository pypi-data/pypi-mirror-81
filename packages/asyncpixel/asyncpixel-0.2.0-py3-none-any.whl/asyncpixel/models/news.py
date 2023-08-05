"""News related objects."""


class News:
    """News object."""

    def __init__(self, material: str, link: str, text: str, title: str) -> None:
        """Init news.

        Args:
            material (str): material
            link (str): link to artivle
            text (str): text
            title (str): title
        """
        self.material = material
        self.link = link
        self.text = text
        self.title = title
