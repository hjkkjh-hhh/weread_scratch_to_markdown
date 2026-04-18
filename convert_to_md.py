import re
from markdownify import markdownify as md
from bs4 import BeautifulSoup
import os
import glob

def clean_html_block(html_content, section_title):
    try:
        soup = BeautifulSoup(html_content, 'html.parser')
        body = soup.find('body')
        if not body:
            content_to_convert = html_content
        else:
            # First, check for images in headers to preserve them
            for h in body.find_all(['h1', 'h2', 'h3']):
                # If the header matches the section title or contains an image
                img = h.find('img')
                if img:
                    # Manually convert img to markdown to be safe
                    alt = img.get('alt', '')
                    src = img.get('src', '')
                    if src:
                        md_img = f"![{alt}]({src})"
                        h.replace_with(md_img)
                    else:
                        h.decompose()
                elif h.get_text().strip() == section_title:
                    # If no image and title matches, remove redundant header
                    h.decompose()
            content_to_convert = str(body)
            
        converted = md(content_to_convert, heading_style="ATX")
        
        # Cleanup: remove XML declarations and other artifacts just in case
        lines = converted.splitlines()
        cleaned_lines = []
        for line in lines:
            ls = line.strip()
            if ls.startswith('xml version="') or ls.startswith('<?xml'):
                continue
            cleaned_lines.append(line)
        
        converted = '\n'.join(cleaned_lines)
        converted = re.sub(r'\n{3,}', '\n\n', converted)
        return converted.strip()
    except Exception as e:
        print(f"Error cleaning block: {e}")
        return md(html_content, heading_style="ATX").strip()

def process_file(input_path, output_path):
    print(f"Converting: {os.path.basename(input_path)}")
    with open(input_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Split by markdown headers
    segments = re.split(r'^(#+ .*)$', content, flags=re.MULTILINE)
    
    result = []
    current_title = ""
    
    for seg in segments:
        if not seg.strip():
            continue
            
        if seg.startswith('#'):
            current_title = seg[seg.find(' ')+1:].strip()
            result.append(seg.strip())
        else:
            if '<?xml' in seg or '<html' in seg:
                html_docs = re.split(r'(<\?xml.*?\?>)', seg)
                merged_docs = []
                temp_doc = ""
                for part in html_docs:
                    if part.startswith('<?xml'):
                        if temp_doc:
                            merged_docs.append(temp_doc)
                        temp_doc = part
                    else:
                        temp_doc += part
                if temp_doc:
                    merged_docs.append(temp_doc)
                
                converted_parts = []
                for doc in merged_docs:
                    if doc.strip():
                        converted_parts.append(clean_html_block(doc, current_title))
                
                result.append('\n\n'.join(converted_parts))
            else:
                result.append(seg.strip())

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n\n'.join(result))

def batch_process(src_dir, dest_dir):
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
        print(f"Created output directory: {dest_dir}")
    
    files = glob.glob(os.path.join(src_dir, "*.md"))
    total = len(files)
    print(f"Found {total} files to process.")
    
    for i, f in enumerate(files):
        # Skip backup files
        if f.endswith("_original.md.bak") or f.endswith("_fixed.md"):
            continue
            
        filename = os.path.basename(f)
        output_path = os.path.join(dest_dir, filename)
        
        try:
            process_file(f, output_path)
            print(f"[{i+1}/{total}] Success: {filename}")
        except Exception as e:
            print(f"[{i+1}/{total}] Failed: {filename} - {e}")

if __name__ == "__main__":
    # Get current script directory
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    src = os.path.join(base_dir, "input_md")
    dest = os.path.join(base_dir, "output_md")
    
    batch_process(src, dest)
    print("Batch processing complete!")
