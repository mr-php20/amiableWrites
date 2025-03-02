import os
import csv
import time
from datetime import datetime, timedelta

def create_github_url(category, filename):
    """Create GitHub raw URL for image."""
    base_url = "https://raw.githubusercontent.com/mr-php20/amiableWrites/refs/heads/main"
    folder_map = {
        "White": "White",
        "Black": "Black",
        "Color": "Spectrum"  # Color images are in Other folder on GitHub
    }
    return f"{base_url}/{folder_map[category]}/{filename}"

def generate_schedule(white_folder, black_folder, color_folder, output_csv, start_date):
    """Generates a CSV file for scheduling Instagram posts."""
    
    # Get absolute paths
    white_folder = os.path.abspath(white_folder)
    black_folder = os.path.abspath(black_folder)
    color_folder = os.path.abspath(color_folder)
    
    # Get files with full paths
    white_images = sorted([os.path.join(white_folder, f) for f in os.listdir(white_folder)])
    black_images = sorted([os.path.join(black_folder, f) for f in os.listdir(black_folder)])
    color_images = sorted([os.path.join(color_folder, f) for f in os.listdir(color_folder)])
    
    caption = (
        "Save this poem as your little love reminder to brighten your day. "
        "If it touched your heart, leave a ❤, and share it with someone who needs to hear this. "
        "Let's spread love... save it, share it!\n\n"
        "இக்கவிதையை உங்கள் நாளை சிறப்பாக்கும் காதல் நினைவாக சேமியுங்கள். "
        "இதன் உணர்வுகள் உங்கள் இதயத்தை தழுவி இருந்தால், ❤ கொடுக்கவும், "
        "இதை உணர வேண்டியவருடன் பகிரவும். காதலை பரப்புவோம்... சேமியுங்கள், பகிருங்கள்!"
    )
    
    hashtags = (
        "#amiablewrites #kadhalthinamthinam #meendumorkadhalmazhai #karpanaiyokadhalvasam "
        "#peachhouseperson #Arivalan\n\n"
        "#TamilKavithai #TamilPoetry #TamilLovePoems #KadhalKavithai #RomanticKavithai "
        "#TamilKadhal #TamilQuotes #TamilKadhalKavithaigal #RomanticQuotes "
        "#TamilKavithaigal #TamilLoveQuotes #TamilSadQuotes #TamilThathuvangal #TamilKavidhai "
        "#TamilPoems #TamilKavithaikal #TamilLoveStory #PoetryInTamil #LoveInTamil "
        "#TamilRomanticQuotes #TamilInstaPoetry #TamilQuoteLovers #InstaKavithai #KadhalInstagram"
    )
    
    # Adjust start time to 6 PM IST (UTC+5:30)
    base_date = datetime.strptime(start_date, "%Y-%m-%d %H:%M:%S")
    ist_time = base_date.replace(hour=18, minute=0, second=0)  # 6:00 PM
    
    schedule = []
    date = ist_time
    
    for i in range(min(len(white_images), len(black_images), len(color_images))):
        if i < len(white_images):
            timestamp = int(time.mktime(date.timetuple()))
            filename = os.path.basename(white_images[i])
            github_url = create_github_url("White", filename)
            schedule.append([
                date.strftime("%Y-%m-%d %H:%M:%S"),
                "White",
                filename,
                white_images[i],
                github_url,
                hashtags,
                caption,
                "",  # Custom Caption (empty by default)
                "Tamil, English",
                timestamp
            ])
            date += timedelta(days=1)

        if i < len(black_images):
            timestamp = int(time.mktime(date.timetuple()))
            filename = os.path.basename(black_images[i])
            github_url = create_github_url("Black", filename)
            schedule.append([
                date.strftime("%Y-%m-%d %H:%M:%S"),
                "Black",
                filename,
                black_images[i],
                github_url,
                hashtags,
                caption,
                "",  # Custom Caption (empty by default)
                "Tamil, English",
                timestamp
            ])
            date += timedelta(days=1)

        if i < len(color_images):
            timestamp = int(time.mktime(date.timetuple()))
            filename = os.path.basename(color_images[i])
            github_url = create_github_url("Color", filename)
            schedule.append([
                date.strftime("%Y-%m-%d %H:%M:%S"),
                "Color",
                filename,
                color_images[i],
                github_url,
                hashtags,
                caption,
                "",  # Custom Caption (empty by default)
                "Tamil, English",
                timestamp
            ])
            date += timedelta(days=1)

    # Write CSV with GitHub URLs
    output_csv = os.path.abspath(output_csv)
    with open(output_csv, "w", newline="", encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([
            "Date", "Category", "Filename", "Filepath", "GitHub_URL",
            "Hashtags", "Caption", "CustomCaption", "Languages", "Publish_Timestamp"
        ])
        writer.writerows(schedule)

    print(f"✅ Schedule generated successfully!")
    print(f"📁 Saved to: {output_csv}")
    print(f"📊 Total entries: {len(schedule)}")
    print(f"📅 Date range: {schedule[0][0]} to {schedule[-1][0]}")

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(script_dir)

    white_folder = os.path.join(parent_dir, "InstaAutomation", "KadhalThinamThinamInsta", "White")
    black_folder = os.path.join(parent_dir, "InstaAutomation", "KadhalThinamThinamInsta", "Black")
    color_folder = os.path.join(parent_dir, "InstaAutomation", "KadhalThinamThinamInsta", "Spectrum")
    output_csv = "haiku_schedule.csv"
    start_date = "2025-03-20 18:00:00"  # 6:00 PM IST

    generate_schedule(white_folder, black_folder, color_folder, output_csv, start_date)