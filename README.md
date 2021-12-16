# Jupyterhub singleuser image for the scikit-learn mooc

## Usage

In your jupyterhub `config.yaml`
```yaml
singleuser:
  image:
    name: brospars/singleuser-scikit-learn-mooc
    tag: latest
```

## Build and publish

```shell
docker build -t brospars/singleuser-scikit-learn-mooc:latest  -t brospars/singleuser-scikit-learn-mooc:vX.X .
docker push brospars/singleuser-scikit-learn-mooc:latest
docker push brospars/singleuser-scikit-learn-mooc:vX.X
```