import os, sys, tempfile, unittest
sys.path.insert(0, ".")
from dupecheck.core import find_duplicates, human

class FindTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        root = self.tmp.name
        def write(rel, data):
            path = os.path.join(root, rel)
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "wb") as handle:
                handle.write(data)
        write("a/foto.jpg", b"X" * 100)
        write("b/foto-copy.jpg", b"X" * 100)
        write("c/foto-lain.jpg", b"Y" * 100)
        write("unik.txt", b"sendiri")
    def tearDown(self):
        self.tmp.cleanup()
    def test_finds_content_duplicates(self):
        result = find_duplicates([self.tmp.name])
        self.assertEqual(len(result["groups"]), 1)
        group = result["groups"][0]
        self.assertEqual(len(group["files"]), 2)
        self.assertEqual(group["wasted"], 100)
        self.assertEqual(result["total_wasted"], 100)
    def test_min_size(self):
        result = find_duplicates([self.tmp.name], min_size=101)
        self.assertEqual(result["groups"], [])
    def test_scanned_count(self):
        result = find_duplicates([self.tmp.name])
        self.assertEqual(result["scanned"], 4)

class HumanTests(unittest.TestCase):
    def test_units(self):
        self.assertEqual(human(512), "512 B")
        self.assertEqual(human(2048), "2.0 KB")
        self.assertEqual(human(5 * 1024 * 1024), "5.0 MB")

if __name__ == "__main__":
    unittest.main()
