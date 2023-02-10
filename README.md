# k8s-begone

A way to automate your Kubernetes deployments.

You'd have to specify a bunch of docker containers that you'd like a Kubernetes cluster, and a natural language description of what the nodes should look like, and it applies all the commands and generates all the configs necessary.

So this is a managed Kubernetes service lol. But not really. Because you're still very much running Kubernetes - think of this tool as an assistant. 

Problems I faced:
1. lots of evicted pods
2. failed readiness checks and it was unclear how to debug them and how to get started
3. should have been a way to pass in a Dockerfile and generate a corresponding kubernetes YAML
4. shouldn't have to learn the semantics of what it means to 


Possible next steps:
1. download the chat history of the kubernetes slack channel with user questions and expert answers, and use that to finetune gpt3 using openai api
2. https://github.com/ht2/gpt_content_indexing/
https://loft.sh/blog/kubernetes-monitoring-dashboards-5-best-open-source-tools/

