import base64

class Base64:
    """Base64 string encoding helper"""

    @staticmethod
    def encode(input_bytes):
        """Encode bytes to base64 string"""
        encoded_bytes = base64.urlsafe_b64encode(input_bytes)
        return encoded_bytes.decode('utf-8')

    @staticmethod
    def decode(input_str):
        """Decode base64 string to bytes"""
        bytes_string = input_str.encode('utf-8')
        decoded_bytes = base64.urlsafe_b64decode(bytes_string)
        return decoded_bytes

    @staticmethod
    def bytes_to_string(bytes):
        """Converts decoded bytes to string"""
        return bytes.decode('utf8', 'surrogateescape')

    @staticmethod
    def string_to_bytes(string):
        return string.encode('utf-8', 'surrogateescape')
