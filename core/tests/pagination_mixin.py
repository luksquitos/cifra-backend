from django.http import HttpResponse


class PaginationInformation:
    offset = 0
    count = 0
    page_size = 2
    current_page_size = 2

    def assert_item(index, item):
        pass

    def __init__(
        self, offset=0, page_size=2, current_page_size=2, count=0, assert_item=None
    ):
        self.offset = offset
        self.page_size = page_size
        self.count = count
        self.current_page_size = current_page_size

        if assert_item:
            self.assert_item = assert_item

    def to_page(page: int, page_size: int):
        return PaginationInformation(
            offset=(page - 1) * page_size,
            page_size=page_size,
        )

    def get_query_params(self):
        return {
            "offset": self.offset,
            "limit": self.page_size,
        }


class PaginationMixin:
    def assertPaginationBody(
        self, response: HttpResponse, config: PaginationInformation
    ):
        response_data = response.json()
        count = response_data.get("count")
        results = response_data.get("results")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(count, config.count)
        self.assertEqual(len(results), config.current_page_size)

        for i in range(0, len(results)):
            item = results[i]
            config.assert_item(i, item)
