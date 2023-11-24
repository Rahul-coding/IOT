from jsonpath_ng import JSONPath, parse
import json
import streamlit as st

with open('.cheez_itz/ocr_output.txt') as json_file:
    json_data = json.load(json_file)
expression = parse('pages[*].lines[*].text')
match = expression.find(json_data)
for match in expression.find(json_data):
    print(match.value)