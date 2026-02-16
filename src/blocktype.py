from enum import Enum
from htmlnode import LeafNode

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def block_to_block_type(block):
    # --- HEADING KONTROLÜ ---
    # 1-6 arası # ve ardından bir boşluk
    if (
        block.startswith("# ") or 
        block.startswith("## ") or 
        block.startswith("### ") or 
        block.startswith("#### ") or 
        block.startswith("##### ") or 
        block.startswith("###### ")
    ):
        return BlockType.HEADING

    # --- CODE BLOCK KONTROLÜ ---
    # En az 6 karakter (```...```) ve doğru başlangıç/bitiş
    if len(block) >= 6 and block.startswith("```") and block.endswith("```"):
        return BlockType.CODE

    lines = block.split("\n")

    # --- QUOTE KONTROLÜ ---
    if block.startswith(">"):
        is_quote = True
        for line in lines:
            if not line.startswith(">"):
                is_quote = False
                break
        if is_quote:
            return BlockType.QUOTE

    # --- UNORDERED LIST KONTROLÜ ---
    if block.startswith("- "):
        is_unordered = True
        for line in lines:
            if not line.startswith("- "):
                is_unordered = False
                break
        if is_unordered:
            return BlockType.UNORDERED_LIST

    # --- ORDERED LIST KONTROLÜ ---
    if block.startswith("1. "):
        is_ordered = True
        for i in range(len(lines)):
            # Her satırın (i+1). şeklinde başladığını kontrol ediyoruz
            expected_prefix = f"{i + 1}. "
            if not lines[i].startswith(expected_prefix):
                is_ordered = False
                break
        if is_ordered:
            return BlockType.ORDERED_LIST

    # Hiçbir şeye uymuyorsa paragraftır
    return BlockType.PARAGRAPH
