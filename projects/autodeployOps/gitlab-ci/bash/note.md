#

## about some variables not defined in script 

those variables are defined in gitlab project as 'Secret Variables'

> about **Secret Variables** 
>
>you can find it in 'YOUR_PROJECT/Settings/CI/CD Pipelines'
>
>These variables will be set to environment by the runner.
>So you can use them for passwords, secret keys or whatever you want.
>The value of the variable can be visible in job log if explicitly asked to do so.
>

## about 'prod_deploy_host.conf', 'test_deploy_host.conf'
format: 
```text
<internal ip>:<ssh port>:<username>:<external ip>
```
'\<external ip>' can be omitted
