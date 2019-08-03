variable "project" {
  type    = "string"
  default = ""
}
variable "credentials" {
  type        = "string"
  description = "google service account key"
  default     = ""
}

variable "region" {
  type        = "string"
  description = "google region"
  default     = "asia-northeast1"
}

variable "bucket_name" {
  type = "string"
  description = "storage bucket for public chart website"
  default = ""
}

variable "storage_class" {
  type = "string"
  description = "storage class"
  default = "REGIONAL"
}

variable "location" {
  type = "string"
  description = "storage location"
  default = "asia-northeast1"
}

variable "timezone" {
  type        = "string"
  description = "time zone used for the schedule"
  default     = "Asia/Tokyo"
}

variable "chart_updater_schedule" {
  type        = "string"
  description = "cron schedule for chart updater"
  default     = "0 */12 * * 1-5"
}

variable "chart_updater_url" {
  type        = "string"
  description = "cloud run http url for chart updater"
  default     = ""
}

