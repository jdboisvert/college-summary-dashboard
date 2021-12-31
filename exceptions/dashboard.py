class NoCollegeMetricsFoundError(Exception):
    def __str__(self) -> str:
        return "No college metrics were found."
