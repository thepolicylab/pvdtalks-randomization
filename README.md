# pvdtalks-randomization

A repo for code that we will use to assign families and groups to experimental conditions so that we can learn about the LENA technology and curriculum.

This is a webapp using the Flask framework.

To develop here, use a virtual environment. For example you can do:

```
python3 -m venv venv
```

or

```
source venv/bin/activate
```

To build and prototype do the following at the unix command line within this directory (edited in case you have different versions, etc)

```
docker-compose up -d
```

You should then be able to go to `http://localhost:5000` in your browser. The default user is `kevin_wilson@brown.edu` with a password of `asdf`. (Obviously this needs to be fixed for deploy.)

To shut down the app do `docker-compose down`.

To shut down the virtual environment do `deactivate`.
