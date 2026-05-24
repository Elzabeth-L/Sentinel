{{- define "aks-governance.name" -}}
aks-governance
{{- end -}}

{{- define "aks-governance.labels" -}}
app.kubernetes.io/name: {{ include "aks-governance.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
app.kubernetes.io/version: {{ .Chart.AppVersion }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end -}}

