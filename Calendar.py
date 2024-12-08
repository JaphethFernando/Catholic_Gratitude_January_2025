import re

# Load data from the text file
with open('Calendar.txt', 'r', encoding='utf-8') as f:  # Add encoding='utf-8'
        data = f.read()

# Split data into chunks for each day, using a more specific split pattern
days = re.split(r'(December \d{1,31}:\s+)', data)[1:]
days = [days[i] + days[i+1] for i in range(0, len(days), 2)]

# Function to extract information for each day
def extract_day_info(day_str):
    # Extract Date
    date_match = re.search(r'December (\d{1,31}):\s+', day_str)
    if date_match:
        date_str = date_match.group(1)
        date = f"202512{date_str.zfill(2)}"  # Format date as YYYYMMDD

    # Extract Title
    title = day_str.split('\n')[0].strip()

    # Extract Bible verse
    bible_verse_match = re.search(r'Bible Verse:\s*"(.*?)"', day_str)
    bible_verse = bible_verse_match.group(1) if bible_verse_match else ""

    # Extract Bible reference
    bible_reference_match = re.search(r'Bible Verse:.+\s*(.*?)\s*$', day_str, re.MULTILINE)
    bible_reference = bible_reference_match.group(1) if bible_reference_match else ""

    # Extract Activities
    activities_match = re.search(r'Activities:\s*(.*)', day_str, re.DOTALL)
    activities = activities_match.group(1).strip() if activities_match else ""

    return date, title, bible_verse, bible_reference, activities

# Process each day's data
for day_str in days:
    date, title, bible_verse, bible_reference, activities = extract_day_info(day_str)

    # Format data into ICS structure
    ics_output = f"""
BEGIN:VEVENT
UID:event-{date}@example.com
DTSTAMP:20241129T022556Z
DTSTART;VALUE=DATE:{date}
DTEND;VALUE=DATE:{int(date) + 1}
SUMMARY:{title}
DESCRIPTION:Bible Verse: "{bible_verse}" \\n{bible_reference} \\n\\nActivities: {activities}
BEGIN:VALARM
TRIGGER:-P1D
ACTION:DISPLAY
DESCRIPTION:Reminder
END:VALARM
END:VEVENT"""

# Print ICS output to console
print(ics_output)
