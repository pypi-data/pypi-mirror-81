variable resource_prefix {}
variable database_machine_type {
  description = "database machine type, such as: db-custom-4-15360, db-custom-8-30720, refer to:https://cloud.google.com/sql/docs/postgres/create-instance"
  default     = "db-custom-4-15360"
}

variable database_disk_size {
  default = 100
}

variable database_user_name {}
variable database_user_password {}
variable vnet_link {}
variable db_version {
  default = "POSTGRES_10"
}

