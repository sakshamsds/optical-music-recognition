# Import necessary libraries
from midiutil import MIDIFile
import pygame

# Open the file containing the detected notes and load its contents into a list
with open('./results/detected_notes.txt', 'r') as f:
    data = [eval(line) for line in f.readlines()]
    
# Define a dictionary that maps note names to their durations
notes = {
    "eighth": 1/2,
    "quarter": 1,
    "half": 2,
    "whole": 4
}

# Set the tempo and time signature
tempo = 120
time_signature = (4, 4)

# Create a MIDI file with one track
midi_file = MIDIFile(1)

# Set the time signature of the MIDI file
midi_file.addTimeSignature(0, 0, *time_signature, clocks_per_tick=24)

# Set the tempo of the MIDI file
midi_file.addTempo(0, 0, tempo)

# Define a dictionary that maps note names to their corresponding frequencies
pitches = {'C': 261.63, 'C#': 277.18, 'D': 293.66, 'D#': 311.13, 'E': 329.63, 'F': 349.23, 'F#': 369.99,
         'G': 392.00, 'G#': 415.30, 'A': 440.00, 'A#': 466.16, 'B': 493.88}

# Find the maximum frequency in the pitches dictionary
max_freq = max(pitches.values())

# Generate a melody using the detected notes
melody = []
for detection in data:
    note = detection[0]
    duration = notes[note]
    pitch = int(pitches[detection[1]] / max_freq * 255)
    volume = 100
    melody.append((note, duration, pitch, volume))

# Add the melody to the MIDI file
time = 0
channel = 0
for note, duration, pitch, volume in melody:
    midi_file.addNote(0, channel, pitch, time, duration, volume)
    time += duration

# Write the MIDI data to a file
with open("./results/melody.mid", "wb") as file:
    midi_file.writeFile(file)
    
# Initialize pygame
pygame.init()

# Load the MIDI file into Pygame's mixer
pygame.mixer.music.load('./results/melody.mid')

# Play MIDI file
pygame.mixer.music.play()

# Wait for the MIDI file to finish playing
while pygame.mixer.music.get_busy():
    # Check if the user wants to stop playing the MIDI file
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            pygame.mixer.music.stop()
    # Limit the loop's speed to 10 times per second
    pygame.time.Clock().tick(10)

# Clean up resources
pygame.quit()

    
    
    

