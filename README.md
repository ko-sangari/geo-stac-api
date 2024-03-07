# 🤖 Geo STAC API
[![forthebadge made-with-python](https://forthebadge.com/images/badges/made-with-python.svg)](https://www.python.org/)
[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/release/python-390/) [![Docker](https://badgen.net/badge/icon/docker?icon=docker&label)](https://https://docker.com/) [![Open Source? Yes!](https://badgen.net/badge/Open%20Source%20%3F/Yes%21/blue?icon=github)](https://github.com/Naereen/badges/)


## ⭕ Contents
- [The project's purpose](#-the-project's-purpose)
- [What tools were used to create this project](#-what-tools-were-used-to-create-this-project)
- [Before you begin](#-before-you-begin)
- [how to run the project](#-how-to-run-the-project)
- [how to run tests](#-how-to-run-tests)
- [Final step](#-final-step)


## ⭕ The project's purpose
The objective of this project is to develop an API application capable of handling geospatial data, specifically dealing with satellite imagery and field boundaries. The core functionality revolves around processing polygonal input, represented in GeoJSON format, to facilitate the retrieval and storage of satellite imagery.

Key functionalities include:

**1. Satellite Image Retrieval**: The API will offer an endpoint where users can submit a polygon in GeoJSON format. In response, the API retrieves the latest `Sentinel-2` satellite image for the specified area. If the image is not already present in the local database, the application will fetch it from an external API and store it for future use.

**2. Field Boundary Storage**: Another endpoint will allow users to upload the boundaries of a particular field, again using GeoJSON format. This data, including the field's boundary and geometry, is stored in the database, aiding in geospatial analyses and record-keeping.

**3. Intersection Querying**: Users can query for fields that intersect with a given polygon. This functionality is particularly useful in scenarios where understanding the overlap or intersection between different geospatial entities is critical, such as in land use planning or environmental monitoring.

Key Details:

- Polygons must be in GeoJSON format. (You can easily generate GeoJSON using `geojson.io`, or check the `geojson.sample` file in the root directory.)

- Documentation for satellite image retrieval is available in the `pystac-client` library documentation.


## ⭕ What tools were used to create this project
| Technology         |    🔗             |
| -----------------  | ----------------- |
| fastapi            | [[Github Link](https://github.com/tiangolo/fastapi)] |
| uvicorn            | [[Github Link](https://github.com/encode/uvicorn)] |
| pydantic           | [[Github Link](https://github.com/pydantic/pydantic)] |
| pydantic-settings  | [[Github Link](https://github.com/pydantic/pydantic-settings)]  |
| asyncio            | [[Github Link](https://github.com/python/cpython/blob/main/Doc/library/asyncio.rst) ] |
| httpx              | [[Github Link](https://github.com/encode/httpx/)] |
| sqlalchemy         | [[Github Link](https://github.com/sqlalchemy/sqlalchemy)] |
| asyncpg            | [[Github Link](https://github.com/MagicStack/asyncpg)] |
| geoalchemy2        | [[Github Link](https://github.com/geoalchemy/geoalchemy2)] |
| pystac-client      | [[Github Link](https://github.com/stac-utils/pystac-client)] |
| planetary-computer | [[Documents](https://planetarycomputer.microsoft.com/docs/quickstarts/reading-stac/)] |
| poetry             | [[Github Link](https://github.com/python-poetry/poetry)] |
| docker             | [[Github Link](https://github.com/docker-library/python)] |
| docker-compose     | [[Github Link](https://github.com/docker/compose)] |
| pytest             | [[Github Link](https://github.com/pytest-dev/pytest)] |
| pytest-asyncio     | [[Github Link](https://github.com/pytest-dev/pytest-asyncio)] |
| coverage           | [[Github Link](https://github.com/nedbat/coveragepy?tab=readme-ov-file)] |
| mypy               | [[Github Link](https://github.com/python/mypy)] |


## ⭕ Before you begin
Before you begin, please follow these steps:

1. Create a folder named `secret` in the `root` directory.
2. Move the `.env.template` file which is in the root directory into the each `secret` folder.
3. Rename the `.env.template` file to `.env`.
4. Update the variables in the `.env` file according to your local environment.

Additionally, make sure you have another `.env` file named `.env.docker`, which should contain Docker-related variables. (Check the `.env.template` file for more details.)


## ⭕ How to Run the Project
Navigate to the root of the project. <br>
To build the image from the Dockerfile, run:
```commandline
docker compose up --build -d
```

<br>Or, there's a `Makefile` for your convenience, so just run: (Check other commands too!)
```commandline
make run
```

<br>Or, If you want to run the project locally, you need to have `poetry` installed first.
```commandline
pip install poetry
poetry install
poetry run uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
```

<br>Now, you can check the **Swagger** URL for API documentation.
```commandline
http://localhost:8000/
```


## ⭕ How to run tests
Run _pytest_ command to run the tests separately.<br>
```commandline
make tests
```

<br>And, what about Test Coverage?
```commandline
make coverage

# Backend Directory               Stmts   Miss  Cover
# -----------------------------------------------------
# Test Coverage TOTAL              413     25    94%
```

<br>🌟 This project has been thoroughly checked with `mypy` for type consistency, and it currently passes all mypy checks without any issues.
```commandline
make mypy
```

## ⭕ Final step
```commandline
make coffee
```
#### Be Happy Even if Things Aren’t Perfect Now. 🎉🎉🎉
#### Enjoy your coffee! ☕

![](https://i1.wp.com/justmaths.co.uk/wp-content/uploads/2016/10/celebration-gif.gif)
