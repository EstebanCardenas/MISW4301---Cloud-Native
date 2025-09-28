region = "us-east-1"
owner = "af.donoso"

consumer_config = {
  lambda_name     = "consumer-application"
  repository_name = "consumer"
  image_version   = "3.0.0"
  env_variables   = {
    "LOG_LEVEL" = "INFO"
    "CREDIT_CARDS_URL" = "http://ad71c221904be47f6bf3487c02269208-181576732.us-east-1.elb.amazonaws.com/credit-cards"
    "TRUE_NATIVE_URL" = "http://ad71c221904be47f6bf3487c02269208-181576732.us-east-1.elb.amazonaws.com/native"
    "SECRET_TOKEN_TRUE_NATIVE" = "my-secret-token"
    "NOTIFICATIONS_URL" = "http://ad71c221904be47f6bf3487c02269208-181576732.us-east-1.elb.amazonaws.com/notifications"
  }
}

queue_name = "producer-consumer-queue"
number_of_messages_to_process = 1
