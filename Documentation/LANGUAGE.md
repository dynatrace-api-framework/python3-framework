# Language


## Tenant, Cluster & Set
Tenant - Dynatrace Tenant (aka *Dynatrace Environment*)<br/>
Cluster - Dynatrace Cluster (SaaS can have all tenants under 1 "cluster")<br/>
Set - All defined Dynatrace Clusters in user variables<br/>

### Referencing Tenant, Cluster & Set
Tenant -> function (uv.FULL_SET['CLUSTER_NAME'], "Tenant")<br/>
Cluster -> function (uv.FULL_SET['CLUSTER_NAME])<br/>
Set -> function (uv.FULL_SET)<br/>


## Environment and App
Environment - Customer Environments/Lifecycles (e.g. Dev/Test/Perf/Acpt/Prod/DR)<br/>
App - Customer Applications (used with Tagging and MZ Rules)<br/>

## Python Descriptions
Dict - Python Dictionary (Note: API calls that use JSON payloads should pass in Dicts, and responses will be converted to Dicts)