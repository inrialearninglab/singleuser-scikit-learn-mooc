FROM jupyter/scipy-notebook:notebook-6.5.4

# Add custom nbreset extension
ADD ./nb-reset/dist/nbreset-0.0.1-py3-none-any.whl /srv/nbreset-0.0.1-py3-none-any.whl
RUN python3 -m pip install /srv/nbreset-0.0.1-py3-none-any.whl

# Install custom nbreset extension
USER root
RUN jupyter nbextension install --py nbreset

# Run as jovyan (default user)
USER jovyan

# Install jupyterhub and nbgitpuller
RUN python3 -m pip install --no-cache jupyterhub==1.5.0 nbgitpuller==1.0.2

# Install mooc requirements
RUN wget https://raw.githubusercontent.com/INRIA/scikit-learn-mooc/master/requirements.txt
RUN python3 -m pip install --no-cache -r requirements.txt

# Custom javascript
COPY custom /tmp/custom

# Enable extensions
RUN jupyter serverextension enable --py nbgitpuller --sys-prefix
RUN jupyter serverextension enable --py nbreset ; \
    jupyter nbextension enable --py nbreset

# Add init notebooks script
COPY init_notebooks.py /srv/init_notebooks.py
# Preload notebooks in tmp directory
RUN mkdir /tmp/home; NOTEBOOK_DIR=/tmp/home python /srv/init_notebooks.py