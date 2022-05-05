

### Install

First, install Docker.

Second, install cog with the following commands.

```
sudo curl -o /usr/local/bin/cog -L https://github.com/replicate/cog/releases/latest/download/cog_`uname -s`_`uname -m`
sudo chmod +x /usr/local/bin/cog
```

### Generate the models

To generate the models run the following script:

```
python create_models.py
```

For any further testing use...

```
python query_models.py
```

### Deploy the models


First go to a model's folder (e.g. models/rfc/).

Now, you can run predictions on this model:

```
$ cog predict -i sex=1 age=12
--> Building Docker image...
--> Running Prediction...
--> Output written to output.jpg
```

Or, build a Docker image for deployment:

```
$ cog build -t django-shock-rfc-model
--> Building Docker image...
--> Built my-colorization-model:latest

$ docker run -d -p 5000:5000 --gpus all my-colorization-model

$ curl http://localhost:5000/predictions -X POST \
    -H 'Content-Type: application/json' \
    -d '{"input": {"sex": 1, "age": 12}}'
```