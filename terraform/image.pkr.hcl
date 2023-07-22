variable "YC_FOLDER_ID" {
  type = string
  default = env("YC_FOLDER_ID")
}

variable "YC_ZONE" {
  type = string
  default = env("YC_ZONE")
}

variable "YC_SUBNET_ID" {
  type = string
  default = env("YC_SUBNET_ID")
}

source "yandex" "my_image" {
  folder_id           = "${var.YC_FOLDER_ID}"
  source_image_family = "debian-11"
  ssh_username        = "debian"
  use_ipv4_nat        = "true"
  image_description   = "My image"
  image_family        = "my-images"
  image_name          = "myimage"
  subnet_id           = "${var.YC_SUBNET_ID}"
  disk_type           = "network-hdd"
  zone                = "${var.YC_ZONE}"
}

build {
  sources = ["source.yandex.my_image"]

  provisioner "shell" {
    script = "init.sh"
  }
}