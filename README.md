# k8s-begone
### By the end of the week this tool will be a kubectl plugin.

Assuming your application logic is sound, most of Kubernetes debugging is a process of triage until you've isolated the problem. Broadly speaking, there's two possible debugging modes  - you can be debugging the cluster, or a specific application (defined as an issue with a Pod, ReplicaSet, Deployment or Service).

Let's say your `pizza-delivery` pod is failing, and you're not sure why. Looking at the wonderful [Kubernetes docs](https://kubernetes.io/docs/tasks/debug/debug-application/debug-pods/#debugging-pods), we see step 1 is to diagnose the problem, and determine whether it is a problem with a pod, a ReplicationController, or a Service. 

That's three branches of a tree. Let's go down the first branch. The docs tell us to run `kubectl describe pods pizza-delivery` - and check to see the state of the containers in the pod. 

The server returns this command to the client - and the client execs the `kubectl` command. It pipes the output back to the server. Now we make a second query to our LLM - constructing our prompt with this additional context. 

Recurse until we've found the problem.


What would the ultimate k8s assistant look like?
- you give it a design doc, and it makes all the config files, sets up permissions stuff (?), understands which application and which service corresponds to which container image
- knows what limits to place on each container image through a reinforcement loop 


But this is boiling the ocean

Interpretability/latent saliency maps - https://arxiv.org/pdf/2210.13382.pdf


~~You'd have to specify a bunch of docker containers that you'd like a Kubernetes cluster, and a natural language description of what the nodes should look like, and it applies all the commands and generates all the configs necessary.~~

~~So this is a managed Kubernetes service. But not really. Because you're still very much running Kubernetes - think of this tool as an assistant.~~

