region = "us-east-1"
owner = "gd.martinez"

consumer_config = {
  lambda_name     = "consumer-application"
  repository_name = "consumer-lambda"
  image_version   = "3.0.0"
  env_variables   = {
    "LOG_LEVEL" = "INFO"
    "CREDIT_CARDS_URL = "http://credit-cards-service/credit-cards"
    "TRUE_NATIVE_URL" = "http://service-truenative/native"
    "SECRET_TOKEN_TRUE_NATIVE" = "token"
    "NOTIFICATIONS_URL" = "http://service-notifications/notifications"
  }
}

queue_name = "producer-consumer-queue"
number_of_messages_to_process = 1
