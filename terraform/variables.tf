variable "project" {
  type    = "string"
  default = "personal-finance-228402"
}
variable "credentials" {
  type        = "string"
  description = "google service account key"
  default     = "/Users/xiaohan/workspace/credentials/gcp-infra.json"
}

variable "region" {
  type        = "string"
  description = "google region"
  default     = "asia-northeast1"
}
