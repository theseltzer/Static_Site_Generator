import unittest
from inline_markdown import *

class TestInlineMarkdown(unittest.TestCase):
    
    def test_extract_markdown_images(self):
        # Birden fazla resim içeren metin
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        matches = extract_markdown_images(text)
        
        # Beklenen sonuç: Bir liste içinde tuple'lar
        expected = [
            ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
            ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")
        ]
        
        # self.assertListEqual -> unittest'in bize sunduğu, listeleri kıyaslayan araç
        self.assertListEqual(matches, expected)

    def test_extract_markdown_links(self):
        # Birden fazla link içeren metin
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        matches = extract_markdown_links(text)
        
        expected = [
            ("to boot dev", "https://www.boot.dev"),
            ("to youtube", "https://www.youtube.com/@bootdotdev")
        ]
        
        self.assertListEqual(matches, expected)

    def test_extract_links_should_not_extract_images(self):
        # Link fonksiyonu resimleri (başında ! olanları) yakalamamalı!
        text = "This is a ![image](https://url.com) and a [link](https://boot.dev)"
        matches = extract_markdown_links(text)
        
        # Sadece linki yakalamış olmalı
        expected = [("link", "https://boot.dev")]
        self.assertListEqual(matches, expected)

    def test_split_images(self):
        # 1. Senaryo: Normal metin içinde birden fazla resim
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.NORMAL),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.NORMAL),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

    def test_split_images_at_start(self):
        # 2. Senaryo: Metin resimle başlarsa (Boş düğüm üretmemeli!)
        node = TextNode("![start](https://url.com) and some text", TextType.NORMAL)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("start", TextType.IMAGE, "https://url.com"),
                TextNode(" and some text", TextType.NORMAL),
            ],
            new_nodes,
        )


    def test_split_links(self):
        # 3. Senaryo: Metin sonunda link olması
        node = TextNode(
            "Check out [Boot.dev](https://www.boot.dev)",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Check out ", TextType.NORMAL),
                TextNode("Boot.dev", TextType.LINK, "https://www.boot.dev"),
            ],
            new_nodes,
        )

    def test_split_links_multiple(self):
        # 4. Senaryo: Arka arkaya linkler (Boşluksuz)
        node = TextNode(
            "[link1](u1)[link2](u2)",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("link1", TextType.LINK, "u1"),
                TextNode("link2", TextType.LINK, "u2"),
            ],
            new_nodes,
        )


    def test_split_links_ignore_images(self):
        # 5. Senaryo: Link fonksiyonu resme dokunmamalı
        node = TextNode(
            "Look at this ![image](url1) and this [link](url2)",
            TextType.NORMAL,
        )
        # Sadece linkleri ayır diyoruz
        new_nodes = split_nodes_link([node])
        
        # Resim kısmı hala NORMAL metin olarak kalmalı çünkü split_nodes_link ünlemi tanımaz
        self.assertListEqual(
            [
                TextNode("Look at this ![image](url1) and this ", TextType.NORMAL),
                TextNode("link", TextType.LINK, "url2"),
            ],
            new_nodes,
        )
    def test_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
    
        self.assertListEqual(
            [
                TextNode("This is ", TextType.NORMAL),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.NORMAL),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.NORMAL),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.NORMAL),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.NORMAL),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            nodes,
        )

if __name__ == "__main__":
    unittest.main()
