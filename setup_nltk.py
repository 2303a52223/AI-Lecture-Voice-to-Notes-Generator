"""
NLTK Data Setup Script
Downloads required NLTK data packages
"""
import nltk
import ssl
import os

def setup_nltk():
    """Download all required NLTK data"""
    
    # Handle SSL certificate issues
    try:
        _create_unverified_https_context = ssl._create_unverified_context
    except AttributeError:
        pass
    else:
        ssl._create_default_https_context = _create_unverified_https_context
    
    # Required datasets
    datasets = [
        'punkt_tab',
        'stopwords',
        'averaged_perceptron_tagger_eng',
        'wordnet',
        'omw-1.4'
    ]
    
    print("📥 Downloading NLTK data packages...")
    print("=" * 40)
    
    success_count = 0
    fail_count = 0
    
    for dataset in datasets:
        try:
            print(f"  Downloading {dataset}...", end=" ")
            nltk.download(dataset, quiet=True)
            print("✅")
            success_count += 1
        except Exception as e:
            print(f"❌ ({e})")
            fail_count += 1
    
    print("=" * 40)
    print(f"✅ Successfully downloaded: {success_count}/{len(datasets)}")
    
    if fail_count > 0:
        print(f"❌ Failed: {fail_count}/{len(datasets)}")
        print("\nTip: If downloads fail due to SSL errors, try running:")
        print("  python -c \"import nltk; nltk.download('all')\"")
    else:
        print("\n🎉 All NLTK data packages installed successfully!")

if __name__ == "__main__":
    setup_nltk()
