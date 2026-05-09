# Lab 1 — Agentic infrastructure (agentgateway + kagent)

Submission notes and artifacts. Add screenshots under [`screenshots/`](screenshots/) (see [`screenshots/README.md`](screenshots/README.md)).

## Objectives (per course wording)

- **Beginners:** local **agentgateway**, LLM provider, `config.yaml`, UI, LLM check, Backends and Policy.
- **Experienced (this repo):** Helm **agentgateway** on Kubernetes, **Secret** / **ConfigMap**, **kagent**, LLM via gateway (`curl`), agent verified in UI (Kubernetes tools).

## Versions used (update when you submit)

| Component | Version |
|-----------|---------|
| agentgateway (Helm chart) | `1.1.0` |
| kagent CLI / chart | `0.9.2` |
| Kubernetes context | `sandbox-apps` (example) |
| Namespace | `sandbox-kostiuchenko` |

## Files in this repo

| File | Purpose |
|------|---------|
| `config.yaml` | Local standalone agentgateway (no secrets; key via `export OPENAI_API_KEY`) |
| `config-k8s.yaml` | `Gateway` (Gateway API) for agentgateway data plane |
| `k8s-openai-backend.yaml` | `AgentgatewayBackend` → OpenAI |
| `k8s-openai-httproute.yaml` | `HTTPRoute` for `/v1/chat/completions` |
| `k8s-lab-configmap.yaml` | ConfigMap with non-secret lab metadata |
| `k8s-kagent-modelconfig-via-agentgateway.yaml` | Optional: `ModelConfig` for LLM via internal `agentgateway-proxy` |
| `LAB01-experienced-setup-commands.md` | Bring-up runbook (sandbox, PVC, tolerations) |
| `LAB01-teardown-sandbox-kostiuchenko.md` | Teardown runbook |

## Evidence (text)

### LLM via agentgateway in the cluster

HTTP check through the gateway (model must match `k8s-openai-backend.yaml`):

```bash
curl -sS --max-time 60 "http://<GATEWAY-ADDRESS>/v1/chat/completions" \
  -H "Content-Type: application/json" \
  -d '{"model":"gpt-4.1-nano","messages":[{"role":"user","content":"Hello!"}]}'
```

`<GATEWAY-ADDRESS>` — DNS from `kubectl get gateway agentgateway-proxy -n sandbox-kostiuchenko` (**ADDRESS** column), or `localhost:8080` with `kubectl port-forward deploy/agentgateway-proxy 8080:80`.

Expected: JSON with `choices[0].message.content` and `usage`.

### kagent

- Install: `kagent install --profile demo -n sandbox-kostiuchenko` (troubleshooting in `LAB01-experienced-setup-commands.md`).
- Verify: UI (`kagent dashboard`) or chat; example: list pods in `sandbox-kostiuchenko` using `k8s_get_resources` / `k8s_get_available_api_resources`.

## Environment notes (shared EKS sandbox)

You may need:

- explicit **StorageClass** for kagent Postgres PVC (e.g. `ebs-generic`);
- **tolerations** for node taints (e.g. `ajax.systems/workloads`);
- lower **CPU requests** for bundled Postgres when you see `Insufficient cpu`.

Documented in `LAB01-experienced-setup-commands.md`.

## Screenshots

Place under `screenshots/` (see [`screenshots/README.md`](screenshots/README.md)), for example:

1. agentgateway UI or route proof (if you used UI).
2. Successful `curl` / response snippet (no keys).
3. kagent: agent list or chat with a successful tool call.

## References

- [agentgateway](https://agentgateway.dev/)
- [kagent quickstart](https://kagent.dev/docs/kagent/getting-started/quickstart)
- [LLM gateway tutorial (standalone)](https://agentgateway.dev/docs/standalone/latest/tutorials/llm-gateway/)
- [Helm install (Kubernetes)](https://agentgateway.dev/docs/kubernetes/latest/install/helm/)
