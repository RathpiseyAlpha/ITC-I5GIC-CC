provider "local" {
  # This provider is used for local operations.
}

resource "null_resource" "create_txt_file" {

  provisioner "local-exec" {
    command = "echo 'Congratulations!' > example.txt"
  }
}