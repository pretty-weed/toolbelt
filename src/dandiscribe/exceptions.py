class NewDocError(Exception):
    pass


class InvalidSheet(Exception):
    pass


class NoObjects(Exception):
    """
    Raise this when there are no objects for some action
    """

    def __init__(self, document: str, page: int):
        self.doc = document
        self.page = page
        super().__init__(f"No objects in doc {document} on page {page}")
