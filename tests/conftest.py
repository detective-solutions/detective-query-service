# import third party modules
import pytest
import pandas as pd


@pytest.fixture(scope="session")
def dummy_data():
    yield pd.DataFrame({
        "test_column": list(range(5))
    })


@pytest.fixture(scope="session")
def find_column_first_message():
    yield {
       "case": "90d404c5-9d20-11ec-83f2-287fc999439d",
       "event_type": "find_columns_first",
       "query": [
          "SHOW COLUMNS FROM freequery"
       ],
       "source": [
          "9ebc4876-7135-11ec-8fb9-2f89zf6e439d"
       ],
       "groups": [
          "4e45ac4b-9d18-11ec-8804-287fcf6e439d"
       ],
       "follow_query_event": {
          "case": "90d404c5-9d20-11ec-83f2-287fc999439d",
          "query_type": "general",
          "query": [
             "SELECT * FROM freequery LIMIT 100"
          ],
          "source": [
             "9ebc4876-7135-11ec-8fb9-2f89zf6e439d"
          ],
          "groups": [
             "4e45ac4b-9d18-11ec-8804-287fcf6e439d"
          ]
       }
    }
