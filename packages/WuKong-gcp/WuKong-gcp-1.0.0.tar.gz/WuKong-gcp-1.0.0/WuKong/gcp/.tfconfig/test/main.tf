variable resource_prefix {
  description = "A prefix mark for all infra resources created in GCP"
  default     = "sdeploy"
}

locals {
  ssh_private_key = "./keys/id_rsa"
  ssh_public_key  = "./keys/id_rsa.pub"
}

module network {
  source          = "./network"
  resource_prefix = var.resource_prefix
  region          = var.region
}

module cluster {
  source          = "./cluster"
  resource_prefix = var.resource_prefix
  region          = var.region
  k8s_version     = var.k8s_version
  vnet_link       = module.network.link
  subnet_link     = module.network.subnet_link_0
}

module database {
  source                 = "./database"
  resource_prefix        = var.resource_prefix
  database_user_name     = "gcpdefault"
  database_user_password = var.database_password
  vnet_link              = module.network.link
  db_version             = "POSTGRES_${var.pg_version}"
}

module nfs {
  source               = "./nfs"
  resource_prefix      = var.resource_prefix
  filestore_share_name = var.filestore_share_name
  project              = var.project
  region               = var.region
  vnet_name            = module.network.name
}

module bastion {
  source               = "./bastion"
  resource_prefix      = var.resource_prefix
  project              = var.project
  region               = var.region
  ssh_public_key_file  = file(local.ssh_public_key)
  ssh_private_key_file = file(local.ssh_private_key)
  vnet_link            = module.network.link
  subnet_link          = module.network.subnet_link_0
  vm_user              = var.vm_user
  k8s_cluster_name     = module.cluster.name
}

module dns {
  source          = "./dns"
  fqdn            = var.fqdn
  project         = var.project
  region          = var.region
  resource_prefix = var.resource_prefix
}
