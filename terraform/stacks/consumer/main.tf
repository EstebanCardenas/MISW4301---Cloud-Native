###########################################################
# Consumer Stack Configuration
###########################################################

module "sqs_queue" {
  source     = "../../modules/sqs"
  queue_name = var.queue_name
}

module "consumer" {
  source          = "../../modules/lambda"
  lambda_name     = var.consumer_config.lambda_name
  repository_name = var.consumer_config.repository_name
  image_version   = var.consumer_config.image_version
  env_variables   = var.consumer_config.env_variables
}

# Create an event source mapping to connect the SQS queue to the consumer Lambda.
# This configures Lambda to automatically pull messages from the SQS queue.
resource "aws_lambda_event_source_mapping" "consumer_mapping" {
  event_source_arn = module.sqs_queue.sqs_queue_arn
  function_name    = module.consumer.lambda_name
  batch_size       = var.number_of_messages_to_process
  enabled          = true
}
