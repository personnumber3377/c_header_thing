import struct

class ParsedHeader:
    format = 'STRUCT_FORMAT'

    def __init__(self, data):
        unpacked = struct.unpack(self.format, data[:struct.calcsize(self.format)])
        fields = FIELDS
        print("unpacked: ")
        print(unpacked)
        for field, value in zip(fields, unpacked):
            print("value == "+str(value))
            if isinstance(value, tuple): # This is a multibyte value.
                # Should be integers all
                assert all([x >= 0 and x <= 255 for x in value]) # Should be integers representing single bytes.
                # Make a list and then just use bytes
                b = bytes(value)
                # Now make the integer...
                # int.from_bytes(byte_data, byteorder='little')
                integer = int.from_bytes(b, byteorder='little')
                setattr(self, field, (len(b), value))
            else:
                assert value >= 0 and value <= 255 
                setattr(self, field, (1, value)) # Size of one byte
        self.remaining_data = data[struct.calcsize(self.format):]
        print("Here is the size thing: "+str(struct.calcsize(self.format)))
        # return self.remaining_data # Return the remaining data after reading the header.

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        fields = FIELDS
        parsed_fields = {field: getattr(self, field) for field in fields}
        return f"<ParsedHeader {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"