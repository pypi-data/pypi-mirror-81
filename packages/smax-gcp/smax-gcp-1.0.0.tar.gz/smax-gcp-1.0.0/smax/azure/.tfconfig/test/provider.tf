variable "subscription_id" {
  description = "The subscription id for the Service Principal to use"
  default     = "6f33f7c2-ad9f-4cde-b090-e4065a475109"
}

variable "tenant_id" {
  description = "The tenant id for the Service Principal to use"
}

variable "client_id" {
  description = "The Client ID for the Service Principal to use"
}

variable "client_secret" {
  description = "The Client Secret for the Service Principal to use"
}

provider "azurerm" {
  # DONOT use ">="!! Just use fixed version to keep stable
  #version         = "1.44.0"
  subscription_id = var.subscription_id
  client_id       = var.client_id
  client_secret   = var.client_secret
  tenant_id       = var.tenant_id
  features {}
}

