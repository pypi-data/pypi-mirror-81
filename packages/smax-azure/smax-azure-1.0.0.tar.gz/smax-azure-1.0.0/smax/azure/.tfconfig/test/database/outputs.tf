output db_private_ip {
  value = data.null_data_source.db_srv_info.outputs["db_private_ip"]
}

output db_public_ip {
  value = data.null_data_source.db_srv_info.outputs["db_public_ip"]
}

