# Architecture

This document is the detailed companion to the summary in the root README. It contains
the full set of views a design authority expects: context, containers, components,
request lifecycle, approval sequence, deployment, data classification, and the audit chain.

## 1. System context

```mermaid
flowchart LR
    subgraph People
        ENG[Engineer]
        APP[Platform approver]
        SEC[Security approver]
        EXE[CIO / CISO / CFO]
    end
    subgraph Portal[Developer Self-Service Portal]
        UI[Portal web]
        API[Portal API]
    end
    subgraph Enterprise
        ENTRA[Entra ID / SSO]
        CMDB[(CMDB / service catalogue)]
        SIEM[(Central SIEM)]
        FINOPS[(Cost management export)]
        TEAMS[Teams / email relay]
    end
    subgraph Cloud[Landing zones]
        AZ[Azure]
        AWS[AWS]
        GCP[GCP]
    end
    ENG --> UI
    APP --> UI
    SEC --> UI
    EXE --> UI
    UI --> API
    ENTRA --> UI
    API --> CMDB
    API --> SIEM
    API --> TEAMS
    API --> AZ
    API --> AWS
    API --> GCP
    FINOPS --> API
```

## 2. Containers

```mermaid
flowchart TB
    subgraph Edge
        WAF[Web application firewall]
        GW[API gateway with mTLS]
    end
    subgraph Runtime[AKS, private cluster]
        WEB[portal-web]
        API2[portal-api]
        WRK[portal-worker]
        NTF[portal-notifier]
    end
    subgraph Data
        PG[(Postgres: requests)]
        AUD[(Postgres: audit, append-only)]
        BUS[(Service Bus: provisioning)]
        KV[(Key Vault)]
    end
    WAF --> GW --> WEB
    GW --> API2
    API2 --> PG
    API2 --> AUD
    API2 --> BUS
    BUS --> WRK
    WRK --> PG
    WRK --> AUD
    API2 --> NTF
    API2 -. secrets .-> KV
    WRK -. secrets .-> KV
```

## 3. Components inside the API

```mermaid
flowchart LR
    R1[routes/requests.py] --> POL[core/policy.py]
    R1 --> CAT[core/catalog.py]
    R1 --> AUD[core/audit.py]
    R1 --> STO[core/store.py]
    R1 --> NTF[notifier/notify.py]
    R1 --> PRV[worker/provisioner.py]
    PRV --> ADP{adapter}
    ADP --> DRY[worker/adapters/dry_run.py]
    ADP --> TF[worker/adapters/terraform.py]
    R2[routes/catalog.py] --> CAT
    R3[routes/audit.py] --> AUD
```

## 4. Request state machine

```mermaid
stateDiagram-v2
    [*] --> Submitted
    Submitted --> Rejected: policy violation (G-02, G-03, catalog)
    Submitted --> PendingApproval: prod or approval-required (G-01)
    Submitted --> Approved: auto-approved template
    PendingApproval --> Approved: independent approver accepts (G-06)
    PendingApproval --> Rejected: approver declines
    Approved --> Provisioning: only via gate (G-05)
    Provisioning --> Ready
    Provisioning --> Failed
    Ready --> Expired: TTL reached (lifecycle)
    Expired --> [*]
    Ready --> [*]
    Rejected --> [*]
    Failed --> [*]
```

## 5. Approval sequence with segregation of duties

```mermaid
sequenceDiagram
    autonumber
    participant E as Engineer
    participant API as Portal API
    participant POL as Policy
    participant A as Approver
    participant AUD as Audit chain
    participant W as Worker

    E->>API: POST /requests (payments-prod, prod)
    API->>POL: evaluate
    POL-->>API: allowed, needs_approval
    API->>AUD: request.submitted
    API-->>E: 201 pending_approval
    E->>API: POST /requests/{id}/approve (self)
    API->>POL: can_approve(E, E)
    POL-->>API: denied (G-06)
    API->>AUD: request.approval_denied
    API-->>E: 403
    A->>API: POST /requests/{id}/approve
    API->>POL: can_approve(A, E)
    POL-->>API: allowed
    API->>AUD: request.approved
    API->>W: plan (gate G-05)
    W-->>API: ready
    API->>AUD: request.ready
```

## 6. Deployment topology

```mermaid
flowchart TB
    subgraph Connectivity[Connectivity subscription]
        HUB[Hub VNet + Azure Firewall]
        DNS[Private DNS]
    end
    subgraph Platform[Platform subscription]
        AKS[AKS private cluster]
        PG[(Postgres flexible, zone-redundant)]
        SB[(Service Bus Premium)]
        KV[(Key Vault, HSM-backed)]
        LA[(Log Analytics to SIEM)]
    end
    subgraph Landing[Landing zones, one per business unit]
        SBX[Sandbox subscription]
        STG[Staging subscription]
        PRD[Production subscription]
    end
    HUB --- AKS
    AKS --> PG
    AKS --> SB
    AKS --> KV
    AKS --> LA
    SB --> SBX
    SB --> STG
    SB --> PRD
```

## 7. Data classification

```mermaid
quadrantChart
    title Data handled by the portal
    x-axis Low sensitivity --> High sensitivity
    y-axis Low volume --> High volume
    quadrant-1 Monitor closely
    quadrant-2 Protect and retain
    quadrant-3 Keep minimal
    quadrant-4 Automate
    Request metadata: [0.25, 0.8]
    Cost estimates: [0.45, 0.55]
    Approver identity: [0.6, 0.4]
    Justification text: [0.5, 0.2]
    Provisioned resource IDs: [0.7, 0.7]
    Credentials: [0.95, 0.1]
```

Credentials never pass through the portal. Workers use managed identities from the landing-zone runner.

## 8. Audit chain

```mermaid
flowchart LR
    G[genesis 000...] --> E1[seq 1<br/>request.submitted<br/>hash H1]
    E1 -->|prev_hash = H1| E2[seq 2<br/>request.provisioning<br/>hash H2]
    E2 -->|prev_hash = H2| E3[seq 3<br/>request.approved<br/>hash H3]
    E3 -->|prev_hash = H3| E4[seq 4<br/>request.ready<br/>hash H4]
```

Each hash covers the entry body and the previous hash. Editing or deleting any entry breaks
every hash after it, which `GET /audit/verify` reports as `first_broken_seq`.

## 9. Failure and recovery

```mermaid
flowchart TD
    START([Provisioning requested]) --> APPLY{Adapter result}
    APPLY -->|ok| READY[status = ready]
    APPLY -->|error| FAILED[status = failed, error recorded]
    FAILED --> RETRY{Retry allowed?}
    RETRY -->|transient| APPLY
    RETRY -->|no| ALERT[Page platform on-call]
    ALERT --> RUNBOOK[docs/runbooks/provisioning-failure.md]
```

## Design decisions

See `docs/adr/` for the reasoning behind policy-as-code (0001), the first-build synchronous
adapter (0002), hash-chained audit (0003), and the mandatory approver separation (0004).
