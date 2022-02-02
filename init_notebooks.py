# Script to initialize learner environment (notebooks and datasets)

import json
import os
import urllib.error
import urllib.request
import concurrent.futures


def download_file(entry):
    path, url = entry
    if not (os.path.exists(path)):
        try:
            urllib.request.urlretrieve(url, path)
            filename, ext = os.path.splitext(path)
            print('Downloaded ' + filename)
            if ext == ".ipynb":
                add_nb_metadata(path, url)
                print('Add metadata ' + filename)

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
    # Url of the json files that lists all the needed content
    base_url = 'https://gist.githubusercontent.com/brospars/c86986af126c17d3ede848b11e3a5a65/raw/'
    notebook_list_url = base_url + 'notebooks.json'

    notebook_dir = os.environ.get('NOTEBOOK_DIR')
    if not notebook_dir:
        print("Error notebook dir")
    elif not (os.path.isdir(notebook_dir)):
        print("Notebook dir not exists")
    else:
        # Read json and iterate on notebooks and datasets
        with urllib.request.urlopen(notebook_list_url) as content:
            data = json.loads(content.read().decode())

            # Create /notebooks
            if not os.path.exists(os.path.join(notebook_dir, 'notebooks')):
                os.mkdir(os.path.join(notebook_dir, 'notebooks'))

            # Create /notebooks/helpers
            if not os.path.exists(os.path.join(notebook_dir, 'notebooks', 'helpers')):
                os.mkdir(os.path.join(notebook_dir, 'notebooks', 'helpers'))

            # Create /datasets
            if not os.path.exists(os.path.join(notebook_dir, 'datasets')):
                os.mkdir(os.path.join(notebook_dir, 'datasets'))

            # Create /figures
            if not os.path.exists(os.path.join(notebook_dir, 'figures')):
                os.mkdir(os.path.join(notebook_dir, 'figures'))

            # Create list of file to download
            download_entries = []
            # Add start guide notebook
            nb_guide_url = base_url + 'JupyterNotebookGuide.ipynb'
            nb_guide_path = os.path.join(notebook_dir, 'notebooks', 'JupyterNotebookGuide.ipynb')
            download_entries.append((nb_guide_path, nb_guide_url))

            # Add notebooks
            for notebook in data['notebooks']:
                nb_path = os.path.join(notebook_dir, os.path.dirname(notebook), os.path.basename(notebook))
                download_entries.append((nb_path, data['baseUrl'] + notebook))
            # Add datasets
            for dataset in data['datasets']:
                data_path = os.path.join(notebook_dir, 'datasets', os.path.basename(dataset))
                download_entries.append((data_path, data['baseUrl'] + dataset))
            # Add figures
            for figure in data['figures']:
                figure_path = os.path.join(notebook_dir, 'figures', os.path.basename(figure))
                download_entries.append((figure_path, data['baseUrl'] + figure))

            # Parallel download file using threads
            with concurrent.futures.ThreadPoolExecutor() as exector:
                exector.map(download_file, download_entries)

            # Create empty wrapups
            for wrapup in data['wrapups']:
                wrapup_path = os.path.join(notebook_dir, 'notebooks', os.path.basename(wrapup))
                if not (os.path.exists(wrapup_path)):
                    # Create empty notebook
                    with open(wrapup_path, "w") as wrapup_nb:
                        wrapup_nb.write('{"cells":[],"metadata":{},"nbformat":4,"nbformat_minor":4}')
                        print('Creating ' + wrapup_path)


if __name__ == "__main__":
    main()
