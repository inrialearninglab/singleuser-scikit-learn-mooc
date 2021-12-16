FROM jupyter/scipy-notebook

# Run as jovyan (default user)
USER jovyan

# Install jupyterhub and nbgitpuller
RUN python3 -m pip install --no-cache jupyterhub==1.5.0 nbgitpuller==1.0.2

# Install mooc requirements
RUN wget https://raw.githubusercontent.com/INRIA/scikit-learn-mooc/master/requirements.txt
RUN python3 -m pip install --no-cache -r requirements.txt

# Custom javascript
COPY custom /home/jovyan/.jupyter/custom

# Add custom nbreset extension
ADD nb-reset /srv/nb-reset
RUN python3 -m pip install --no-cache /srv/nb-reset
RUN jupyter serverextension enable --py nbreset ; \
    jupyter nbextension install --py nbreset ; \
    jupyter nbextension enable --py nbreset

# Enable
RUN jupyter serverextension enable --py nbgitpuller --sys-prefix

# Add init notebooks script
COPY init_notebooks.py /srv/init_notebooks.py
# Preload notebooks in tmp directory
RUN mkdir /tmp/work; NOTEBOOK_DIR=/tmp/work python /srv/init_notebooks.py
