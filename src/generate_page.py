import os
from markdown_blocks import generate_page 

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path,basepath):
    
    entries = os.listdir(dir_path_content)
    
    for entry in entries:
        
        from_path = os.path.join(dir_path_content, entry)
        dest_path = os.path.join(dest_dir_path, entry)
        
        
        if os.path.isfile(from_path):
            
            if from_path.endswith(".md"):
                
                dest_html_path = dest_path.replace(".md", ".html")
                
                generate_page(from_path, template_path, dest_html_path,basepath)
        
        # (recursive call)
        else:
            generate_pages_recursive(from_path, template_path, dest_path,basepath)
