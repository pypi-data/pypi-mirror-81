
## Building the Docker image
```
docker build . -t betelgeuse:latest
```

## Running the Docker image

```
docker run -it betelgeuse *args
```

Spawn a docker container on host and run brakeman_analyzer
```
docker run -it betelgeuse -t master -r {remote access id} -w True -a {authorization code}
```

where 
-t: is the branch name.
-w: wait for the status.
-e: (optional , default: True) exits if the build return is false.
-a: authorization code.
-r: remote access id for the api.
-v: (optional, default: error) logging. 

## Running Locally

```
python3 setup.py install
```

```
betelgeuse --Host <Enterprise_Strobes_API_URL> -a authorization_token -r remote_access_id -w True -t <branch_name>|<URL>|<container_image_name>
```
