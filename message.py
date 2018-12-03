from datetime import datetime
from collections import Counter


class Person(object):
    def __init__(self, name):
        self._name = name

    @property
    def name(self):
        return self._name

    def __eq__(self, other):
        return self.name == other.name

    def __repr__(self):
        return "Person(" + self.name + ")"

    def __str__(self):
        return self.name


class Message(object):
    def __init__(self, raw_message, conversation_id=None):
        self._conversation_id = conversation_id
        self._raw_message = raw_message
        assert self._is_message_valid(
            raw_message
        ), "Message text does not constitute a valid message"

        self._message = raw_message.split(": ", 1)[-1]
        self._sender = Person(self._handle_sender_info(raw_message))
        self._timestamp = datetime.strptime(
            raw_message.split(" - ", 1)[0], "%d/%m/%y, %I:%M %p"
        )
        self._is_media = self._message == "<Media omitted>"

    @staticmethod
    def _is_message_valid(raw_message):
        try:
            datetime.strptime(raw_message.split(" - ")[0], "%d/%m/%y, %I:%M %p")
        except ValueError:
            return False

        return True

    def _handle_sender_info(self, raw_message):
        # Fix message extraction in this case
        split = raw_message.split(" - ", 1)[1].split(":", 1)[0]
        special_messages = [
            "changed",
            "removed",
            "added",
            "deleted",
            "encryption",
            "changed",
            "security code",
            "left",
        ]

        if any([x in split for x in special_messages]):
            return "<OTHER>"
        else:
            return split

    @property
    def conversation_id(self):
        return self._conversation_id

    @property
    def message(self):
        return self._message

    @property
    def is_media(self):
        return self._is_media

    @property
    def sender(self):
        return self._sender

    @property
    def timestamp(self):
        return self._timestamp

    @property
    def date(self):
        return self.timestamp.date()

    @property
    def time(self):
        return self.timestamp.time()

    def __repr__(self):
        return "Message(" + str(self._raw_message).strip() + ")"

    def __str__(self):
        return self.message


class Conversation(object):
    def __init__(self, name):
        self._name = name
        self._participants = []
        self._messages = []
        self._message_counts = {}

    @property
    def name(self):
        return self._name

    @property
    def participants(self):
        return self._participants

    def _add_participant(self, person):
        self._participants.append(person)

    @property
    def messages(self):
        return self._messages

    @property
    def message_counts(self):
        return self._message_counts

    def add_raw_message(self, raw_message):
        message = Message(raw_message)
        sender = message.sender
        self._messages.append(message)

        if sender not in self.participants:
            self._add_participant(sender)
            self._message_counts[sender.name] = 0

        self._message_counts[sender.name] += 1

    def __getitem__(self, idx):
        return self.messages[idx]

    def __repr__(self):
        return "Conversation(" + self.name + ")"

    ## Analysis
    def time_composition(self, visualize=True):
        hours, counts = [], []
        counter = Counter(msg.time.hour for msg in self.messages)
        for k, v in counter.items():
            hours.append(k)
            counts.append(v)
        if visualize:
            try:
                import matplotlib
                from matplotlib import pyplot as plt

                plt.bar(hours, counts)
            except ImportError:
                print("Matplotlib not installed")

        return counter

    @property
    def _duration(self):
        return self.messages[-1].timestamp - self.messages[0].timestamp

    def message_rate(self, per="day"):
        divide_by = self._duration.total_seconds()
        if per == "second":
            pass
        elif per == "minute":
            divide_by /= 60
        elif per == "hour":
            divide_by /= 3600
        else:
            divide_by /= 3600 * 24

        return round(len(self.messages) / divide_by, 2)

