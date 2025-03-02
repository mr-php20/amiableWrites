import os
import csv
import requests
import time
from datetime import datetime

class InstagramUploader:
    def __init__(self, access_token, account_id, version="v19.0"):
        self.access_token = access_token
        self.account_id = account_id
        self.base_url = f"https://graph.facebook.com/{version}"
    
    def _print_request_details(self, method, url, params):
        """Print request details for debugging."""
        print("\n🔍 Request Details:")
        print(f"Method: {method}")
        print(f"URL: {url}")
        print("\nParameters:")
        for key, value in params.items():
            if key == 'access_token':
                print(f"  {key}: [HIDDEN]")
            elif key == 'caption':
                print(f"  {key}: (length: {len(value)} chars)")
            else:
                print(f"  {key}: {value}")
        print("-" * 50)
            
    def upload_image(self, github_url, caption):
        """Uploads image from GitHub URL."""
        try:
            params = {
                'image_url': github_url,
                'caption': caption,
                'access_token': self.access_token
            }
            
            upload_url = f"{self.base_url}/{self.account_id}/media"
            self._print_request_details('POST', upload_url, params)
            
            response = requests.post(upload_url, data=params)
            result = response.json()
            
            print("\n📤 Response:", result)
            
            if "id" in result:
                print(f"✅ Media container created")
                return result["id"]
            else:
                print(f"❌ Upload Error: {result}")
                return None
                    
        except Exception as e:
            print(f"❌ Error uploading: {str(e)}")
            return None
            
    def publish_media(self, creation_id):
        """Publishes the uploaded media."""
        try:
            params = {
                'creation_id': creation_id,
                'access_token': self.access_token
            }
            
            publish_url = f"{self.base_url}/{self.account_id}/media_publish"
            self._print_request_details('POST', publish_url, params)
            
            response = requests.post(publish_url, data=params)
            result = response.json()
            
            print("\n📤 Response:", result)
            
            if "id" in result:
                print(f"✅ Published successfully: {result['id']}")
                return True
            else:
                print(f"❌ Publish Error: {result}")
                return False
                
        except Exception as e:
            print(f"❌ Error publishing: {str(e)}")
            return False

def process_schedule(csv_path, uploader, count=1):
    """Process the Instagram posting schedule."""
    try:
        with open(csv_path, "r", encoding='utf-8') as file:
            reader = csv.DictReader(file)
            
            for i, row in enumerate(reader):
                if i >= count:
                    print(f"\nReached limit of {count} posts")
                    break
                    
                print(f"\nProcessing post {i+1} of {count}")
                print(f"Image: {row['Filename']}")
                print(f"GitHub URL: {row['GitHub_URL']}")
                
                # Combine captions
                full_caption = row['CustomCaption'].strip()
                if full_caption:
                    full_caption += "\n\n"
                full_caption += f"{row['Caption']}\n\n{row['Hashtags']}"
                
                # Upload and publish
                creation_id = uploader.upload_image(row["GitHub_URL"], full_caption)
                
                if creation_id:
                    print("Waiting before publishing...")
                    time.sleep(5)
                    
                    success = uploader.publish_media(creation_id)
                    if success:
                        print(f"✅ Successfully posted: {row['Filename']}")
                    
                    print("Waiting before next post...")
                    time.sleep(5)
                
    except Exception as e:
        print(f"❌ Error processing schedule: {str(e)}")
        raise e

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(script_dir)
    csv_path = os.path.join(parent_dir, "haiku_schedule.csv")
    
    print(f"Reading schedule from: {csv_path}")
    
    # Create uploader instance
    uploader = InstagramUploader("EABZBR8GLcdg4BO2iZAK4QVvCAabBHNfyb6BW64GbXTH0zXCMFJRAGma38wZC2UmPUZCIuluPpjnJe8IZAGSAFSuStZA8vRHenrlm7vdsuB3lZAsZA46o482yAHuvoH9gath0pNQGrcOZBPKJj0Kuj3nqFtaPAkyWJXvPeerUGcjEogaZBz7z74qMktrtN9p4lxmKXi3LXCB00ovwzwH69UGoDgZAFaYS6YZD", "17841447987295598")
    
    # Process first 3 posts by default
    process_schedule(csv_path, uploader, count=1)
    
    print("\nScheduled posts have been processed!")

if __name__ == "__main__":
    main()
