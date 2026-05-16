"""
Test File Reader with actual CV files
"""

from utils.file_reader import FileReader
import os


reader = FileReader()


cvs_folder = "data/cvs"

print("=" * 70)
print("TESTING FILE READER WITH YOUR CVs")
print("=" * 70)

# Check if folder exists
if not os.path.exists(cvs_folder):
    print(f"❌ Error: Folder '{cvs_folder}' not found!")
    print("Please create the folder and add your CV files.")
else:
    
    all_files = os.listdir(cvs_folder)
    files = [f for f in all_files if f.lower().endswith(('.pdf', '.docx', '.txt'))]
    
    if not files:
        print(f"\n  No CV files (PDF/DOCX/TXT) found in '{cvs_folder}'")
        print(f"    Found {len(all_files)} other file(s) in the folder.")
        print("    Please add your CV files to this folder.")
    else:
        print(f"\n Found {len(files)} CV file(s) in the folder!")
        print(f"   Total files in folder: {len(all_files)}")
        print("\n" + "=" * 70)
        
        successful = 0
        failed = 0
        
        # Try to read each file
        for i, filename in enumerate(files, 1):
            file_path = os.path.join(cvs_folder, filename)
            
            print(f"\n{i}. {filename}")
            print("-" * 70)
            
            try:
                # Read the file
                text = reader.read_file(file_path)
                
             
                text_clean = ' '.join(text.split())  # Remove extra whitespace
                preview = text_clean[:250] if len(text_clean) > 250 else text_clean
                
                print(f"    Successfully read!")
                print(f"    Preview: {preview}...")
                print(f"    Total characters: {len(text):,}")
                print(f"    Total words: {len(text.split()):,}")
                print(f"    Total lines: {len(text.splitlines()):,}")
                
                successful += 1
                
            except Exception as e:
                print(f"    Error reading file!")
                print(f"    Error details: {str(e)}")
                failed += 1

        # Summary
        print("\n" + "=" * 70)
        print("SUMMARY")
        print("=" * 70)
        print(f"Total files found: {len(files)}")
        print(f" Successfully read: {successful}")
        print(f" Failed to read: {failed}")
        
        if successful > 0:
            print(f"\n Great! {successful} CV(s) ready for analysis!")
        
        if failed > 0:
            print(f"\n {failed} file(s) had errors. Please check them.")

print("\n" + "=" * 70)
print("File reader test complete!")
print("=" * 70)