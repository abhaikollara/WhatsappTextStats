from datetime import datetime
from message import Conversation


def _is_next_message(raw_message):
    try:
        datetime.strptime(raw_message.split(" - ")[0], "%d/%m/%y, %I:%M %p")
    except ValueError:
        return False

    return True


def parse_file(f):
    raw_data = (str(x, encoding="utf-8") for x in f.readlines())
    name = f.filename.split("with ")[1].split(".txt")[0]
    conversation = Conversation(name)
    buffer = next(raw_data)
    for line in raw_data:
        if _is_next_message(line):
            conversation.add_raw_message(buffer.rstrip())
            buffer = line
        else:
            buffer += line
    return conversation

