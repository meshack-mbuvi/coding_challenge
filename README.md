# Coding Challenge App

This is an application that is used to get a profile of a user, organization or
team.
The

## Install:

```
pip install -r requirements.txt
```

## Running the code

### Spin up the service

```
# start up local server
python -m run
```

### Making Requests

```
curl -i "http://127.0.0.1:5000/api/v1/profile?username={username}"
```

The above endpoint requires a parameter named username which takes the name of
the user, organization or team one wants to view profile.

The response returned by the above endpoint is in the format below:

```
{
  "followers": 14,
  "forked repositories": 6,
  "languages used": [
    "Python",
    "JavaScript",
    "C++",
    "C",
    "HTML",
    "python",
    "TypeScript",
    "Java"
  ],
  "original repositories": 32,
  "total": 32
}
```

### Running tests

`nosetests`
