variable project {
  description = "GCP project where infra created in"
  default     = "itom-devops-nonprod"
}

variable region {
  description = "GCP region"
  default     = "us-east4"
}

variable filestore_share_name {
  description = "GCP file store root folder"
  default     = "suitefs"
}

variable filestore_gb {
  description = "GCP file store size (GB)"
  default     = 1024
}

variable vm_user {
  description = "bastion ssh user name"
  default     = "centos"
}

variable database_password {
  default = "Admin_1234"
}

variable k8s_version {
  default = "1.15"
}

variable pg_version {
  default = "10"
}

variable fqdn {
  description = "Suite web address"
  default     = "testonly.cdfdev06.sma-ng.com"
}

variable registry_orgname {
  description = "GCP docker registry organization"
  default     = "itom-smax-nonprod"
}

