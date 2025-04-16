**This is instruction to deployment the Hashcorp vault**

**architecture of vault with hashicorpvault**
![alt text](/report-resources/vault-architecture.png)


**prerequirements:**

1. Have the Kubernetes cluster (Azure Kubernetes or AWS Kubernetes or Google Kubernetes)
2. Helm

**step by step:**

--> for the EKS cluster

1. Enable the IAM OIDC provider for EKS
   
   ```eksctl utils associate-iam-oidc-provider --cluster <your-cluster-name> --approve```

2. Install the Vault on EKS(via helm) - not-recommend ( for test purporse)
  
   ```
    helm repo add hashicorp https://helm.releases.hashicorp.com
    helm repo update
    helm install vault hashicorp/vault \
    --set "server.dev.enabled=true" \
    --namespace vault --create-namespace
   ```
    note: replace the ```server.dev.enabled=true``` with full production config if needed.

3. Enabled the Kubernetes Auth in Vault (vault side)
   
    example of: access to the pod vault ( kubectl exec -it /vaultpod /bin/bash)

    (3*)vault enable: ``` vault auth enable kubernetes```

    **if you install the vault server at local**
    follow bellow steps:
    ```
    wget -O- https://apt.releases.hashicorp.com/gpg | sudo gpg --dearmor -o /usr/share/keyrings/hashicorp-archive-keyring.gpg
            echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hashicorp.list
            sudo apt update && sudo apt install vault
    ```

    3.1 Export vault: ```export VAULT_ADDR='http://localhost:8200'```

    3.2 Login: ```vault login root```

    3.3 Follow the (3*) step
    
4. Configuration the Kubernetes Auth in Vault
   1. Get the kubernetes sa (service account) jwt token and ca cert:
    ```
    kubectl exec -n vault vault-0 -- cat /var/run/secrets/kubernetes.io/serviceaccount/token
    kubectl exec -n vault vault-0 -- cat /var/run/secrets/kubernetes.io/serviceaccount/ca.crt

    ```
    2. In Vault run (get output from step 1):
    ```
    vault write auth/kubernetes/config \
        token_reviewer_jwt="<copied-token>" \
        kubernetes_host="https://<K8s-API-Server>" \
        kubernetes_ca_cert="<copied-ca>"

    ```
    3. Create vault role for application ( namespace of application)
    ```
    vault write auth/kubernetes/role/my-app \
    bound_service_account_names=my-app-sa \
    bound_service_account_namespaces=default \
    policies=my-app-policy \
    ttl=1h
    ```
    4. Create the Vault policy
    ```
    # my-app-policy.hcl
    path "secret/data/my-app/*" {
    capabilities = ["read"]
    }
    ```
    5. Apply the change
    ```
    vault policy write my-app-policy my-app-policy.hcl
    ```
5. Install the vault agent injector
   ```
   helm upgrade --install vault hashicorp/vault \
    --set "injector.enabled=true" \
    --set "server.enabled=false" \
    --namespace vault
    ```
6. Create the simple the vault data
   ```
   vault kv put secret/my-app/config username="admin" password="s3cr3t"

   ```
7. Run the manifest to view the result


**Summary**
1. The candidate can understand  the simple of secret how it storage with 3rd tool.
2. Aware about security and risk.
3. Practices with kubernetes services account

**document**
1. https://developer.hashicorp.com/vault/docs/platform/k8s/injector/annotations
2. https://developer.hashicorp.com/vault/docs/platform/k8s/injector