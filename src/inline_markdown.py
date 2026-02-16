from new import split_nodes_delimiter
import re
from textnode import TextNode, TextType

def extract_markdown_images(text):
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern,text)
    return matches

def extract_markdown_links(text):
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        # Sadece NORMAL metinleri parçalıyoruz
        if node.text_type != TextType.NORMAL:
            new_nodes.append(node)
            continue
        
        original_text = node.text
        images = extract_markdown_images(original_text)
        
        # Eğer resim yoksa orijinal düğümü ekle
        if len(images) == 0:
            new_nodes.append(node)
            continue
            
        current_text = original_text
        for image_alt, image_url in images:
            # Resim ayracını oluşturuyoruz: ![alt](url)
            sections = current_text.split(f"![{image_alt}]({image_url})", 1)
            
            if len(sections) != 2:
                raise ValueError("Invalid markdown: image section not closed")
            
            # Resimden önceki metin varsa ekle
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.NORMAL))
            
            # Resmin kendisini ekle
            new_nodes.append(TextNode(image_alt, TextType.IMAGE, image_url))
            
            # Kalan metni bir sonraki tur için güncelle
            current_text = sections[1]
            
        # En sonda kalan metin varsa ekle
        if current_text != "":
            new_nodes.append(TextNode(current_text, TextType.NORMAL))
            
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.NORMAL:
            new_nodes.append(node)
            continue
        
        original_text = node.text
        links = extract_markdown_links(original_text)
        
        if len(links) == 0:
            new_nodes.append(node)
            continue
            
        current_text = original_text
        for link_text, link_url in links:
            # Link ayracını oluşturuyoruz: [text](url) - Ünlem yok!
            sections = current_text.split(f"[{link_text}]({link_url})", 1)
            
            if len(sections) != 2:
                raise ValueError("Invalid markdown: link section not closed")
            
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.NORMAL))
            
            new_nodes.append(TextNode(link_text, TextType.LINK, link_url))
            
            current_text = sections[1]
            
        if current_text != "":
            new_nodes.append(TextNode(current_text, TextType.NORMAL))
            
    return new_nodes
def text_to_textnodes(text):
    # 1. Adım: Her şey tek bir NORMAL metin düğümü olarak başlar
    nodes = [TextNode(text, TextType.NORMAL)]
    
    # 2. Adım: Sırasıyla tüm parçalayıcıları çağırıyoruz
    # Sıralama genellikle önemlidir; önce kalın/italik/kod, sonra resim/link
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    
    return nodes
