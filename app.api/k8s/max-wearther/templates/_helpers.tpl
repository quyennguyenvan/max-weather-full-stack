{{/* Define common labels and name templates */}}
{{- define "application.fullname" -}}
{{ .Release.Name }}-{{ .Chart.Name }}
{{- end }}

{{- define "application.name" -}}
{{ .Chart.Name }}
{{- end }}

{{- define "application.namespace" -}}
{{ .Values.namespace | default .Release.Namespace }}
{{- end }}
