from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import uuid
import os
from pathlib import Path

UPLOAD_FOLDER = os.path.join('Datastore', 'imgs')
SEMANTIC_FOLDER = os.path.join('Datastore', 'semantics')
MIDI_FOLDER = os.path.join('Datastore', 'midi')
VOCAB_PATH = os.path.join('Data','vocabulary_semantic.txt')
PRIMUS_CONVERTER_PATH = os.path.join('primus_converter', 'primus_conversor', 'app_semantic_conversor.sh')
OMR_FOLDER = 'OMR'
MODEL_FOLDER = 'Models'
# MODEL_NAME = 'trained_semantic_model-7500.meta'
MODEL_NAME = 'semantic_model.meta'

SONGS = [
    # {
    #     'id': "62a06c6471624e4891e92003006237b1",
    #     'title': 'Rick Rollllll',
    #     'original_filename': '000051652-1_2_1.png',
    #     'filepath': os.path.join(MIDI_FOLDER, str(id) + ".mid"),
    #     'semantics': 'clef-C1 keySignature-EbM timeSignature-2/4 multirest-23 barline rest-quarter rest-eighth note-Bb4_eighth barline note-Bb4_quarter. note-G4_eighth barline note-Eb5_quarter. note-D5_eighth barline note-C5_eighth note-C5_eighth rest-quarter',
    # }
]

# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

# sanity check route
@app.route('/songs', methods=['GET', 'POST'])
def all_songs():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        print(request.files)
        print(request.form)
        # validate file
        if 'image_file' not in request.files:
            response_object['status'] = 'failed'
            print("no file my friend")
            return jsonify(response_object)
        # parse file
        file = request.files['image_file']
        if not file.filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            response_object['status'] = 'failed'
            print("are you injecting an invalid image, hacker?")
            return jsonify(response_object)

        # extract file_extension
        original_filename_wo_ext, file_extension = os.path.splitext(file.filename)

        # parse title
        title = request.form['title']
        # generate id
        id = uuid.uuid4().hex
        # generate filename
        filename = str(id) + file_extension
        # save uploaded file
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        # strip extension
        filename_new = Path(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        # predict semantics from music sheet
        semantic_filename = filename_new.with_suffix('.txt').name
        os.system("python " + os.path.join(OMR_FOLDER, "ctc_predict.py") + " -image " + os.path.join(UPLOAD_FOLDER, filename) + " -model " + os.path.join(MODEL_FOLDER , MODEL_NAME) + " -vocabulary " + VOCAB_PATH + " -output " + os.path.join(SEMANTIC_FOLDER, semantic_filename))

        # convert semantics to midi file
        midi_filename = filename_new.with_suffix('.mid').name
        print (PRIMUS_CONVERTER_PATH + " " + os.path.join(SEMANTIC_FOLDER, semantic_filename) + " " + os.path.join(MIDI_FOLDER ,midi_filename))
        os.system(PRIMUS_CONVERTER_PATH + " " + os.path.join(SEMANTIC_FOLDER, semantic_filename) + " " + os.path.join(MIDI_FOLDER ,midi_filename))

        # read semantic file
        semantics = ''
        with open(os.path.join(SEMANTIC_FOLDER, semantic_filename), 'r') as file:
            semantics = file.read().replace('\n', '')

        SONGS.append({
            'id': str(id),
            'title': title,
            'original_filename': original_filename_wo_ext + file_extension,
            'semantics': semantics,
        })

        response_object['id'] = str(id)
        response_object['title'] = title
        response_object['original_filename'] = original_filename_wo_ext + file_extension
        response_object['semantics'] = semantics
        response_object['message'] = 'Song added!'
        print("Semantic: ", response_object['semantics'])
    else:
        response_object['songs'] = SONGS
    return jsonify(response_object)

@app.route('/download/<song_id>', methods=['GET'])
def download(song_id):
    response_object = {'status': 'success'}
    post_data = request.get_json()

    for song in SONGS:
        if song['id'] == song_id:
            download_song = song

    try:
        download_song
    except NameError:
        return "invalid midi file"


    return send_from_directory(directory=MIDI_FOLDER, filename=str(download_song['id']) + ".mid")

def remove_song(song_id):
    for song in SONGS:
        if song['id'] == song_id:
            SONGS.remove(song)
            return True
    return False

@app.route('/songs/<song_id>', methods=['PUT', 'DELETE'])
def single_song(song_id):
    response_object = {'status': 'success'}
    if request.method == 'PUT':
        post_data = request.get_json()
        # remove then append again
        remove_song(song_id)
        SONGS.append({
            'id': uuid.uuid4().hex,
            'title': post_data.get('title'),
            'author': post_data.get('author'),
            'read': post_data.get('read')
        })
        response_object['message'] = 'Song updated!'
    if request.method == 'DELETE':
        remove_song(song_id)
        response_object['message'] = 'Song removed!'
    return jsonify(response_object)


if __name__ == '__main__':
    app.run()