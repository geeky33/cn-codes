class CRC:
    def __init__(self, generator):
        self.generator = generator
        self.degree = len(generator) - 1

    def encode(self, frame):
        frame = frame[:]  # copy to avoid mutating caller's list
        # append degree zeros
        for _ in range(self.degree):
            frame.append(0)

        current_window = frame[:len(self.generator)]

        for i in range(len(self.generator) - 1, len(frame)):
            if current_window[0] == 1:
                for j in range(len(current_window)):
                    current_window[j] ^= self.generator[j]

            # slide window: drop first bit
            current_window.pop(0)

            # append next bit from frame if available
            if i + 1 < len(frame):
                current_window.append(frame[i + 1])

        remainder = [0] + current_window
        for i in range(1, len(self.generator)):
            frame[-i] ^= remainder[len(remainder) - i]

        return frame

    def decode(self, frame):
        frame = frame[:]  # copy to avoid mutating caller's list
        # append degree zeros
        for _ in range(self.degree):
            frame.append(0)

        current_window = frame[:len(self.generator)]

        for i in range(len(self.generator) - 1, len(frame)):
            if current_window[0] == 1:
                for j in range(len(current_window)):
                    current_window[j] ^= self.generator[j]

            # slide window: drop first bit
            current_window.pop(0)

            # append next bit from frame if available
            if i + 1 < len(frame):
                current_window.append(frame[i + 1])

        remainder = [0] + current_window

        if remainder == [0] * len(self.generator):
            return "No error!"
        else:
            return "Error!"


class InternetChecksum:
    def encode(self, frame):
        checksum = 0x0000
        for word in frame:
            checksum += word
            checksum = (checksum & 0xFFFF) + (checksum >> 16)
        checksum = ~checksum & 0xFFFF
        return checksum

    def decode(self, frame):
        total = 0x0000
        for word in frame:
            total += word
            total = (total & 0xFFFF) + (total >> 16)
        if total == 0xFFFF:
            return "No Error!"
        else:
            return "Error!"


if __name__ == "__main__":
    print("For CRC:")
    crc_generator = [1, 0, 0, 1, 1]
    crc = CRC(crc_generator)
    frame = [1, 1, 0, 1, 0, 1, 1, 1, 1, 1]
    print("Original frame: ", frame)

    encoded_frame = crc.encode(frame)
    print("Valid frame (encoded): ", encoded_frame)
    print("CRC decoding result:", crc.decode(encoded_frame[:]))

    # flip a bit to corrupt
    encoded_frame[7] = 1 - encoded_frame[7]
    print("Corrupted frame: ", encoded_frame)
    print("CRC decoding result:", crc.decode(encoded_frame[:]))

    print("\nFor Internet Checksum:")
    checksum = InternetChecksum()
    frame2 = [0xAB12, 0xCD34, 0xEF56]
    print("Original frame: ", [hex(word) for word in frame2])

    chksum = checksum.encode(frame2[:])
    frame2_with_checksum = frame2 + [chksum]
    print("Valid frame with checksum: ", [hex(word) for word in frame2_with_checksum])
    print("Internet checksum decoding result:", checksum.decode(frame2_with_checksum))

    # corrupt one word
    frame2_with_checksum[1] = 0xCD37
    print("Corrupted frame with checksum: ", [hex(word) for word in frame2_with_checksum])
    print("Internet checksum decoding result:", checksum.decode(frame2_with_checksum))
