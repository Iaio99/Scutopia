#!/usr/bin/env python

import json
from django.core.management.utils import get_random_secret_key


with open("keys.json", "r") as fp:
	data = json.load(fp)

data["secretkey"] = get_random_secret_key()
	
with open("keys.json", "w") as fp:
	json.dump(data, fp)
