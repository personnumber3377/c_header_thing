import struct

class ParsedHeader:
    format = 'STRUCT_FORMAT'

    def __init__(self, data):
        unpacked = struct.unpack(self.format, data[:struct.calcsize(self.format)])
        fields = FIELDS
        for field, value in zip(fields, unpacked):
            setattr(self, field, value)
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
        return f"<ParsedHeader {{parsed_fields}}, Remaining: {{len(self.remaining_data)}} bytes>"