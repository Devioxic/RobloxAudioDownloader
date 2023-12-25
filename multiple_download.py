from main import extract_audio_src

ids = [

]

names = [

]

for i in range(len(ids)):
    if len(names) < i:
        extract_audio_src(ids[i], ids[i])
    else:
        extract_audio_src(ids[i], names[i])