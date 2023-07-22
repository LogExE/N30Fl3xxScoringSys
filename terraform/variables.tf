variable "cloud_id" {
  type    = string
  default = "b1gnfug9omgb3nduktd2"
}

variable "folder_id" {
  type    = string
  default = "b1gsdge91vukh1d8u77r"
}

variable "service_key_path" {
  type = string
}

variable "instance_name" {
  type    = string
  default = "neopr"
}

variable "yandex_zone" {
  type    = string
  default = "ru-central1-b"
}

variable "network_name" {
  type    = string
  default = "network1"
}

variable "subnet_name" {
  type    = string
  default = "subnet1"
}

variable "dns_name" {
  type    = string
  default = "dns1"
}

variable "dns_zone" {
  type    = string
  default = "ourscoringsys.ru."
}
