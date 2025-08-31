module "ecr_instances" {
  source = "../../modules/registry"
  for_each = var.repository_names
  keep_tags_number = var.keep_tags_number
  repository_name = each.value
}
