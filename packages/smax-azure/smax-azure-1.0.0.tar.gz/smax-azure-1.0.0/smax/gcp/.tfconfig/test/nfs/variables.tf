variable resource_prefix {}
variable project {}
variable region {}

variable gcp_filestore_tier {
  default = "STANDARD"
}

variable filestore_gb {
  default = 1024
}

variable filestore_share_name {
}

variable vnet_name {}