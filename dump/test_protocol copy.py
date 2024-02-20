from dataclasses import dataclass
import pytest


@dataclass
class SimpleString:
    data: str

@pytest.mark.parametrize("buffer, expected",[
    (b"+Par", (None, 0)),
    (b"+OK\r\n", (SimpleString("OK"), 5)),
    (b"+OK\r\n+Next", (SimpleString("OK"), 5)),
])
def test_read_from_simple_string(buffer, expected):
    actual = extract_frame_from_buffer(buffer)
    assert actual == expected

def test_read_from_simple_string_incomplete_frame():
    buffer = b"+Par"
    frame, frame_size = extract_frame_from_buffer(buffer)
    assert frame == None
    assert frame_size == 0


def test_read_from_simple_string_complete_frame():
    buffer = b"+OK\r\n"
    frame, frame_size = extract_frame_from_buffer(buffer)
    assert frame == SimpleString("OK")
    assert frame_size == 5

def test_read_from_simple_string_extra_data():
    buffer = b"+OK\r\n+Next"
    frame, frame_size = extract_frame_from_buffer(buffer)
    assert frame == SimpleString("OK")
    assert frame_size == 5

MSG_SEPERATOR = b"\r\n"



def extract_frame_from_buffer(buffer):
    match chr(buffer[0]):
        case '+':
            seperator = buffer.find(MSG_SEPERATOR)

            if seperator != -1:
                return SimpleString(buffer[1:seperator].decode()), seperator+2
    return None, 0

    
