from music21 import stream, converter,  note, chord, meter, tempo, scale



s = stream.Stream()#
sc = scale.MajorScale('C4')  
for pitch in sc.getPitches('C4', 'C5'):
    s.append(note.Note(pitch, quarterLength=0.5))

c = chord.Chord(["C4", "E4", "G4"])  
s.append(c)

s.show("text")  
