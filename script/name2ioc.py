# -*- coding: utf-8 -*-
import json

json_string = open("../data/country-codes_json.json",encoding="utf-8").read()
parsed_json = json.loads(json_string,encoding="utf-8")
convert = {}
for j in parsed_json:
	convert[j["CLDR display name"]] =j["IOC"]
print(convert)

