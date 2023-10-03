In order to view metrics on the dashboards, you need to create some usage. Ideally you will use Weaviate as you would normally use it in this step. As a very minimal example, we can import two objects using the /v1/batch API:

``` Bash
curl localhost:8080/v1/batch/objects -H 'content-type:application/json' -d '{"objects":[
  {"class": "Example", "vector": [0.1, 0.3], "properties":{"text": "This is the first object"}},
  {"class": "Example", "vector": [0.01, 0.7], "properties":{"text": "This is another object"}}
]}'
```

### Open Grafana in the browser
* Open your Browser at `localhost:3000`
* Log into the Grafana instance using weaviate/weaviate. 
* Select one of the sample dashboards, such as "Importing Data Into Weaviate".