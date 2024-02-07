{{/* Create the prometheus label */}}

{{- define "prometheusLabel" -}}
prometheus: main
{{- end -}}

{{- define "prometheusNsLabel" -}}
monitoring: prometheus
{{- end -}}
