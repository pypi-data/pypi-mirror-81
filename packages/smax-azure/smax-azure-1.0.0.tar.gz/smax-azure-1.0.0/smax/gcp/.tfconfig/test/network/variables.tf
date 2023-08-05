variable resource_prefix {}
variable region {}

variable vpc_subnet_cidr_block {
  type = list(string)
  default = [
    "10.60.0.0/16",
    #"10.70.0.0/16",
    #"10.80.0.0/16",
    #"10.90.0.0/16",
    #"10.100.0.0/16",
  ]
}
