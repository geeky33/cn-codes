STX = 0x02
ETX = 0x03
DLE = 0x10


def bit_stuffing(data):
    stuffed = ""
    consecutive_ones = 0

    for ch in data:
        # Iterate over bits of ascii character
        ch_binary = bin(ord(ch))[2:].zfill(8)
        for bit in ch_binary:
            stuffed += bit
            if bit == '1':
                consecutive_ones += 1
                if consecutive_ones == 5:
                    stuffed += "0"
                    consecutive_ones = 0
            else:
                consecutive_ones = 0

    return stuffed


def bit_unstuffing(data):
    ascii_output = ""
    bit_buffer = ""
    one_count = 0

    for ch in data:
        if ch == '0':
            if one_count != 5:
                bit_buffer += ch
            one_count = 0
        else:
            bit_buffer += ch
            one_count += 1

        if len(bit_buffer) == 8:
            ascii_output += chr(int(bit_buffer, 2))
            bit_buffer = ""

    return ascii_output


def byte_stuffing(data):
    stuffed = chr(STX)
    for ch in data:
        if ch in [chr(DLE), chr(STX), chr(ETX)]:
            stuffed += chr(DLE)
        stuffed += ch
    stuffed += chr(ETX)
    return stuffed


def byte_unstuffing(data):
    original = ""
    i = 1
    # iterate until the byte before final ETX
    while i < len(data) - 1:
        if data[i] == chr(DLE):
            i += 1
            original += data[i]
        else:
            original += data[i]
        i += 1
    return original


if __name__ == "__main__":
    string = "abcdesodghlkjsgsbgjklsbljfg"
    encoded = bit_stuffing(string)
    print("Bit stuffing encoded string:", encoded)
    decoded = bit_unstuffing(encoded)
    print("Bit stuffing decoded string:", decoded)
    assert decoded == string

    print()

    string = "Hello World!"
    string += chr(DLE)
    string += " Hello Python!"
    encoded = byte_stuffing(string)
    print("Byte stuffing encoded string:", repr(encoded))
    decoded = byte_unstuffing(encoded)
    print("Byte stuffing decoded string:", decoded)
    assert decoded == string
