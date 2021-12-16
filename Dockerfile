FROM jupyter/scipy-notebook

# Run as root
USER root
RUN python3 -m pip install --no-cache jupyterhub==1.5.0

# Add init notebooks script
COPY init_notebooks.py /srv/init_notebooks.py
RUN NOTEBOOK_DIR=/home/jovyan/work python /srv/init_notebooks.py

# Custom javascript
COPY custom /home/jovyan/.jupyter/custom

# Add custom nbreset extension
ADD nb-reset /srv/nb-reset
RUN python3 -m pip install --no-cache /srv/nb-reset plotly
RUN jupyter serverextension enable --py nbreset ; \
    jupyter nbextension install --py nbreset ; \
    jupyter nbextension enable --py nbreset

# Install mooc requirements
RUN wget https://raw.githubusercontent.com/INRIA/scikit-learn-mooc/master/requirements.txt
RUN python3 -m pip install --no-cache -r requirements.txt

# Run as jovyan (default user)
USER jovyan
