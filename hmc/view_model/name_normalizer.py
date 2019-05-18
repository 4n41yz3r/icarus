import re

class NameNormalizer():
    junk_words = r'1080p|720p|540p|480p|mp4|h264|aac|bluray|web-dl|split scenes|rarbg'

    @staticmethod
    def normalize(string):
        string = NameNormalizer._remove_junk_words(string)
        string = NameNormalizer._replace_non_whitespace(string)
        return string.strip()

    @staticmethod
    def normalize_file(string):
        string = NameNormalizer._remove_extension(string)
        string = NameNormalizer._remove_junk_words(string)
        string = NameNormalizer._relax_dash(string)
        string = NameNormalizer._replace_dot_and_underscore(string)
        return string.lower().strip().encode('utf-8', 'surrogateescape') #errors='replace'

    @staticmethod
    def _replace_non_whitespace(string):
        return re.sub(r'\W+|_', ' ', string)
    
    @staticmethod
    def _remove_junk_words(string):
        return re.sub(NameNormalizer.junk_words, '', string, flags=re.IGNORECASE)
    
    @staticmethod
    def _relax_dash(string):
        return re.sub(r'-', ' - ', string)

    @staticmethod
    def _remove_extension(string):
        return re.sub(r'\.[^\. ]+$', '', string)
    
    @staticmethod
    def _replace_dot_and_underscore(string):
        return re.sub(r'[ _\.]+', ' ', string)