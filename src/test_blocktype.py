import unittest
from blocktype import BlockType, block_to_block_type

class TestBlockToBlockType(unittest.TestCase):
    def test_block_to_block_types(self):
        # 1. Heading Testleri
        self.assertEqual(block_to_block_type("# heading"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("### subtitle"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("####### too many"), BlockType.PARAGRAPH)

        # 2. Code Testleri
        self.assertEqual(block_to_block_type("```\npython code\n```"), BlockType.CODE)
        self.assertEqual(block_to_block_type("```code```"), BlockType.CODE)

        # 3. Quote Testleri
        self.assertEqual(block_to_block_type("> line 1\n> line 2"), BlockType.QUOTE)
        self.assertEqual(block_to_block_type("> line 1\nline 2 without bracket"), BlockType.PARAGRAPH)

        # 4. Unordered List Testleri
        self.assertEqual(block_to_block_type("- item 1\n- item 2"), BlockType.UNORDERED_LIST)
        self.assertEqual(block_to_block_type("- item 1\n* item 2"), BlockType.PARAGRAPH)

        # 5. Ordered List Testleri
        self.assertEqual(block_to_block_type("1. first\n2. second\n3. third"), BlockType.ORDERED_LIST)
        # Sırası bozuk liste testi
        self.assertEqual(block_to_block_type("1. first\n3. second"), BlockType.PARAGRAPH)
        # 1 ile başlamayan liste testi
        self.assertEqual(block_to_block_type("2. second\n3. third"), BlockType.PARAGRAPH)

        # 6. Paragraf Testi
        self.assertEqual(block_to_block_type("I am just a normal paragraph text."), BlockType.PARAGRAPH)

if __name__ == "__main__":
    unittest.main()
