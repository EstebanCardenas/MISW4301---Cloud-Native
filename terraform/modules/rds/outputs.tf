output "address" {
  description = "Endpoint de la instancia RDS."
  value       = aws_db_instance.mi_rds_postgres.address
}

output "port" {
  description = "Puerto de la instancia RDS."
  value       = aws_db_instance.mi_rds_postgres.port
}

output "engine" {
  description = "Motor de la base de datos RDS."
  value       = aws_db_instance.mi_rds_postgres.engine
}
