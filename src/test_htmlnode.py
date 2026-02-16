
import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        # Normal bir link etiketi özellikleri
        node = HTMLNode(
            "a", 
            "Link metni", 
            None, 
            {"href": "https://www.google.com", "target": "_blank"}
        )
        self.assertEqual(
            node.props_to_html(), 
            ' href="https://www.google.com" target="_blank"'
        )

    def test_values(self):
        # Tag ve value'nun doğru atandığı kontrolü
        node = HTMLNode("h1", "Merhaba Dünya")
        self.assertEqual(node.tag, "h1")
        self.assertEqual(node.value, "Merhaba Dünya")
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)

    def test_repr(self):
        #__repr__ çıktısının beklediğimiz formatta olması
        node = HTMLNode("p", "Paragraf", None, {"class": "primary"})
        expected = "HTMLNode(p, Paragraf, children: None, {'class': 'primary'})"
        self.assertEqual(repr(node), expected)

    def test_empty_props(self):
        # Props None olduğunda boş string dönmeli
        node = HTMLNode("div", "İçerik")
        self.assertEqual(node.props_to_html(), "")

class TestLeafNode(unittest.TestCase):
    # 1. Senaryo: Standart bir paragraf etiketi
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    # 2. Senaryo: Özellikleri (props) olan bir link etiketi
    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(
            node.to_html(), 
            '<a href="https://www.google.com">Click me!</a>'
        )

    # 3. Senaryo: Tag None olduğunda sadece ham metin dönmeli (Raw Text)
    def test_leaf_to_html_raw_text(self):
        node = LeafNode(None, "Just some plain text")
        self.assertEqual(node.to_html(), "Just some plain text")

    # 4. Senaryo: Farklı bir etiket (örneğin kalın yazı)
    def test_leaf_to_html_bold(self):
        node = LeafNode("b", "Bold text")
        self.assertEqual(node.to_html(), "<b>Bold text</b>")

    # 5. Senaryo: Birden fazla props durumu
    def test_leaf_to_html_complex_props(self):
        node = LeafNode("img", "", {"src": "image.png", "alt": "Description"})
        # Not: Image etiketi genelde kendi kendini kapatır ama bizim mevcut
        # mantığımızda <img...></img> şeklinde render edilecektir.
        self.assertEqual(
            node.to_html(), 
            '<img src="image.png" alt="Description"></img>'
        )

class TestParentNode(unittest.TestCase):
    # 1. Senaryo: Senin verdiğin temel çocuk testi
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    # 2. Senaryo: Senin verdiğin derin (torunlu) test
    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    # 3. Senaryo: Çoklu ve karışık çocuklar (Parent + Leaf bir arada)
    def test_to_html_many_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                ParentNode("span", [LeafNode(None, "Nested text")]),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i><span>Nested text</span></p>"
        )

    # 4. Senaryo: Özellikleri (props) olan bir ParentNode
    def test_to_html_with_props(self):
        node = ParentNode(
            "div",
            [LeafNode("span", "hello")],
            {"class": "container", "id": "main"}
        )
        self.assertEqual(
            node.to_html(),
            '<div class="container" id="main"><span>hello</span></div>'
        )

    # 5. Senaryo: Hata Durumu - Tag eksikse
    def test_to_html_no_tag(self):
        node = ParentNode(None, [LeafNode("b", "test")])
        with self.assertRaises(ValueError) as cm:
            node.to_html()
        self.assertEqual(str(cm.exception), "Invalid HTML: no tag provided")

    # 6. Senaryo: Hata Durumu - Children eksikse
    def test_to_html_no_children(self):
        node = ParentNode("div", None)
        with self.assertRaises(ValueError) as cm:
            node.to_html()
        self.assertEqual(str(cm.exception), "Invalid HTML: no children provided")


if  __name__=="__main__":
    unittest.main()
