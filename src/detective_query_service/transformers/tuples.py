# import standard modules
import json
import pandas as pd
from decimal import Decimal


class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return str(obj)
        return json.JSONEncoder.default(self, obj)


def tuple_to_json(keys, tuple_list):
    # unzip list of tuples to list of lists
    raw_data = list(zip(*tuple_list))
    results = dict(zip(keys, raw_data))
    for key, values in results.items():
        results[key] = list(values)

    results = json.dumps(results, cls=DecimalEncoder)
    results = json.loads(results)

    results = json.loads(pd.DataFrame(results).to_json(orient="records"))
    return results
