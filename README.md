# Jupyterhub singleuser image for the scikit-learn mooc

## Usage

Test locally 

```shell
# Build
docker build -t brospars/singleuser-scikit-learn-mooc:latest .

# As normal user
docker run -p 8888:8888 brospars/singleuser-scikit-learn-mooc:latest /bin/bash -c "cp -rup /tmp/home/* /home/jovyan; cp -rup /tmp/custom /home/jovyan/.jupyter; jupyter notebook;"

# As root
docker run --user=root -p 8888:8888 brospars/singleuser-scikit-learn-mooc:root /bin/bash -c "cp -rup /tmp/home/* /home/jovyan; cp -rup /tmp/custom /home/jovyan/.jupyter; jupyter notebook --allow-root"
```

In your jupyterhub `config.yaml`
```yaml
singleuser:
  image:
    name: brospars/singleuser-scikit-learn-mooc
    tag: vX.X
```

## Build and publish

```shell
VERSION=$(git tag --sort=committerdate | tail -1)
docker build -t brospars/singleuser-scikit-learn-mooc:latest  -t brospars/singleuser-scikit-learn-mooc:$VERSION .
docker push brospars/singleuser-scikit-learn-mooc:latest
docker push brospars/singleuser-scikit-learn-mooc:$VERSION
```