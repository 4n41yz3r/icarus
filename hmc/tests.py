from unittest import TestCase
from .services import MediaFile

# Create your tests here.
class MediaFileTest(TestCase):
    def setUp(self):
        self.sut = MediaFile('c:/dir/file.ext')

    def test_source_returns_string(self):
        src = self.sut.source()
        self.assertTrue(isinstance(src, str))

    def test_source_returns_base64_encoded_url(self):
        src = self.sut.source()
        self.assertEqual(src, 'YzovZGlyL2ZpbGUuZXh0')

    def test_kind_returns_unknown_for_unknown_extensions(self):
        self.assertEqual(MediaFile('a.txt').kind(), 'unknown')

    def test_kind_returns_video_for_video_extensions(self):
        self.assertEqual(MediaFile('a.mp4').kind(), 'video')

    def test_kind_returns_audio_for_audio_extensions(self):
        self.assertEqual(MediaFile('a.mp3').kind(), 'audio')

    def test_file_name_returns_expected(self):
        self.assertEqual(self.sut.file_name(), 'file.ext')

    def test_extension_returns_expected_value(self):
        self.assertEqual(self.sut.extension(), 'ext')

    def test_is_media_returns_false_for_unknown_media(self):
        self.assertEqual(MediaFile('a.txt').is_media(), False)
    
    def test_is_media_returns_true_for_known_media(self):
        self.assertEqual(MediaFile('a.mp3').is_media(), True)
        self.assertEqual(MediaFile('a.mp4').is_media(), True)