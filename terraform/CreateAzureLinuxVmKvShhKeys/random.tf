# Generate a 4 character long random string used for the unique name
# of resources
resource "random_id" "name" {
  byte_length = 2
}