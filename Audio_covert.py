from pydub import AudioSegment
import numpy as np
from scipy.fft import fft, fftfreq
import matplotlib.pyplot as plt
import pandas as pd

# Load your audio file
audio = AudioSegment.from_file("test.m4a", format="m4a")

# Convert audio to a numpy array
samples = np.array(audio.get_array_of_samples())
if audio.channels == 2:
    samples = samples.reshape((-1, 2))
    samples = samples.mean(axis=1)

# Get the sample rate
sample_rate = audio.frame_rate

# Get time values for the waveform
time = np.arange(len(samples)) / sample_rate

# Perform FFT to get frequency components
N = len(samples)
yf = fft(samples)
xf = fftfreq(N, 1 / sample_rate)

# Get the magnitude and frequencies
magnitude = np.abs(yf)
frequency = xf

# Only take the positive frequencies
magnitude = magnitude[:N // 2]
frequency = frequency[:N // 2]

# Create a DataFrame with the raw data
waveform_data = {
    'Time': time,
    'Amplitude': samples
}
waveform_df = pd.DataFrame(waveform_data)

# Calculate the number of samples per segment to match the waveform
segment_length = int(np.ceil(len(time) / len(frequency)))

# Repeat frequency and magnitude to match the time segments
repeated_frequency = np.repeat(frequency, segment_length)[:len(time)]
repeated_magnitude = np.repeat(magnitude, segment_length)[:len(time)]

# Create the combined DataFrame
combined_data = {
    'Time': time,
    'Amplitude': samples,
    'Frequency': repeated_frequency,
    'Magnitude': repeated_magnitude
}

combined_df = pd.DataFrame(combined_data)

# Save to CSV file
combined_df.to_csv('combined_data.csv', index=False)

# Print the combined DataFrame (optional)
print(combined_df.head())

# Plot the waveform and the frequency spectrum
fig, ax1 = plt.subplots(figsize=(12, 8))

# Plot the waveform with amplitude on the left y-axis
color = 'tab:blue'
ax1.set_xlabel('Time [s]')
ax1.set_ylabel('Amplitude', color=color)
ax1.plot(combined_df['Time'], combined_df['Amplitude'], color=color)
ax1.tick_params(axis='y', labelcolor=color)
ax1.grid()

# Create a second y-axis for frequency and magnitude
ax2 = ax1.twinx()
color = 'tab:red'
ax2.set_ylabel('Frequency [Hz] / Magnitude', color=color)
ax2.plot(combined_df['Time'], combined_df['Frequency'], color=color, linestyle='--', label='Frequency')
ax2.plot(combined_df['Time'], combined_df['Magnitude'], color='tab:green', linestyle=':', label='Magnitude')
ax2.tick_params(axis='y', labelcolor=color)

# Add legends
fig.legend(loc="upper right", bbox_to_anchor=(1,1), bbox_transform=ax1.transAxes)

# Show the plots
plt.tight_layout()
plt.show()
