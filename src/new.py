from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        # TEXT yerine NORMAL kullanıyoruz
        if node.text_type != TextType.NORMAL:
            new_nodes.append(node)
            continue
        
        parts = node.text.split(delimiter)
        if len(parts) % 2 == 0:
            raise ValueError("Invalid markdown: delimiter not closed")
        
        split_nodes = []
        for i in range(len(parts)):
            if parts[i] == "":
                continue
            if i % 2 == 0:
                # Burası da NORMAL oldu
                split_nodes.append(TextNode(parts[i], TextType.NORMAL))
            else:
                split_nodes.append(TextNode(parts[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes
