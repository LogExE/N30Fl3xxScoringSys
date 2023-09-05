#resource "yandex_dns_zone" "zone1" {
#  name = var.dns_name
#
#  zone   = var.dns_zone
#  public = true
#}

#resource "yandex_dns_recordset" "inst_record" {
#  zone_id = yandex_dns_zone.zone1.id
#  name = var.dns_zone
#  type = "A"
#  ttl = 200
#  data = [yandex_compute_instance.neopr.network_interface.0.nat_ip_address]
#}
