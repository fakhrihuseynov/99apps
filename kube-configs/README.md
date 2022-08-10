# USER-SERVICE RUNNING ON MINIKUBE CLUSTER

### Instruction

<!-- Please write down how to use the configurations to make the app up and running on minikube in this section! -->

For the up and running of the app on the ./user-service folder, we need to containerize the **app.py** file on a dedicated Docker file which will be created on the root folder of the project as **Dockerfile** and then we need to push the Dockerfile to any remote repository for the future pulling the image and run it on minikube cluster

### Steps for containerize 
1) Create a Docker file on the root folder
2) Get a solution from the python library
3) Create a separate working directory for the application file and copy all files to a dedicated folder
4) Install only required dependencies from the ***requirements.txt*** file

Build and test your docker image
1) To the build a docker image you can use the commands below

`docker build -t <your_image_name>:<your_tag> . `

2) Also you can test a dockerfile creating a local container on your local docker engine for example:

`docker run -d -p 9000:8001 <your_image_name>:<your_tag>`

3) For pushing the image, I have used my own remote repository and tagged my image using
- `docker tag service-app faxri/99app:service-app`and pushing the image as:
- `docker push faxri/99app:service-app`
This image will be used on the template for the minikube cluster deployment
### Steps for creating a cluster on minikube 
1) Installed minikube onto VirtualBox using

`minikube start --driver=virtualbox` 

if you need to ignore check system virtualization check for your machine you can use

`minikube start --driver=virtualbox --no-vtx-check`

2) After installing minikube you can create your cluster in several  ways (in my case I have used a default creation)

`minikube start`

Or you can specify exact resource parameters for your nodes by multiplying as

`minikube start --cpus=2 --memory=3gb --disk-size=20gb --nodes=3`

3) You can also install kubectl tool for using kubernetes commands
4) After you can check the status of your running node (nodes)

`kubectl get nodes`

Output example:

``` 
NAME       STATUS   ROLES                  AGE   VERSION
minikube   Ready    control-plane,master   14h   v1.23.3

```
### Steps for containerizing the solution
We need to run app service on previously created minikube cluster using kind for a deployment configuration file with YAML extension for the Kubernetes and expose load-balancer for the pods with 3 replicas
1) Create a YAML file with Deployment kind with the name ***app-deploy.yaml***
2) Specify the spec configuration with labels and project metadata name on it and deployment name with ***my99app***
3) Specify the spec for the containers using a previously pushed image to the remote repository, in our case, it should be ***faxri/99app:service-app***
4) Add additional spec for load balance service with name ***appservice*** and target port for ***8001*** for exposing default application port wich is existing on ***app.py*** solution
5) Deploy a template file using

`kubectl apply -f .\kube-configs\app-deploy.yaml`

6) Check if deployment was successfully created

`kubectl get deployment my99app`

Output example:

``` 
NAME      READY   UP-TO-DATE   AVAILABLE   AGE
my99app   3/3     3            3           48m

```

7) Check if the service is also created

`kubectl get service appservice`

Output example:

``` 
NAME         TYPE           CLUSTER-IP      EXTERNAL-IP   PORT(S)        AGE
appservice   LoadBalancer   10.106.251.83   <pending>     80:31103/TCP   50m

```

### Check running app on minikube
In my case minikube running locally and not exposing any ***external-ip*** it will delay on pending status

8) For checking minikube exposing inbound service for the running solution we need to get a minikube created IP address and listening load balance port using

 `minikube service --url appservice`

Output example:

```http://192.168.59.100:31103```

Now we can use curl to get API responses like:
```curl.exe -XGET "192.168.59.100:31103/v1/users"```

Also we can create a new user using
```curl -XPOST "192.168.59.100:31103/v1/users" -F name="Admin" -F email="admin@gmail.com"```

Output example:
```
{"user_id": "uunr1xvz04"}
```
