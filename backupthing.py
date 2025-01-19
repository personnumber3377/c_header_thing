import re

def gen_python_code(struct_format, fields):
    fh = open("template.py", "r")
    data = fh.read()
    fh.close()
    # 
    # STRUCT_FORMAT is struct_format and FIELDS is fields in the template.
    data = data.replace("STRUCT_FORMAT", struct_format)
    data = data.replace("FIELDS", fields)
    return data

def c_header_to_python(header):
    # Mapping of C types to struct format characters
    type_mapping = {
        # Integer types
        "BYTE": "B",         # Unsigned 1 byte
        "CHAR": "b",         # Signed 1 byte
        "UCHAR": "B",        # Unsigned 1 byte
        "SHORT": "h",        # Signed 2 bytes
        "USHORT": "H",       # Unsigned 2 bytes
        "WORD": "H",         # Unsigned 2 bytes (Windows-specific)
        "INT": "i",          # Signed 4 bytes
        "UINT": "I",         # Unsigned 4 bytes
        "LONG": "l",         # Signed 4 bytes
        "ULONG": "L",        # Unsigned 4 bytes
        "DWORD": "I",        # Unsigned 4 bytes (Windows-specific)
        "LONGLONG": "q",     # Signed 8 bytes
        "ULONGLONG": "Q",    # Unsigned 8 bytes
        "SIZE_T": "Q",       # Platform-dependent size type (64-bit here)

        # Floating-point types
        "FLOAT": "f",        # 4 bytes
        "DOUBLE": "d",       # 8 bytes

        # Character types
        "TCHAR": "c",        # 1 character (use Unicode-specific mappings if needed)
        "WCHAR": "H",        # 2 bytes (Unicode character)
        "CHAR16": "H",       # UTF-16 2-byte character
        "CHAR32": "I",       # UTF-32 4-byte character

        # Composite types
        "RECTL": "4i",       # Rectangle (4 signed LONGs)
        "SIZEL": "2i",       # Size (2 signed LONGs)
        "POINTL": "2i",      # Point (2 signed LONGs)
        "RECT": "4i",        # Rectangle structure
        "SIZE": "2i",        # Size structure
        "POINT": "2i",       # Point structure

        # Boolean types
        "BOOL": "I",         # 4 bytes (commonly used in Windows)
        "BOOLEAN": "B",      # 1 byte (commonly used in Unix)

        # Special types
        "HANDLE": "P",       # Pointer to a handle (platform-dependent size)
        "LPVOID": "P",       # Void pointer
        "LPSTR": "P",        # Pointer to a string
        "LPCSTR": "P",       # Pointer to a constant string
        "LPWSTR": "P",       # Pointer to a wide string
        "LPCWSTR": "P",      # Pointer to a constant wide string

        # Unix-specific
        "int8_t": "b",       # Signed 1 byte
        "uint8_t": "B",      # Unsigned 1 byte
        "int16_t": "h",      # Signed 2 bytes
        "uint16_t": "H",     # Unsigned 2 bytes
        "int32_t": "i",      # Signed 4 bytes
        "uint32_t": "I",     # Unsigned 4 bytes
        "int64_t": "q",      # Signed 8 bytes
        "uint64_t": "Q",     # Unsigned 8 bytes
        "pid_t": "i",        # Process ID type
        "off_t": "q",        # File offset type
        "time_t": "q",       # Time type (signed 8 bytes)
        "ssize_t": "q",      # Signed size type
        "size_t": "Q",       # Unsigned size type
        "uid_t": "I",        # User ID
        "gid_t": "I",        # Group ID

        # Pointers
        "void*": "P",        # Generic pointer (platform-dependent)
        "char*": "P",        # Pointer to a character array
        "int*": "P",         # Pointer to an integer
        "float*": "P",       # Pointer to a float
        "double*": "P",      # Pointer to a double
    }

    # Regular expression to match C-style fields
    field_regex = re.compile(r"(\w+)\s+(\w+);")
    struct_format = ""
    fields = []

    # Process the header line by line
    for line in header.splitlines():
        match = field_regex.search(line)
        if match:
            c_type, field_name = match.groups()
            if c_type in type_mapping:
                struct_format += type_mapping[c_type]
                fields.append(field_name)
            else:
                raise ValueError(f"Unknown type: {c_type}")

    # Generate Python code
    '''
    python_code = f"""import struct

class EMFHeader:
    format = '{struct_format}'

    def __init__(self, data):
        unpacked = struct.unpack(self.format, data)
        fields = {fields}
        for field, value in zip(fields, unpacked):
            setattr(self, field, value)

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read(struct.calcsize(cls.format))
            return cls(data)
"""
    '''

    python_code = gen_python_code(struct_format, str(fields))
    return python_code

'''
# Example usage
c_header = """
DWORD   iType;
DWORD   nSize;
RECTL   rclBounds;
RECTL   rclFrame;
DWORD   dSignature;
DWORD   nVersion;
DWORD   nBytes;
DWORD   nRecords;
WORD    nHandles;
WORD    sReserved;
DWORD   nDescription;
DWORD   offDescription;
DWORD   nPalEntries;
SIZEL   szlDevice;
SIZEL   szlMillimeters;
"""
'''
#generated_code = c_header_to_python(c_header)
#print(generated_code)


def gen_header(filename: str) -> None:
    fh = open(filename, "r")
    data = fh.read()
    fh.close()
    print(c_header_to_python(data))
    return

import sys

if __name__=="__main__":
    if len(sys.argv) != 2:
        print("Usage: "+str(sys.argv[0])+" INPUT_C_HEADER_FILE")
        exit(0)
    gen_header(sys.argv[1])
    exit(0)