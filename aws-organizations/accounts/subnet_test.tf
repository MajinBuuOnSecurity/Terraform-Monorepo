data "aws_subnets" "public" {
 filter {
   name = "map-public-ip-on-launch"
   values = [true]
 }
}

data "aws_subnet" "public_subnet_map" {
  for_each = toset(data.aws_subnets.public.ids)
  id       = each.value
}

output "public_subnet_map" {
  value = [for subnet in data.aws_subnet.public_subnet_map : subnet.arn]
}
