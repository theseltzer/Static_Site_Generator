import os
from htmlnode import ParentNode, LeafNode
from inline_markdown import text_to_textnodes
from textnode import text_node_to_html_node


class BlockType:
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def block_to_block_type(block):
    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    if len(block) >= 6 and block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    if block.startswith(">"):
        return BlockType.QUOTE
    if block.startswith("* ") or block.startswith("- "):
        return BlockType.UNORDERED_LIST
    if block[0].isdigit() and block.startswith(". ", 1):
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH



def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    filtered_blocks = []
    for block in blocks:
        cleaned_block = block.strip()
        if cleaned_block != "":
            filtered_blocks.append(cleaned_block)
    return filtered_blocks

def text_to_children(text):
    
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children

def paragraph_to_html_node(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)

def heading_to_html_node(block):
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    content = block[level + 1 :].strip()
    children = text_to_children(content)
    return ParentNode(f"h{level}", children)

def quote_to_html_node(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("Invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)

def code_to_html_node(block):
    text = block.strip("```").strip()
    code_node = LeafNode("code", text)
    return ParentNode("pre", [code_node])

def ulist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[2:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ul", html_items)

def olist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        pos = item.find(". ")
        text = item[pos + 2 :]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ol", html_items)

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == BlockType.HEADING:
            node = heading_to_html_node(block)
        elif block_type == BlockType.CODE:
            node = code_to_html_node(block)
        elif block_type == BlockType.QUOTE:
            node = quote_to_html_node(block)
        elif block_type == BlockType.UNORDERED_LIST:
            node = ulist_to_html_node(block)
        elif block_type == BlockType.ORDERED_LIST:
            node = olist_to_html_node(block)
        else:
            node = paragraph_to_html_node(block)
        children.append(node)
    return ParentNode("div", children)

def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:].strip()
    raise Exception("No h1 header found in markdown")

def generate_page(from_path, template_path, dest_path,basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    
    with open(from_path, "r", encoding="utf-8") as f:
        markdown_content = f.read()
    with open(template_path, "r", encoding="utf-8") as f:
        template = f.read()

    html_node = markdown_to_html_node(markdown_content)
    content_html = html_node.to_html()
    title = extract_title(markdown_content)

    template = template.replace('href="/', f'href="{basepath}')
    template = template.replace('src="/', f'src="{basepath}')

    dest_dir_path = os.path.dirname(dest_path)
    if dest_dir_path != "":
        os.makedirs(dest_dir_path, exist_ok=True)

    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(template)
