import sys
import os
import shutil
from copy_static import copy_files_recursive
from markdown_blocks import markdown_to_html_node, extract_title
from generate_page import generate_pages_recursive
def main():
    basepath = "/"
    if len(sys.argv) > 1:
        basepath = sys.argv[1]

    source_static = "./static"
    dest_public = "./docs"
    content_dir = "./content"
    template_file = "template.html"

    # 1. Temizlik
    print("Cleaning public directory...")
    if os.path.exists(dest_public):
        shutil.rmtree(dest_public)

    # 2. Statik dosyaları kopyala
    print("Copying static files...")
    copy_files_recursive(source_static, dest_public)

    # 3. Tüm sayfaları özyinelemeli olarak üret
    print("Generating all pages...")
    generate_pages_recursive(content_dir, template_file, dest_public, basepath)

if __name__ == "__main__":
    main()
