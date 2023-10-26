import os
import shutil
import subprocess
import urllib.request, json
from tornado import web
from notebook.base.handlers import IPythonHandler


def _build_msg_json(**kwargs):
    return dict(**kwargs)


os.chdir('/home/jovyan')


class NbResetHandler(IPythonHandler):
    @web.authenticated
    def post(self):
        nb_url = self.get_argument('nburl')
        nb_path = os.path.join(os.getcwd(), self.get_argument('nbpath'))

        if nb_url:
            with urllib.request.urlopen(nb_url) as url:
                nb_data = json.loads(url.read().decode())

                nb_data["metadata"]["nbreset"] = nb_url

                with open(nb_path, "w") as nb_out:
                    json.dump(nb_data, nb_out)
                    msg_json = _build_msg_json(title="Reset successful", body="Your notebook has been reset")
        else:
            msg_json = _build_msg_json(title="Error", body="Missing notebook url")

        self.write(msg_json)
        self.flush()


class NbResetAllHandler(IPythonHandler):
    @web.authenticated
    def post(self):
        folder = '/home/jovyan'
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path) and os.path.basename(file_path) != 'wrapups':
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))

        result = subprocess.run(['python', '/srv/init_notebooks.py'], env=dict(os.environ, NOTEBOOK_DIR=folder))
        if result.returncode != 0:
            msg_json = _build_msg_json(title="Reset error", body="Something went wrong")
        else:
            msg_json = _build_msg_json(title="Reset successful", body="Notebooks have been reset")
        self.write(msg_json)
        self.flush()


class NbResetDatasetsHandler(IPythonHandler):
    @web.authenticated
    def post(self):
        folder = '/home/jovyan'
        try:
            shutil.rmtree(folder + '/datasets') 
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))
        
        result = subprocess.run(['python', '/srv/init_notebooks.py'], env=dict(os.environ, NOTEBOOK_DIR=folder))
        if result.returncode != 0:
            msg_json = _build_msg_jsonf(title="Reset error", body="Something went wrong")
        else:
            msg_json = _build_msg_json(title="Reset successful", body="Datasets have been reset")

        self.write(msg_json)
        self.flush()
