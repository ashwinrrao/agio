import pytest

from grocery import process_resposne


@pytest.mark.parametrize(
    "response_dict, expected_result",
    [
        # test case for empty input
        ({}, (0, set())),
        # test case which contains a single item for an order
        (
            {"orders": [{"items": [{"total_price": 5, "category": "produce"}]}]},
            (5, set(["produce"])),
        ),
        # test case for when an order contains multiple items
        (
            {
                "orders": [
                    {
                        "items": [
                            {"total_price": 5, "category": "produce"},
                            {"total_price": 6, "category": "frozen"},
                        ]
                    }
                ]
            },
            (11, set(["produce", "frozen"])),
        ),
        # test case for when there are multiple orders and items
        (
            {
                "orders": [
                    {
                        "items": [
                            {"total_price": 5, "category": "produce"},
                            {"total_price": 6, "category": "frozen"},
                        ]
                    },
                    {
                        "items": [
                            {"total_price": 25, "category": "grain"},
                            {"total_price": 30, "category": "frozen"},
                        ]
                    },
                ]
            },
            (66, set(["produce", "grain", "frozen"])),
        ),
    ],
)
def test_process_response(response_dict, expected_result):
    assert process_resposne(response_dict) == expected_result
