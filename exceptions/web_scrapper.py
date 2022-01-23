class PageDetailsError(Exception):
    def __str__(self) -> str:
        return "Could not get page details."
