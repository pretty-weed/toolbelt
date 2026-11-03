
variable "BASEFILE" {
  default = "../docker/ci_tools/Dockerfile"
}

group "default" {
  targets = ["workImg"]
}

target "base" {
  dockerfile = BASEFILE
  tags = ["taskfile-test-base:latest"]
}

target "workImg" {
  dockerfile = "Dockerfile.test"
  tags = ["taskfile-test:latest"]
  contexts = {
    base = "target:base"
  }
}
