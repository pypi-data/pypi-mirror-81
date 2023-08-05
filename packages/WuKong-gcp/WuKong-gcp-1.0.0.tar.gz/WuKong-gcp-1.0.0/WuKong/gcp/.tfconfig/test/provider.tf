locals {
  gcp_svc_key = "./keys/svc-key.json"
}

provider google {
  version     = ">= 3.23.0, <4.0.0, != 3.29.0"
  credentials = file(local.gcp_svc_key)
  project     = var.project
  region      = var.region
}

provider google-beta {
  version     = ">= 3.23.0, <4.0.0, != 3.29.0"
  credentials = file(local.gcp_svc_key)
  project     = var.project
  region      = var.region
}