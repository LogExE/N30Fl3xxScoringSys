
resource "yandex_compute_image" "debian11" {
  source_family = "debian-11"
}

resource "yandex_compute_instance" "neopr" {
  name = var.instance_name

  platform_id = "standard-v3"
  resources {
    core_fraction = 20
    cores         = 2
    memory        = 2
  }

  boot_disk {
    initialize_params {
      image_id = yandex_compute_image.debian11.id
      size     = 10
    }
  }

  network_interface {
    subnet_id = yandex_vpc_subnet.subnet-1.id
    nat       = true
  }

  scheduling_policy {
    preemptible = true
  }

  metadata = {
    user-data = "${file("meta.txt")}"
  }
}

resource "yandex_vpc_network" "network-1" {
  name = var.network_name
}

resource "yandex_vpc_subnet" "subnet-1" {
  name           = var.subnet_name
  zone           = var.yandex_zone
  network_id     = yandex_vpc_network.network-1.id
  v4_cidr_blocks = ["192.168.10.0/24"]
}

output "external_ip_address_neopr" {
  value = yandex_compute_instance.neopr.network_interface.0.nat_ip_address
}
