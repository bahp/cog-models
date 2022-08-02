

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

For any further testing before using cog...

```
python query_models.py
```

Note that models are all stored in the models folder. For deployment, each
model is accompanied by a cog.yaml file to describe the environment set up 
process (e.g libraries, python version, and the predictor to use) and the
predict.py file with the BasePredictor which describes what model to load,
the input parameters and types and the output type.




### Deploy the models

First go to a model's folder (e.g. ./models/rfc/).

Now, build a Docker image for deployment:

```
$ cog build -t dengue-shock-rfc-model
--> Building Docker image...
--> Built dengue-shock-rfc-model

$ docker run -d -p 5000:5000 dengue-shock-rfc-model
```

To make a query go to http://localhost:5000/docs.

Otherwise you could use curl...

```
$ curl http://localhost:5000/predictions -X POST \
    -H 'Content-Type: application/json' \
    -d '{"input": {"sex": 1, "age": 12}}'

--> {"status":"succeeded","output":0.017614366149118245}% 
```

Save the image

```
$ docker save dengue-shock-rfc-model > dengue-shock-rfc-model.tar
```

Also, the image could be stored in a container repository, for instance
you could use the GitHub container registry and GitHub actions to publish 
the images if needed. For more information see 
https://blog.codecentric.de/en/2021/03/github-container-registry/

Notes:
  - Would it be possible to enable gpus with cog using --gpus all?