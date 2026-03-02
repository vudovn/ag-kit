import json
import shutil
import os

def sync_files():
    with open('file_diffs.json', 'r') as f:
        diffs = json.load(f)
    
    source_base = "C:\\repos\\antigravity-kit"
    dest_base = "c:\\repos_pn\\antigravity-kit"
    
    all_files = diffs['new'] + diffs['modified']
    
    for rel_path in all_files:
        src = os.path.join(source_base, rel_path)
        dst = os.path.join(dest_base, rel_path)
        
        # Ensure destination directory exists
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        
        print(f"Copying: {rel_path}")
        shutil.copy2(src, dst)
    
    print(f"\nSuccessfully synced {len(all_files)} files.")

if __name__ == "__main__":
    sync_files()
