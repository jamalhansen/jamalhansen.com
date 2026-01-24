import re

test = """categories: Python
featureimage:
cardimage:
draft: false"""

feature_match = re.search(r'^featureimage:\s*([^\n]*)$', test, re.MULTILINE)
card_match = re.search(r'^cardimage:\s*([^\n]*)$', test, re.MULTILINE)

print("Feature match:", repr(feature_match.group(1) if feature_match else None))
print("Card match:", repr(card_match.group(1) if card_match else None))

if feature_match:
    print("Feature stripped:", repr(feature_match.group(1).strip()))
    print("Feature bool:", bool(feature_match.group(1).strip()))
