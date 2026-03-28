import json
import re


def safe_parse(response):
    try:
        return json.loads(response)
    except:
        # try to extract JSON
        match = re.search(r"\{.*\}", response, re.DOTALL)
        if match:
            try:
                return json.loads(match.group())
            except:
                pass

    return {"error": "Invalid JSON", "raw": response}