from pydub import AudioSegment
import numpy as np
from scipy.fft import fft, fftfreq
import matplotlib.pyplot as plt
import pandas as pd

# Load your audio file
audio = AudioSegment.from_file("Final_Apex_Audio_Part_2.m4a", format="m4a")

# Convert audio to a numpy array
samples = np.array(audio.get_array_of_samples())
if audio.channels == 2:
    samples = samples.reshape((-1, 2))
    samples = samples.mean(axis=1)

# Get the sample rate
sample_rate = audio.frame_rate

# Get time values for the waveform
time = np.arange(len(samples)) / sample_rate

# Take the absolute value of the samples to ensure all amplitudes are positive
abs_samples = np.abs(samples)

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

# Calculate the number of samples per segment to match the waveform
segment_length = int(np.ceil(len(time) / len(frequency)))

# Repeat frequency and magnitude to match the time segments
repeated_frequency = np.repeat(frequency, segment_length)[:len(time)]
repeated_magnitude = np.repeat(magnitude, segment_length)[:len(time)]

# Create the combined DataFrame
combined_data = {
    'Time': time,
    'Amplitude': abs_samples,  # Using the absolute values of the samples
    'Frequency': repeated_frequency,
    'Magnitude': repeated_magnitude
}

combined_df = pd.DataFrame(combined_data)

# Save to CSV file
combined_df.to_csv('combined_data_2.csv', index=False)

# Print the first few rows of the DataFrame
print(combined_df.head())

# Plotting
fig, ax1 = plt.subplots(figsize=(12, 8))

color = 'tab:blue'
ax1.set_xlabel('Time [s]')
ax1.set_ylabel('Amplitude', color=color)
ax1.plot(combined_df['Time'], combined_df['Amplitude'], color=color)
ax1.tick_params(axis='y', labelcolor=color)
ax1.grid()

ax2 = ax1.twinx()
color = 'tab:red'
ax2.set_ylabel('Frequency [Hz] / Magnitude', color=color)
ax2.plot(combined_df['Time'], combined_df['Frequency'], color=color, linestyle='--', label='Frequency')
ax2.plot(combined_df['Time'], combined_df['Magnitude'], color='tab:green', linestyle=':', label='Magnitude')
ax2.tick_params(axis='y', labelcolor=color)

fig.legend(loc="upper right", bbox_to_anchor=(1, 1), bbox_transform=ax1.transAxes)

plt.tight_layout()
plt.show()
