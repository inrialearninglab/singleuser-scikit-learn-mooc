# Jupyterhub singleuser image for the scikit-learn mooc

## Usage

Test locally 

```shell
# As normal user
docker build -t brospars/singleuser-scikit-learn-mooc:latest .
docker run -p 8888:8888 brospars/singleuser-scikit-learn-mooc:latest

# As root
docker build -t brospars/singleuser-scikit-learn-mooc:root .
docker run -p 8888:8888 brospars/singleuser-scikit-learn-mooc:root /bin/bash -c "jupyter notebook --allow-root"
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
docker build -t brospars/singleuser-scikit-learn-mooc:latest  -t brospars/singleuser-scikit-learn-mooc:vX.X .
docker push brospars/singleuser-scikit-learn-mooc:latest
docker push brospars/singleuser-scikit-learn-mooc:vX.X
```