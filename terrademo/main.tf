terraform {
  required_providers {
    google = {
      source = "hashicorp/google"
      version = "7.16.0"
    }
  }
}

provider "google" {
    credentials = "./keys/creds.json"
    project     = "meta-imagery-484316-j9"
    region      = "europe-west4"
}

resource "google_storage_bucket" "demo-bucket" {
  name          = "meta-imagery-484316-j9"
  location      = "EU"
  force_destroy = true

  lifecycle_rule {
    condition {
      age = 1
    }
    action {
      type = "AbortIncompleteMultipartUpload"
    }
  }
}