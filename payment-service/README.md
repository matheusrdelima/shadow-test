# Shadow Test (Traffic Mirroring) com Istio

Este repositório demonstra, de forma prática e didática, como funciona o **Shadow Test (Traffic Mirroring)** utilizando **Istio**, **Kubernetes** e uma aplicação simples em **Python (Flask)**.

O objetivo é entender o comportamento real do espelhamento de requisições, evitando confusões comuns entre mirror, load balancing e canary deployment.

---

## 📌 Objetivo

Simular um cenário real onde:

* **v1** é a versão produtiva da aplicação
* **v2** é uma nova versão em modo shadow
* o usuário **sempre recebe resposta da v1**
* a v2 recebe **uma cópia da requisição**
* a resposta da v2 **nunca é retornada ao cliente**

Esse padrão é amplamente utilizado para:

* validação de novas regras de negócio
* testes com tráfego real
* migração de monólitos
* validação de performance
* observabilidade em produção

---

## 🧠 Conceito importante

> Shadow test **não divide tráfego**.
> Shadow test **copia requisições**.

Fluxo real:

```
Request
   |
   v
Istio (Envoy)
   |
   ├── v1 → resposta real
   |
   └── v2 → shadow (somente observação)
```

---

## 📁 Estrutura do projeto

```
payment-service/
├── v1/
│   ├── app.py
│   └── Dockerfile
├── v2/
│   ├── app.py
│   └── Dockerfile
└── k8s/
    ├── deployment-v1.yaml
    ├── deployment-v2.yaml
    ├── service.yaml
    ├── destination-rule.yaml
    └── virtual-service.yaml
```

---

## ⚙️ Pré-requisitos

* Docker
* Kubernetes (Kind, Minikube ou EKS)
* Istio instalado
* kubectl configurado

---

## 🚀 Passo a passo

### 1️⃣ Clonar o repositório

```bash
git clone https://github.com/seu-usuario/payment-shadow-istio.git
cd payment-shadow-istio
```

---

### 2️⃣ Build das imagens

```bash
docker build -t payment:v1 ./v1
docker build -t payment:v2 ./v2
```

Se estiver usando **Kind**:

```bash
kind load docker-image payment:v1
kind load docker-image payment:v2
```

---

### 3️⃣ Habilitar sidecar injection

O Istio só funciona se o tráfego passar pelo proxy.

```bash
kubectl label namespace default istio-injection=enabled
```

Recrie os pods se necessário:

```bash
kubectl delete pod -l app=payment
```

---

### 4️⃣ Aplicar manifests

```bash
kubectl apply -f k8s/
```

---

## 🔎 Validação

### Verifique se os pods possuem sidecar

```bash
kubectl get pods
```

Saída esperada:

```
2/2 Running
```

Isso indica:

* aplicação
* istio-proxy

---

## 🧪 Testando a aplicação

### Criar pod de teste

```bash
kubectl run curl \
  -it --rm \
  --image=curlimages/curl \
  --restart=Never \
  -- sh
```

---

### Request normal (sem shadow)

```bash
curl -X POST http://payment/pay \
  -H "Content-Type: application/json" \
  -d '{"amount": 100}'
```

Resultado:

* v1 recebe request
* v2 NÃO recebe

---

### Request com shadow habilitado

```bash
curl -X POST http://payment/pay \
  -H "Content-Type: application/json" \
  -H "x-shadow: true" \
  -d '{"amount": 100}'
```

Resultado:

* v1 recebe request
* v2 recebe request (mirror)
* resposta ao cliente continua sendo da v1

---

## 📜 Logs

### v1

```bash
kubectl logs deploy/payment-v1 -f
```

### v2 (shadow)

```bash
kubectl logs deploy/payment-v2 -f
```

Você deverá observar:

```
➡️ V1 recebeu request
👀 V2 recebeu request (shadow)
```

---

## ✅ Boas práticas

* nunca usar mirror global em produção
* preferir mirror ativado por header
* evitar efeitos colaterais na versão shadow
* usar dry-run, feature flag ou mocks
* monitorar logs, métricas e traces separadamente


---

## ✨ Autor

Matheus R. de Lima
