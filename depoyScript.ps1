###################################################################################
# Steps for containerize

Param(
    [Parameter(Mandatory, HelpMessage = "Create your docker image")]
    [String]$imageName,
    [Parameter(Mandatory, HelpMessage = "Create your docker image")]
    [String]$tag
)
$givedImage = -join ($imageName, ":", $tag)
$myImage = "faxri/99app:service-app"

Write-Host -ForegroundColor Green "Creating your docker-image"
docker build -t $givedImage .
Write-Host -ForegroundColor Yellow "Do you want to test your image on 9000 port? (Type Yes or No)"

Function testImage(

    [Parameter(Mandatory, HelpMessage = "Create your docker image")]
    [string]$yourAnswer

) {
    if ($yourAnswer -eq 'Yes') {
        docker run -d -p 9000:8001 $givedImage
    }
    else {
        Write-Host -ForegroundColor Yellow "Continue creating tags for pushing an image....."
    }
}
testImage
Write-Host -ForegroundColor Yellow "Adding tags to newly created images"
docker tag $givedImage $myImage
docker images
Write-Host -ForegroundColor Yellow "Please login to dockerhub......................"
docker login
Write-Host -ForegroundColor Yellow "Now pushing image to dockerhub................."
docker push $myImage

###################################################################################
# Steps for creating a cluster on minikube

Write-Host -ForegroundColor Yellow "Now creating a minikube cluster................"

minikube start --driver=virtualbox --no-vtx-check

Write-Host -ForegroundColor Yellow "Checking your runing node......................"
kubectl get nodes

Write-Host -ForegroundColor Yellow "Create deployment for 99appp..................."
kubectl apply -f .\kube-configs\app-deploy.yaml

Write-Host -ForegroundColor Yellow "Get your deployment status....................."
kubectl get deployment my99app

Write-Host -ForegroundColor Yellow "Get your runing service status.................."
kubectl get service appservice

Write-Host -ForegroundColor Yellow "Get your minikube service URL..................."
minikube service --url appservice

# Now we can use curl to get API responses like: 
# curl.exe -XGET "192.168.59.100:31103/v1/users"
# Also we can create a new user using 
# curl.exe -XPOST "192.168.59.100:31103/v1/users" -F name="Admin" -F email="admin@gmail.com"




