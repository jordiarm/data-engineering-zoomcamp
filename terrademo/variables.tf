variable "project" {
  description = "My project name"
  default     = "meta-imagery-484316-j9"
}

variable "region" {
  description = "Project Region"
  default     = "europe-west4"
}

variable "location" {
  description = "Project Location"
  default     = "EU"
}

variable "bcs_bucket_name" {
  description = "My Storage Bucket Name"
  default     = "meta-imagery-484316-j9"
}

variable "bq_dataset_name" {
  description = "My BigQuery Dataset Name"
  default     = "example_dataset"
}

variable "delete_contents_on_destroy" {
  default = true
}

variable "credentials" {
    description = "My credentials"
    default = "./keys/creds.json"
}