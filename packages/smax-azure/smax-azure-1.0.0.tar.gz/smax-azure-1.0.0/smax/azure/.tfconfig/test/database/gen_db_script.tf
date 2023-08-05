data template_file setup_pg {
  template = file("${path.module}/scripts/setup_pg.sh.tpl")
  vars = {
    db_password = var.database_user_password
  }
}

resource local_file setup_pg_script {
  content  = data.template_file.setup_pg.rendered
  filename = "${var.upload_folder}/setup_pg.sh"
}

resource local_file pg_hba_conf {
  content  = file("${path.module}/scripts/pg_hba.conf")
  filename = "${var.upload_folder}/pg_hba.conf"
}

resource local_file extend_disk {
  content  = file("${path.module}/scripts/extend_disk.sh")
  filename = "${var.upload_folder}/extend_disk.sh"
}

resource local_file pg_conf {
  content  = file("${path.module}/scripts/postgresql.conf")
  filename = "${var.upload_folder}/postgresql.conf"
}