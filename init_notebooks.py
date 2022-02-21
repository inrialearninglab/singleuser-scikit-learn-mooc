# Script to initialize learner environment (notebooks and datasets)

import json
import os
import urllib.error
import urllib.request
import concurrent.futures

repo_base_url = 'https://raw.githubusercontent.com/inrialearninglab/singleuser-scikit-learn-mooc/master/'
skl_mooc_base_url = 'https://raw.githubusercontent.com/INRIA/scikit-learn-mooc/main/'
skl_api_base_url = 'https://api.github.com/repos/INRIA/scikit-learn-mooc/contents/'

notebook_dir = os.environ.get('NOTEBOOK_DIR')


def get_filelist(directory):
    filelist = []
    print('Fetching : ' + directory)
    with urllib.request.urlopen(skl_api_base_url + directory) as response:
        entries = json.loads(response.read().decode())
        for entry in entries:
            if entry['type'] == 'file':
                if '_sol_' not in entry['name']:
                    filelist.append((os.path.join(notebook_dir, entry['path']), entry['download_url']))
            elif entry['type'] == 'dir':
                filelist.extend(get_filelist(entry['path']))
            else:
                print('Error entry type not supported')
        return filelist


def download_file(entry):
    path, url = entry
    if not (os.path.exists(path)):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        try:
            urllib.request.urlretrieve(url, path)
            filename, ext = os.path.splitext(path)
            print('Downloaded ' + filename)
            if ext == ".ipynb":
                add_nb_metadata(path, url)
                print('Add metadata ' + path)

        # In case of request error
        except urllib.error.URLError:
            print('Error downloading ' + url)


# Edit metadata to add source url (used for reset)
def add_nb_metadata(notebook_path, notebook_url):
    with open(notebook_path, "r") as nb_in:
        nb_in_data = json.load(nb_in)
    nb_in_data["metadata"]["nbreset"] = notebook_url
    with open(notebook_path, "w") as nb_out:
        json.dump(nb_in_data, nb_out)


def main():
    if not notebook_dir:
        print("Error notebook dir")
    elif not (os.path.isdir(notebook_dir)):
        print("Notebook dir not exists")
    else:
        download_entries = []

        # Add start guide notebook
        nb_guide_url = repo_base_url + 'JupyterNotebookGuide.ipynb'
        nb_guide_path = os.path.join(notebook_dir, 'notebooks', 'JupyterNotebookGuide.ipynb')
        download_entries.append((nb_guide_path, nb_guide_url))

        dir_to_sync = ['datasets', 'figures', 'notebooks']

        for directory in dir_to_sync:
            download_entries.extend(get_filelist(directory))

        # Parallel download file using threads
        with concurrent.futures.ThreadPoolExecutor() as exector:
            exector.map(download_file, download_entries)

        # Create empty wrapups
        for wrapup in [
            "evaluation/ensemble_questions.ipynb",
            "evaluation/linear_models_questions.ipynb",
            "evaluation/trees_questions.ipynb",
            "evaluation/predictive_modeling_pipeline_questions.ipynb",
            "evaluation/overfit_questions.ipynb",
            "evaluation/tuning_questions.ipynb",
            "evaluation/evaluation_questions.ipynb",
            "evaluation/sandbox_notebook.ipynb"
        ]:
            wrapup_path = os.path.join(notebook_dir, 'notebooks', os.path.basename(wrapup))
            if not (os.path.exists(wrapup_path)):
                # Create empty notebook
                with open(wrapup_path, "w") as wrapup_nb:
                    wrapup_nb.write('{"cells":[],"metadata":{},"nbformat":4,"nbformat_minor":4}')
                    print('Creating ' + wrapup_path)


if __name__ == "__main__":
    main()
