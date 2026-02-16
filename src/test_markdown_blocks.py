import unittest

from markdown_blocks import markdown_to_blocks, extract_title 

class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
# This is a heading

This is a paragraph of text. It has some **bold** and _italic_ words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(len(blocks), 3)
        self.assertEqual(blocks[0], "# This is a heading")
        self.assertEqual(blocks[1], "This is a paragraph of text. It has some **bold** and _italic_ words inside of it.")

    
    def test_extract_title(self):
        # Normal durum
        md = "# Hello World"
        self.assertEqual(extract_title(md), "Hello World")

        # Boşluklu durum
        md = "#    Spacey Title    "
        self.assertEqual(extract_title(md), "Spacey Title")

        # Birden fazla satır arasında h1
        md = """
Bu bir paragraf.
# Gerçek Başlık
Bu da başka bir satır.
"""
        self.assertEqual(extract_title(md), "Gerçek Başlık")

    
    def test_extract_title_fail(self):
        # h1 olmayan durum (Exception fırlatmalı)
        md = "## Sadece h2 var"
        with self.assertRaises(Exception):
            extract_title(md)

if __name__ == "__main__":
    unittest.main()
