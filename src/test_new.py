import unittest
from textnode import TextNode, TextType
from new import split_nodes_delimiter

class TestInlineMarkdown(unittest.TestCase):
    def test_delim_bold(self):
        # TextType.NORMAL olarak güncellendi
        node = TextNode("This is text with a **bolded** word", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text_type, TextType.NORMAL)
        self.assertEqual(new_nodes[1].text, "bolded")
        self.assertEqual(new_nodes[1].text_type, TextType.BOLD)

    def test_delim_code(self):
        node = TextNode("This is a `code block`", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        
        # Eğer metnin sonunda başka yazı yoksa 2 düğüm oluşması doğrudur
        self.assertEqual(len(new_nodes), 2) 
        self.assertEqual(new_nodes[0].text, "This is a ")
        self.assertEqual(new_nodes[1].text, "code block")
    def test_delim_bold_exception(self):
        node = TextNode("This is **invalid bold", TextType.NORMAL)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "**", TextType.BOLD)

if __name__ == "__main__":
    unittest.main()
