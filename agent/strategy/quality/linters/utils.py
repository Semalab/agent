import json
import re

MATCHER_GCC = r'^(?P<filename>.*?):(?P<line_num>\d+):(?P<col_num>\d*):\s+\w+:\s+(?P<err_message>.*)$'
MATCHER_UNIX = r'^(?P<filename>.*?):(?P<line_num>\d+):(?P<col_num>\d*):\s+(?P<err_message>.*)$'

def parse_to_json(message_file, json_file, message_re):
    json.dump(
        [match.groupdict()
            for line in message_file
            if (match := re.match(message_re, line)) is not None],
        json_file)
