output kube_config {
  value = azurerm_kubernetes_cluster.cluster.kube_config_raw
}

output kube_config_admin {
  value = azurerm_kubernetes_cluster.cluster.kube_admin_config_raw
}

output version {
  value = data.azurerm_kubernetes_service_versions.current.latest_version
}