# fix_bom.py
import sys

def remove_bom(filepath):
    with open(filepath, 'rb') as f:
        content = f.read()
    
    # Remove UTF-8 BOM if present
    if content.startswith(b'\xef\xbb\xbf'):
        content = content[3:]
        with open(filepath, 'wb') as f:
            f.write(content)
        print(f"BOM removed from {filepath}")
    else:
        print(f"No BOM found in {filepath}")

if __name__ == '__main__':
    remove_bom('D:\\Programming\\Wigs\\soie\\backend\\soie_data.json')