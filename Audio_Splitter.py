from pydub import AudioSegment

# Load your audio file
audio = AudioSegment.from_file("Final_Apex_Audio.m4a", format="m4a")

# Calculate the duration of each part in milliseconds
part_duration = len(audio) // 5

# Split and save each part
for i in range(5):
    start_time = i * part_duration
    end_time = (i + 1) * part_duration if i < 4 else len(audio)  # Ensure the last part includes the remainder
    part = audio[start_time:end_time]
    part.export(f"Final_Apex_Audio_Part_{i+1}.m4a", format="m4a")

print("Audio has been split into 5 parts successfully.")
