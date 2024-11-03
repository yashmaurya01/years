import json
import requests
import tarfile
import pytesseract
from PIL import Image
import os
import tempfile
from pathlib import Path
from tqdm import tqdm

def download_tar(url, output_path):
    """Download a tar file from URL with progress indication"""
    print(f"Starting download from: {url}")
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    
    progress_bar = tqdm(
        total=total_size, 
        unit='iB', 
        unit_scale=True,
        desc='Downloading'
    )
    
    with open(output_path, 'wb') as file:
        for data in response.iter_content(chunk_size=1024*1024):
            size = file.write(data)
            progress_bar.update(size)
    
    progress_bar.close()
    print(f"Download completed. Saved to: {output_path}")

def process_images_in_tar(tar_path, output_dir):
    """Extract and perform OCR on images from tar file"""
    print(f"\nProcessing tar file: {tar_path}")
    print(f"Output directory: {output_dir}")
    
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    sample_dir = "sample_files"
    Path(sample_dir).mkdir(parents=True, exist_ok=True)
    
    with tarfile.open(tar_path, 'r:bz2') as tar:
        members = tar.getmembers()
        print(f"Total files in tar: {len(members)}")
        
        # Extract and save first 10 files
        print("\nFirst 10 files in tar:")
        for member in members[:10]:
            print(f"- {member.name} ({os.path.splitext(member.name)[1]})")
            tar.extract(member, path=sample_dir)
            
        # Count all unique extensions
        extensions = {}
        for member in members:
            ext = os.path.splitext(member.name)[1].lower()
            extensions[ext] = extensions.get(ext, 0) + 1
            
        print("\nFile extension distribution:")
        for ext, count in extensions.items():
            print(f"- {ext}: {count} files")
        
        print(f"\nExtracted first 10 files to: {os.path.abspath(sample_dir)}")

def main():
    print("Starting OCR processing script")
    
    # Read OCR JSON file
    json_path = 'data/ocr.json'
    print(f"Reading JSON file: {json_path}")
    with open(json_path, 'r') as f:
        ocr_data = json.load(f)
    
    print(f"JSON data loaded. Found {len(ocr_data['ocr'])} entries")
    
    # Get first URL from OCR data
    first_url = ocr_data['ocr'][0]['url']
    print(f"Processing URL: {first_url}")
    
    # Create temporary directory for downloaded tar
    with tempfile.NamedTemporaryFile(suffix='.tar.bz2', delete=False) as tmp_tar:
        download_tar(first_url, tmp_tar.name)
        
        # Process images
        output_dir = 'ocr_results'
        process_images_in_tar(tmp_tar.name, output_dir)
        
        # Cleanup
        print(f"Cleaning up temporary tar file: {tmp_tar.name}")
        os.unlink(tmp_tar.name)
    
    print("\nScript completed!")

if __name__ == "__main__":
    main()