{{/* vim: set filetype=mustache: */}}
{{/*
Expand the name of the chart.
*/}}
{{- define "portfolio-app.name" -}}
{{- .Chart.Name | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{/*
Create a default fully qualified app name, <release-name>-<chart-name>
This is also used to prefix all resources names within this deployment
We truncate at 63 chars because some Kubernetes name fields are limited to this (by the DNS naming spec).
*/}}
{{- define "portfolio-app.fullname" -}}
{{- printf "%s-%s" .Release.Name .Chart.Name | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "portfolio-app.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{/*
Common labels
*/}}
{{- define "portfolio-app.labels" -}}
helm.sh/chart: {{ include "portfolio-app.chart" . }}
{{ include "portfolio-app.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end -}}

{{/*
Selector labels
*/}}
{{- define "portfolio-app.selectorLabels" -}}
app.kubernetes.io/name: {{ include "portfolio-app.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end -}}

{{/*
Create the name of the service account to use
*/}}
{{- define "portfolio-app.serviceAccountName" -}}
{{- if .Values.serviceAccount.create -}}
{{ include "portfolio-app.fullname" . }}-{{ .Values.serviceAccount.name }}
{{- end -}}
{{- end -}}

{{/*
Generate pod security context to use (global takes precedence)
*/}}
{{- define "portfolio-app.podSecurityContext" -}}
{{- if .Values.podSecurityContext -}}
{{- toYaml .Values.podSecurityContext }}
{{- end }}
{{- end -}}

{{/*
Generate security context to use (global takes precedence)
*/}}
{{- define "portfolio-app.securityContext" -}}
{{- if .Values.securityContext -}}
{{- toYaml .Values.securityContext }}
{{- end }}
{{- end -}}


{{/*
Generate configMapRef data to be injected into deployment 
*/}}
{{- define "portfolio-app.portfolio-env" -}}
{{- $portfolioAppFullname := include "portfolio-app.fullname" . -}}
{{- range .Values.global.portfolio_env }}
- configMapRef:
    name: {{ $portfolioAppFullname }}-{{ .name }}
{{- end }}
{{- end -}}


{{/*
Generate secretRef data to be injected into deployment 
*/}}
{{- define "portfolio-app.portfolio-secret" -}}
{{- $portfolioAppFullname := include "portfolio-app.fullname" . -}}
{{- range .Values.global.portfolio_secret }}
- secretRef:
    name: {{ $portfolioAppFullname }}-{{ .name }}
{{- end }}
{{- end -}}


{{/*
Generate a list of volumes to be injected into deployment
*/}} 
{{- define "portfolio-app.volumes" -}}

{{- $portfolioAppFullname := include "portfolio-app.fullname" . -}}

{{- range .Values.global.portfolio_file }}
- name: {{ .name }}
  configMap:
    name: {{ $portfolioAppFullname }}-{{ .name }}
{{- end }}

{{- end -}}


{{/*
Generate a list of volumes mounts for the portfolio-app container
*/}}
{{- define "portfolio-app.volMounts" -}}

{{- range .Values.global.portfolio_file }}
- name: {{ .name }}
  mountPath: {{ tpl .mountPath $ }}
  subPath: {{ tpl .subPath $ }}
  readOnly: {{ .readOnly | default false }}
{{- end }}

{{- end -}}

{{/*
Generate livenessProbe data to be injected into deployment 
*/}}
{{- define "portfolio-app.liveness-probe" -}}
httpGet:
  path: "/"
{{- range .Values.service.ports }}
  port: {{ .port }}
{{- end }}
initialDelaySeconds: {{ .Values.initialDelaySeconds }}
{{- with .Values.livenessProbe }}
periodSeconds: {{ .periodSeconds }}
timeoutSeconds: {{ .timeoutSeconds }}
successThreshold: {{ .successThreshold }}
failureThreshold: {{ .failureThreshold }}
{{- end }}
{{- end -}}

{{/*
Generate readinessProbe data to be injected into deployment 
*/}}
{{- define "portfolio-app.readiness-probe" -}}
httpGet:
  path: "/"
{{- range .Values.service.ports }}
  port: {{ .port }}
{{- end }}
initialDelaySeconds: {{ .Values.initialDelaySeconds }}
{{- with .Values.readinessProbe }}
periodSeconds: {{ .periodSeconds }}
timeoutSeconds: {{ .timeoutSeconds }}
successThreshold: {{ .successThreshold }}
failureThreshold: {{ .failureThreshold }}
{{- end }}
{{- end -}}