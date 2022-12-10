terraform {
  backend "s3" {
    bucket = "pipedrive-store-states"
    key = "python/flask"
    region = "eu-west-1"
  }
}
