# Project Tech Stack
- Frontend: vuejs
- Backend: python (flask)

# Project Architecture
- Frontend: 
	+ Submit music image file and display semantics of added file
	+ Download midi file from server
- Backend: 
	+ Recognize music objects in sent music image file and write into semantic file
	+ Convert semantic file to midi file and store locally

# Project Structure
## Frontend
- Lies in folder `omr-client`
- `src/components/Songs.vue` contain the page for interacting with server
- `src/router/index.js` for routing
- `src/App.vue` for main page

## Backend
- Lies in folder `OMR-end-to-end`
- `app.py` host the server and control flow for converting step by calling python scripts
- folder `primus_converter` containing script to convert semantic file to midi file
  - the primus converter can be found at https://grfia.dlsi.ua.es/primus/
- put predict and model python script (from training repo) into folder `OMR`
- put trained model file (.meta) into folder `Models`
- structure folder `Datastore` as: 
	+ imgs
	+ midi
	+ semantics
- folder `Data` contains `vocabulary_semantic.txt` for semantic acknowledgement

# Run Project
## Frontend
- Locates in `omr-client` and run `npm run serve`

## Backend
- Install requirements from `requirements.txt`
- Locates in `OMR-end-to-end` and run `python app.py`



