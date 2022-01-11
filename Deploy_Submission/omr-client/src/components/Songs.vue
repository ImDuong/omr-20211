<template>
  <div class="container">
    <div class="row">
      <div class="col-sm-10">
        <h1>OMR Songs</h1>
        <hr><br><br>
        <alert :message=message v-if="showMessage"></alert>
        <button type="button" class="btn btn-success btn-sm" v-b-modal.song-modal>Add Song</button>
        <br><br>
        <table class="table table-hover">
          <thead>
            <tr>
              <th scope="col">Title</th>
              <th scope="col">Semantics</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(song, index) in songs" :key="index">
              <td>{{ song.title }}</td>
              <td>{{ song.semantics }}</td>
              <td>
                <div class="btn-group" role="group">
                  
                  <button
                          type="button"
                          class="btn btn-danger btn-sm"
                          @click.prevent="downloadSong(song)"
                          >
                      Download
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    <b-modal ref="addSongModal"
            id="song-modal"
            title="Add a new song"
            hide-footer>
      <b-form  @submit="onSubmit" @reset="onReset" class="w-100">
        <b-form-file
      v-model="file1"
      required
      :state="Boolean(file1)"
      placeholder="Choose a file or drop it here..."
      drop-placeholder="Drop file here..."
    ></b-form-file>
    <div class="mt-3">Selected file: {{ file1 ? file1.name : '' }}</div>
      <b-form-group id="form-title-group"
                    label="Title:"
                    label-for="form-title-input">
          <b-form-input id="form-title-input"
                        type="text"
                        v-model="addSongForm.title"
                        required
                        placeholder="Enter title">
          </b-form-input>
        </b-form-group>
        <b-button-group>
          <b-button type="submit" variant="primary">Submit</b-button>
          <b-button type="reset" variant="danger">Reset</b-button>
        </b-button-group>
      </b-form>
    </b-modal>
    <b-modal ref="editSongModal"
            id="song-update-modal"
            title="Update"
            hide-footer>
      <b-form @submit="onSubmitUpdate" @reset="onResetUpdate" class="w-100">
      <b-form-group id="form-title-edit-group"
                    label="Title:"
                    label-for="form-title-edit-input">
          <b-form-input id="form-title-edit-input"
                        type="text"
                        v-model="editForm.title"
                        required
                        placeholder="Enter title">
          </b-form-input>
        </b-form-group>
        <b-form-group id="form-author-edit-group"
                      label="Author:"
                      label-for="form-author-edit-input">
            <b-form-input id="form-author-edit-input"
                          type="text"
                          v-model="editForm.author"
                          required
                          placeholder="Enter author">
            </b-form-input>
          </b-form-group>
        <b-form-group id="form-read-edit-group">
          <b-form-checkbox-group v-model="editForm.read" id="form-checks">
            <b-form-checkbox value="true">Read?</b-form-checkbox>
          </b-form-checkbox-group>
        </b-form-group>
        <b-button-group>
          <b-button type="submit" variant="primary">Update</b-button>
          <b-button type="reset" variant="danger">Cancel</b-button>
        </b-button-group>
      </b-form>
    </b-modal>
  </div>
</template>

<script>
import axios from 'axios';
import Alert from './Alert.vue';
import MidiPlayer from 'midi-player-js';

// Initialize player and register event handler
var Player = new MidiPlayer.Player(function(event) {
	console.log(event);
});

export default {
  data() {
    return {
      songs: [],
      addSongForm: {
        title: '',
        songFile: null,
      },
      message: '',
      showMessage: false,
      editForm: {
        id: '',
        title: '',
      },
      file1: null,
    };
  },
  components: {
    alert: Alert,
  },
  methods: {
    getSongs() {
      const path = 'http://localhost:5000/songs';
      axios.get(path)
        .then((res) => {
          this.songs = res.data.songs;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    downloadSong (song) {
      console.log(song);
      var song_id = song.id
      console.log(song_id)
      const path = 'http://localhost:5000/download/' + song_id;
      axios.get(path, { responseType: 'blob' })
        .then(response => {
          const blob = new Blob([response.data], { type: 'application/pdf' })
          const link = document.createElement('a')
          link.href = URL.createObjectURL(blob)
          link.download = song.original_filename.replace(/\.[^/.]+$/, "") + ".mid"
          link.click()
          URL.revokeObjectURL(link.href)
        }).catch(console.error)
    },
    playSong (song) {
      console.log(song);
      var song_id = song.id
      console.log(song_id)
      const path = 'http://localhost:5000/download/' + song_id;
      axios.get(path, { responseType: 'blob' })
        .then(response => {
          const blob = new Blob([response.data], { type: 'application/pdf' })
          Player.loadFile(blob);
          Player.play();
        }).catch(console.error)
    },
    addSong(payload) {
      const path = 'http://localhost:5000/songs';
      axios.post(path, payload)
        .then(() => {
          this.getSongs();
          this.message = 'Song added!';
          this.showMessage = true;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.log(error);
          this.getSongs();
        });
    },
    initForm() {
      this.addSongForm.title = '';
      this.addSongForm.songFile = null;
      this.editForm.id = '';
      this.editForm.title = '';
    },
    onSubmit(evt) {
      evt.preventDefault();
      this.$refs.addSongModal.hide();
      let read = false;
      var payload = new FormData();
      payload.append("image_file", this.file1, this.file1.name);
      payload.append("title", this.addSongForm.title);
      // const payload = {
      //   title: this.addSongForm.title,
      //   author: this.addSongForm.author,
      //   read, // property shorthand
      //   songFile: this.file1
      // };
      console.log(payload);
      this.addSong(payload);
      this.initForm();
    },
    onReset(evt) {
      evt.preventDefault();
      this.$refs.addSongModal.hide();
      this.initForm();
    },
    editSong(song) {
      this.editForm = song;
    },
    onSubmitUpdate(evt) {
      evt.preventDefault();
      this.$refs.editSongModal.hide();
      let read = false;
      const payload = {
        title: this.editForm.title,
      };
      this.updateSong(payload, this.editForm.id);
    },
    updateSong(payload, songID) {
      const path = `http://localhost:5000/songs/${songID}`;
      axios.put(path, payload)
        .then(() => {
          this.getSongs();
          this.message = 'Song updated!';
          this.showMessage = true;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
          this.getSongs();
        });
    },
    onResetUpdate(evt) {
      evt.preventDefault();
      this.$refs.editSongModal.hide();
      this.initForm();
      this.getSongs(); // why?
    },
    removeSong(songID) {
      const path = `http://localhost:5000/songs/${songID}`;
      axios.delete(path)
        .then(() => {
          this.getSongs();
          this.message = 'Song removed!';
          this.showMessage = true;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
          this.getSongs();
        });
    },
    onDeleteSong(song) {
      this.removeSong(song.id);
    },
  },
  created() {
    this.getSongs();
  },
};
</script>