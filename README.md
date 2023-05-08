# fraud
Basic Fraud Detection Demo

```
.
├── application                            Inference Application
│   ├── Dockerfile
│   ├── model_application.py
│   └── requirements.txt
├── data                                   Training data
│   └── card_transdata.csv
└── model                    
    ├── 01-model-training-fusion.ipynb     Notebook to train and save the model.
    └── 03-s3-testing.ipynb
```

### RHODS notes

### Data science workbench values

These values are needed by the Jupyter Notebook.

| Workbench          |                        |
|--------------------|------------------------|
| Image Selection    | Standard Data Science  |
| Version Selection  | py3.9-v2               |
| Deployment Size    | Small                  |
| FUSION_ACCESS_KEY  | <access_key>           |
| FUSION_SECRET_KEY  | <secret_key>           |
| FUSION_S3_ENDPOINT | <endpoint_url>         |
| FUSION_VAULT       | <vault or bucket name> |

### Data Connection

These values are used by the model server.

| Environment variables |                               |
|-----------------------|-------------------------------|
| AWS_ACCESS_KEY_ID     | <access_key>                  |
| AWS_SECRET_ACCESS_KEY | <secret_key>                  |
| AWS_S3_ENDPOINT       | <endpoint_url>                |
| AWS_S3_BUCKET         | <vault or bucket name>        |
| Connected Workbench   | <The workbench created above> |

### Create a small model server with 1 replica with no external route.

### Deploy a model.

| Deploy Model      |                  |
|-------------------|------------------|
| Name              | fraud            |
| Model framework   | onnx-1           |
| Data Connection   | <from_above>     |
| Folder path       | fraud.onnx       |

After the model deploy's and you see a green checkmark, click on **Internal Service** and copy 
the restUrl (i.e. `http://modelmesh-serving.bk-fraud-trng:8008`)
and create the `REST_URL` variable.

`REST_URL=http://modelmesh-serving.bk-fraud-trng:8008`

From within Jupyter Lab, change to the `model` directory and run the
`01-model-training-fusion.ipynb` notebook. It should train the model
and upload the `fraud.onnx` model artifact to S3 storage so the model server can find it.

### Login to Openshift and Deploy the inference application.

Construct the `INFERENCE_ENDPOINT` variable using the `REST_URL`
and the deployed model name from above.

`INFERENCE_ENDPOINT=${REST_URL}/v2/models/fraud/infer`

Create a new openshift project.
`oc new-project fraud-infer`

Create a new Openshift application.
`oc new-app https://github.com/bkoz/fraud.git --context-dir=/application --env=INFERENCE_ENDPOINT=${INFERENCE_ENDPOINT}`

Visit the application route. When the [gradio](https://gradio.app/) application appears click on a sample request from the bottom of the page and make a
prediction.
